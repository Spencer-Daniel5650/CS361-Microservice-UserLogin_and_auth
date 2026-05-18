# CS361 Microservice 2
# Contributers: Daniel, Gerardo, Elise, Mathew, Thampanhaboth
# DRAFT VERSION

import json
import time
from urllib import error, request


BASE_URL = "http://localhost:8000"


def post_json(path, data):
    url = BASE_URL + path
    body = json.dumps(data).encode("utf-8")

    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    return send_request(req)


def get_json(path):
    url = BASE_URL + path
    req = request.Request(url, method="GET")
    return send_request(req)


def send_request(req):
    try:
        with request.urlopen(req) as response:
            response_body = response.read().decode("utf-8")
            return response.status, json.loads(response_body)
    except error.HTTPError as http_error:
        response_body = http_error.read().decode("utf-8")
        return http_error.code, json.loads(response_body)


def print_result(title, status_code, data):
    print("\n" + title)
    print("HTTP status:", status_code)
    print(json.dumps(data, indent=2))


def main():
    test_email = f"demo_user_{int(time.time())}@example.com"
    test_password = "SecurePassword123"

    register_status, register_data = post_json("/auth/register", {
        "name": "Demo User",
        "email": test_email,
        "password": test_password,
        "role": "user",
    })
    print_result("1. Register user", register_status, register_data)

    login_status, login_data = post_json("/auth/login", {
        "email": test_email,
        "password": test_password,
    })
    print_result("2. Login user", login_status, login_data)

    if login_data.get("status") == "success":
        user_id = login_data["userID"]
        role_status, role_data = get_json(f"/auth/role/{user_id}")
        print_result("3. Check user role", role_status, role_data)


if __name__ == "__main__":
    main()
