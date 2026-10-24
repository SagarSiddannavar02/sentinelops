from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os
import time

app = Flask(__name__)

START_TIME = time.time()

# Count requests by HTTP method, endpoint, and status code.
REQUEST_COUNT = Counter(
    "sentinelops_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# Measure how long requests take.
REQUEST_LATENCY = Histogram(
    "sentinelops_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"]
)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def record_metrics(response):
    # Avoid counting Prometheus scraping its own metrics endpoint.
    if request.path != "/metrics":
        duration = time.time() - getattr(
            request, "start_time", time.time()
        )

        REQUEST_COUNT.labels(
            request.method,
            request.path,
            str(response.status_code)
        ).inc()

        REQUEST_LATENCY.labels(request.path).observe(duration)

    return response


@app.route("/")
def home():
    return jsonify({
        "service": "SentinelOps",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/info")
def info():
    return jsonify({
        "service": "SentinelOps",
        "hostname": os.getenv("HOSTNAME", "local"),
        "uptime_seconds": round(time.time() - START_TIME, 2)
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)