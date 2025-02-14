import logging

# Configure logging
logging.basicConfig(filename="mcp_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_interaction(query, response, category):
    """Logs interactions for auditing."""
    logging.info(f"{category}: {query} -> {response}")
