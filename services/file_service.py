import json
import os
from logger_config import logger

def read_json(path, fallback):
    """
    Reads JSON from the given file path.
    Returns 'fallback' if the file does not exist or fails to read.
    """
    if not os.path.exists(path):
        logger.info(f"File not found, returning fallback: {path}")
        return fallback

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Successfully read JSON from {path}")
            return data
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Failed to read JSON from {path} | Error: {e}")
        return fallback

def write_json(path, data):
    """
    Writes the provided data to the JSON file at 'path'.
    Logs success or failure.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Successfully wrote JSON to {path}")
    except (IOError, OSError) as e:
        logger.error(f"Failed to write JSON to {path} | Error: {e}")
