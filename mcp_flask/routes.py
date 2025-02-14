from flask import Blueprint, request, jsonify, session
from .handler import generate_command, execute_command

api_bp = Blueprint("api", __name__)

@api_bp.route("/query", methods=["POST"])
def process_query():
    data = request.json
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    command = generate_command(user_query)
    output = execute_command(command)

    return jsonify({"command": command, "output": output})

@api_bp.route("/reset", methods=["POST"])
def reset_session():
    """Clears the conversation history in the session."""
    session.pop("conversation", None)
    return jsonify({"message": "Session reset successfully."})
