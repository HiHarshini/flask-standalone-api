from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# ---- HARD-CODED DATA ----
DATA = {
    "1001": {
        "name": "Harshini",
        "department": "Data Science",
        "document": "Employee Profile A"
    },
    "1002": {
        "name": "Rahul",
        "department": "Backend",
        "document": "Employee Profile B"
    },
    "1003": {
        "name": "Sneha",
        "department": "AI/ML",
        "document": "Employee Profile C"
    }
}

# ---- SWAGGER CONFIG ----
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Standalone Stub API"}
)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Standalone Stub API is running"})

@app.route("/lookup", methods=["POST"])
def lookup():
    payload = request.get_json()

    if not payload or "id" not in payload:
        return jsonify({"message": "ID is required"}), 400

    request_id = payload["id"]

    if request_id in DATA:
        return jsonify({
            "status": "success",
            "message": "Document found",
            "data": DATA[request_id]
        })
    else:
        return jsonify({"message": "Document not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)