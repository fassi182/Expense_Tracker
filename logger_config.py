import logging
import os

# ---------------- Absolute path for logs ----------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# ---------------- Logger configuration ----------------
logger = logging.getLogger("expense_tracker")
logger.setLevel(logging.INFO)  # Capture INFO and above

# Remove all handlers if re-imported
if logger.hasHandlers():
    logger.handlers.clear()

# File handler (write logs only to file)
file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Test message
logger.info("Logger initialized successfully. Logs will be written ONLY to logs/app.log")
