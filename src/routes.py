from flask import request, jsonify, make_response
from openai import OpenAI
from models import db, ChatSession, ChatData
from datetime import datetime
import uuid
from os import environ

client = OpenAI(api_key=environ.get("OPENAI_API_KEY"))


def initialize_chat_session():
    session = ChatSession(
        id=str(uuid.uuid4()),
    )
    db.session.add(session)
    db.session.commit()
    return session.id


def create_chat_data(session_id, question, answer):
    chat_data = ChatData(
        id=str(uuid.uuid4()),
        question_asked=question,
        answer_provided=answer,
        chat_session_id=session_id,
    )
    db.session.add(chat_data)
    db.session.commit()


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def get_response():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    elif request.method == "POST":
        try:
            data = request.get_json()
            user_message = data.get("message", "")
            session_id = data.get("session_id")

            # Retrieve existing chat data associated with session ID
            context_messages = []
            if session_id:
                chat_data_entries = ChatData.query.filter_by(
                    chat_session_id=session_id
                ).all()
                for entry in chat_data_entries:
                    context_messages.append(
                        {"role": "user", "content": entry.question_asked}
                    )
                    context_messages.append(
                        {"role": "system", "content": entry.answer_provided}
                    )

            # Send non-empty message to OpenAI API to get a response
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=context_messages + [{"role": "user", "content": user_message}],
            )

            # Extract and return the response
            if completion and completion.choices:
                response_message = completion.choices[0].message.content

                create_chat_data(session_id, user_message, response_message)
                return _corsify_actual_response(
                    jsonify({"response": response_message, "session_id": session_id})
                )
            else:
                return _corsify_actual_response(
                    jsonify({"message": "No response received from OpenAI API"})
                )
        except Exception as e:
            return _corsify_actual_response(
                jsonify({"message": "Error processing request", "error": str(e)})
            )
    elif request.method == "GET":
        try:
            session_id = initialize_chat_session()
            return _corsify_actual_response(jsonify({"session_id": session_id}))
        except Exception as e:
            return _corsify_actual_response(
                jsonify({"message": "Error processing request", "error": str(e)})
            )
