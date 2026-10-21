"""
Practice target: minimal Fitness Flask API for Week 2 reconnaissance.

LOCAL USE ONLY. Run on your own machine and recon against 127.0.0.1.
This stands in for the 'target Flask API' the course references but did not supply.
It is intentionally simple so you can practise endpoint/parameter mapping.

Run:
    pip install flask
    python3 app.py
Then recon:
    curl -s http://127.0.0.1:5000/api/health
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory sample data (no real users, no secrets)
USERS = {
    1: {"id": 1, "name": "Alice", "plan": "pro"},
    2: {"id": 2, "name": "Bob", "plan": "free"},
}
WORKOUTS = {
    1: [{"id": 10, "type": "run", "minutes": 30}],
    2: [{"id": 11, "type": "cycle", "minutes": 45}],
}


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "fitness-api", "version": "v1"})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    user = data.get("username")
    return jsonify({"message": "login endpoint", "received_user": user}), 200


@app.route("/api/users/<int:user_id>/profile", methods=["GET"])
def profile(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify(user)


@app.route("/api/users/<int:user_id>/workouts", methods=["GET", "POST"])
def workouts(user_id):
    if request.method == "POST":
        body = request.get_json(silent=True) or {}
        return jsonify({"message": "created", "echo": body}), 201
    limit = request.args.get("limit", default=10, type=int)
    return jsonify(WORKOUTS.get(user_id, [])[:limit])


@app.route("/api/admin/stats", methods=["GET"])
def admin_stats():
    return jsonify({"total_users": len(USERS), "total_workouts": len(WORKOUTS)})


if __name__ == "__main__":
    # Note for the hardening phase: debug=True is itself API8 (Security Misconfiguration).
    app.run(host="127.0.0.1", port=5000)
