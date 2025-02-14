import subprocess
import ollama
import platform
from flask import session
from .logger import log_interaction

# Restricted system commands for security
RESTRICTED_COMMANDS = ["rm", "shutdown", "reboot", "kill", "format", "del", "rmdir"]

def initialize_session():
    """Ensure conversation history is initialized."""
    if "conversation" not in session:
        session["conversation"] = []

def reset_conversation():
    """Clear the conversation history."""
    session["conversation"] = []

def generate_command(user_query: str) -> str:
    """Generate a system command while keeping conversation history intact."""
    initialize_session()

    if user_query.lower() == "reset":
        reset_conversation()
        return "Conversation reset."

    # Detect OS
    user_os = platform.system().lower()

    # Define strict system prompt for LLM
    system_prompt = f"""
    You are an MCP-compliant system command generator. Your job is to generate ONLY executable system commands based on user queries while maintaining conversation history.
    - Do NOT include explanations, greetings, or unrelated text.
    - Ensure commands match the user's OS ({user_os}).
    - Use context from previous queries.

    Linux:
      - Use 'ls' for listing files
      - Use 'df -h' for disk space
      - Use 'pwd' for current directory
      - Use 'cat filename' for reading files
      
    Windows:
      - Use 'dir' for listing files
      - Use 'wmic logicaldisk get size,freespace,caption' for disk space
      - Use 'cd' for current directory
      - Use 'type filename' for reading files

    Example Conversations:
    User: What is my current directory?
    Assistant: cd  (Windows) / pwd  (Linux)
    
    User: List files in this directory
    Assistant: dir  (Windows) / ls  (Linux)

    User: Read file1.txt
    Assistant: type file1.txt  (Windows) / cat file1.txt  (Linux)
    """

    # Add user query to conversation history
    session["conversation"].append({"role": "user", "content": user_query})

    # Query LLM with full conversation history
    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": system_prompt},
        *session["conversation"]  # Include complete previous conversation history
    ])

    # Extract command
    command = response["message"]["content"].strip()

    # Save response in conversation history
    session["conversation"].append({"role": "assistant", "content": command})

    # Log interaction
    log_interaction(user_query, command, "Generated command")

    return command

def execute_command(command: str) -> str:
    """Execute the generated system command securely."""
    if any(keyword in command for keyword in RESTRICTED_COMMANDS):
        log_interaction(command, "Blocked", "Restricted command")
        return "Error: Restricted command detected."

    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        output = result.stdout if result.stdout else result.stderr

        # Store execution result in conversation history
        session["conversation"].append({"role": "assistant", "content": output})

        log_interaction(command, output, "Execution result")
        return output
    except Exception as e:
        return f"Error: {str(e)}"
