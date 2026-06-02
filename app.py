# # CS361 Microservice 2
# Contributers: Daniel, Gerardo, Elise, Mathew, Thampanhaboth
# DRAFT VERSION

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from database import add_user, find_user_by_email, get_public_user, load_users


app = Flask(__name__)

ALLOWED_ROLES = {"admin", "manager", "user"}


def make_response(status, message, status_code, **extra_data):
    response_body = {
        "status": status,
        "message": message,
    }
    response_body.update(extra_data)
    return jsonify(response_body), status_code


def valid_email(email):
    return isinstance(email, str) and "@" in email and "." in email


def valid_password(password):
    return isinstance(password, str) and len(password) >= 6


@app.get("/")
def home():
    return jsonify({
        "service": "User Authentication Microservice",
        "endpoints": ["/auth/register", "/auth/login", "/auth/role/<user_id>"],
    })


@app.get("/health")
def health():
    return jsonify({"status": "success", "message": "Service is running."})


@app.post("/auth/register")
def register():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "user").strip().lower()

    if not name:
        return make_response("error", "Name is required.", 400)

    if not valid_email(email):
        return make_response("error", "A valid email is required.", 400)

    if not valid_password(password):
        return make_response("error", "Password must be at least 6 characters.", 400)

    if role not in ALLOWED_ROLES:
        return make_response("error", "Role must be admin, manager, or user.", 400)

    if find_user_by_email(email):
        return make_response("error", "Email already exists.", 409)

    user = add_user({
        "name": name,
        "email": email,
        "password_hash": generate_password_hash(password, method="pbkdf2:sha256"),
        "role": role,
    })

    return make_response(
        "success",
        "Account created successfully.",
        201,
        userID=user["id"],
        role=user["role"],
        user=get_public_user(user),
    )


def parse_login_data(request):
    data = request.get_json(silent=True) or {}
    return data.get("email", "").strip().lower(), data.get("password", "")


def validate_login_data(email, password):
    if not valid_email(email) or not password:
        return "Invalid email or password."
    return None


def authenticate_user(email, password):
    user = find_user_by_email(email)
    if not user:
        return None
    if not check_password_hash(user["password_hash"], password):
        return None
    return user


@app.post("/auth/login")
def login():
    email, password = parse_login_data(request)

    error = validate_login_data(email, password)
    if error:
        return login_error()

    user = authenticate_user(email, password)
    if not user:
        return login_error()

    return make_response(
        "success",
        "Login successful.",
        200,
        userID=user["id"],
        role=user["role"],
        user=get_public_user(user),
    )


@app.get("/auth/role/<user_id>")
def get_role(user_id):
    users = load_users()

    for user in users:
        if user["id"] == user_id:
            return make_response(
                "success",
                "Role found.",
                200,
                userID=user["id"],
                role=user["role"],
            )

    return make_response("error", "User not found.", 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
