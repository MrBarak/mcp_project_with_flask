**MCP (Model Context Protocol) Client-Server System**

This project implements an MCP-compliant Client-Server system using Flask and Ollama to dynamically generate and execute system commands while maintaining full conversation context.

📌 Features

Maintains Conversation History: Uses session-based storage for chat context.

Contextual Command Generation: Commands are generated based on previous queries.

Secure Command Execution: Blocks restricted system commands to prevent security risks.

Multi-OS Support: Adapts to Windows and Linux for accurate command execution.

Logging: Stores interactions for debugging and auditing.

🛠️ Installation

1️⃣ Clone the Repository

git clone https://github.com/MrBarak/mcp_project_with_flask.git
cd mcp_project_with_flask

2️⃣ Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate    # For Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Install and Run Ollama (LLM)

If you haven't installed Ollama:

curl -fsSL https://ollama.com/install.sh | sh  # For Linux/Mac
winget install ollama  # For Windows

Then, start Ollama:

ollama serve

🚀 Running the MCP Server

python app.py

The Flask server will start on http://127.0.0.1:5000

📡 MCP Client Usage

Run the client to interact with the system:

python client.py

Now you can give prompts on terminal
