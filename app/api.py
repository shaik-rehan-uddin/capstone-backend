from flask import request, jsonify, current_app
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.models.filters import BaseFilter
from openai import OpenAI
from . import appbuilder, db
from .models import ChatSession, ChatData
from os import environ
import uuid

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
    response = current_app.make_default_options_response()
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


class ChatApi(BaseApi):
    route_base = "/api/chatrequest"

    @expose("/get_response", methods=["GET", "POST", "OPTIONS"])
    def get_response(self):
        """
        Get response from OpenAI API for a given chat session.

        ---
        get:
            description: Get a response from OpenAI API for a given chat session
            responses:
                200:
                    description: Response received successfully
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    response:
                                        type: string
                                        description: The response received from OpenAI API
                                    session_id:
                                        type: string
                                        description: The session ID associated with the chat session
                400:
                    description: Bad request
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    message:
                                        type: string
                                        description: Error message describing the issue
        post:
            description: Send a message to OpenAI API and get a response
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
                                    description: The message sent by the user
                                session_id:
                                    type: string
                                    description: The session ID associated with the chat session
            responses:
                200:
                    description: Response received successfully
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    response:
                                        type: string
                                        description: The response received from OpenAI API
                                    session_id:
                                        type: string
                                        description: The session ID associated with the chat session
                400:
                    description: Bad request
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    message:
                                        type: string
                                        description: Error message describing the issue
        options:
            description: CORS preflight
            responses:
                200:
                    description: CORS preflight response
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    message:
                                        type: string
                                        description: Description of the preflight response
        """
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
                    chat_data_entries = (
                        db.session.query(ChatData)
                        .filter_by(chat_session_id=session_id)
                        .all()
                    )
                    print(chat_data_entries)
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
                    messages=context_messages
                    + [{"role": "user", "content": user_message}],
                )

                # Extract and return the response
                if completion and completion.choices:
                    response_message = completion.choices[0].message.content

                    create_chat_data(session_id, user_message, response_message)
                    return _corsify_actual_response(
                        jsonify(
                            {"response": response_message, "session_id": session_id}
                        )
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


appbuilder.add_api(ChatApi)
