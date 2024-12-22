import os
import json
import datetime
import traceback
import threading

class Logger:
    LOG_DIRECTORY = os.path.join(os.getenv('LOCALAPPDATA', os.getcwd()), "WCG847", "YANIM", "Logs")
    LOG_FILE = os.path.join(LOG_DIRECTORY, "log.json")
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    _lock = threading.Lock()

    def __init__(self):
        self._setup_log_directory()

    def _setup_log_directory(self):
        try:
            os.makedirs(self.LOG_DIRECTORY, exist_ok=True)
        except Exception as e:
            print(f"Failed to create log directory: {self.LOG_DIRECTORY}. Error: {e}")

    def log_error(self, error_code, message, exception=None):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "error_code": error_code,
            "message": message,
            "exception": str(exception) if exception else None,
            "traceback": traceback.format_exc() if exception else None
        }
        self._write_log(log_entry)

    def log_info(self, message):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "message": message,
            "type": "info"
        }
        self._write_log(log_entry)

    def _write_log(self, log_entry):
        try:
            with self._lock:
                # Check if log file exceeds size limit
                if os.path.exists(self.LOG_FILE) and os.path.getsize(self.LOG_FILE) > self.MAX_LOG_FILE_SIZE:
                    archive_file = self.LOG_FILE.replace(".json", "_archive.json")
                    os.rename(self.LOG_FILE, archive_file)

                if not os.path.exists(self.LOG_FILE):
                    with open(self.LOG_FILE, 'w') as file:
                        json.dump([], file)

                with open(self.LOG_FILE, 'r+') as file:
                    logs = json.load(file)
                    logs.append(log_entry)
                    file.seek(0)
                    file.truncate()
                    json.dump(logs, file, indent=4)
        except Exception as e:
            print(f"Failed to write log entry. Error: {e}")

    def log_crash(self, error_code, exception):
        crash_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "error_code": error_code,
            "message": "Application crash detected.",
            "exception": str(exception),
            "traceback": traceback.format_exc()
        }
        self._write_log(crash_log)
        print(f"Application crashed with error code {error_code}. Logs saved to {self.LOG_FILE}")
