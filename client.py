import requests

SERVER_URL = "http://127.0.0.1:5000/api/mcp/query"
RESET_URL = "http://127.0.0.1:5000/api/mcp/reset"

def send_query(user_query):
    """Sends a query to the MCP server and returns the response."""
    response = requests.post(SERVER_URL, json={"query": user_query})
    return response.json()

if __name__ == "__main__":
    while True:
        print("\n\n====================================================================================")
        user_input = input("\nEnter your query (or 'reset' to start over, 'exit' to quit) >>>  ")

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "reset":
            requests.post(RESET_URL)
            print("Conversation reset.")
            continue

        response = send_query(user_input)
        print(f"\n\nGENERATED COMMAND:\n {response.get('command')}")
        print(f"\n\nEXECUTION OUTPUT:\n {response.get('output')}")
