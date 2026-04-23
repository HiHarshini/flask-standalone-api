import os
from flask import Flask, request, jsonify, send_file
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

DOCUMENTS_DIR = "documents"

# ---- Swagger ----
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Standalone LOA Stub API"}
)
app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)


def error_response(message, status_code):
    return jsonify({
        "status": "error",
        "message": message
    }), status_code


@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "Stub API is running"
    })


@app.route("/lookup", methods=["POST"])
def lookup():
    app.logger.info("Received lookup request")

    payload = request.get_json()

    # ---- Strict validation ----
    if not payload or "id" not in payload:
        return error_response("Field 'id' is required", 400)

    if payload["id"] is None or payload["id"] == "":
        return error_response("Field 'id' must not be empty", 400)

    # Normalize ID to string
    request_id = str(payload["id"])

    file_name = f"LOA_{request_id}.pdf"
    file_path = os.path.join(DOCUMENTS_DIR, file_name)

    if not os.path.exists(file_path):
        return error_response("Document not found", 404)

    response = send_file(
        file_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=file_name
    )

    # ---- Metadata in headers ----
    response.headers["X-Employee-Id"] = request_id
    response.headers["X-Document-Type"] = "LOA"

    return response


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)