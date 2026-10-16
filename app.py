import os
import shutil
import csv
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import time
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    multiprocess
)
from flask import Response

app = Flask(__name__)

# Total number of HTTP requests, grouped by method, endpoint and status.
REQUEST_COUNT = Counter(
    "file_organizer_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"]
)

# Time taken to process HTTP requests, in seconds.
REQUEST_LATENCY = Histogram(
    "file_organizer_http_request_duration_seconds",
    "HTTP request processing duration in seconds",
    ["method", "endpoint"]
)

# File categories (unchanged from original)
file_types = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
}

@app.before_request
def start_request_timer():
    request.start_time = time.perf_counter()


@app.after_request
def record_request_metrics(response):
    # Do not count requests made to the metrics endpoint.
    if request.endpoint == "metrics":
        return response

    start_time = getattr(request, "start_time", None)

    if start_time is not None:
        duration = time.perf_counter() - start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint or "unknown",
            http_status=str(response.status_code)
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.endpoint or "unknown"
        ).observe(duration)

    return response

CSV_LOG = "organizer_log.csv"


def log_to_csv(file_name, destination, status):
    """Append a move action to the CSV log file."""
    file_exists = os.path.isfile(CSV_LOG)
    with open(CSV_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "File", "Destination", "Status"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_name, destination, status])


def read_csv_log():
    """Read all entries from the CSV log."""
    if not os.path.isfile(CSV_LOG):
        return []
    with open(CSV_LOG, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def organize_files(folder_path):
    """Organize files and return a list of log entries."""
    logs = []

    if not os.path.isdir(folder_path):
        return None, "Invalid folder path."

    try:
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)

            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                moved = False

                for folder, extensions in file_types.items():
                    if ext.lower() in extensions:
                        dest_folder = os.path.join(folder_path, folder)
                        os.makedirs(dest_folder, exist_ok=True)
                        shutil.move(file_path, dest_folder)
                        log_to_csv(file, folder, "Moved")
                        logs.append({"file": file, "destination": folder, "status": "Moved"})
                        moved = True
                        break

                if not moved:
                    dest_folder = os.path.join(folder_path, "Others")
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(file_path, dest_folder)
                    log_to_csv(file, "Others", "Moved")
                    logs.append({"file": file, "destination": "Others", "status": "Moved"})

        return logs, None

    except Exception:
        app.logger.exception("An error occurred while organizing files.")
        return None, "An unexpected error occurred while organizing the folder."


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/")
def index():
    return render_template("index.html", categories=list(file_types.keys()))


@app.route("/organize", methods=["POST"])
def organize():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "A valid JSON object is required."
        }), 400

    folder_path = data.get("folder_path", "")

    if not isinstance(folder_path, str):
        return jsonify({
            "success": False,
            "error": "folder_path must be a string."
        }), 400

    folder_path = folder_path.strip()

    if not folder_path:
        return jsonify({
            "success": False,
            "error": "No folder path provided."
        }), 400

    logs, error = organize_files(folder_path)

    if error:
        return jsonify({
            "success": False,
            "error": error
        }), 400

    return jsonify({
        "success": True,
        "logs": logs,
        "total": len(logs)
    }), 200


@app.route("/history")
def history():
    logs = read_csv_log()
    return jsonify({"logs": logs})


@app.route("/clear-history", methods=["POST"])
def clear_history():
    if os.path.isfile(CSV_LOG):
        os.remove(CSV_LOG)
    return jsonify({"success": True})

@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)

    return Response(
        generate_latest(registry),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(debug=True)