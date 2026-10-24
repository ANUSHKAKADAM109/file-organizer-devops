from flask import Flask, jsonify, request
from datetime import datetime, timezone
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

received_alerts = []


@app.route("/alert-webhook", methods=["POST"])
def receive_alert():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    alerts = payload.get("alerts", [])

    for alert in alerts:
        received_alerts.append({
            "received_at": datetime.now(timezone.utc).isoformat(),
            "alertname": alert.get("labels", {}).get("alertname", "unknown"),
            "status": alert.get("status", "unknown"),
            "severity": alert.get("labels", {}).get("severity", "unknown"),
            "summary": alert.get("annotations", {}).get("summary", ""),
        })

    app.logger.info("Received %d alert(s)", len(alerts))
    return jsonify({"received": len(alerts)}), 200


@app.route("/alerts", methods=["GET"])
def list_alerts():
    return jsonify(received_alerts)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)