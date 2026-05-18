# CS361 User Authentication Microservice
Contributers: Daniel, Gerardo, Elise, Mathew, Thampanhaboth

This is our microservice 2 for the team project. It is a small REST API that lets other programs register users, log users in, and check a user's role.


## What it does

- Register a new user
- Prevent duplicate emails
- Hash passwords before saving them
- Log in with email and password
- Return user ID and role after login
- Check a user's role by user ID
- Never return the user's password in an API response

## How it is set up 

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The server runs at:

```text
http://localhost:8000
```

## How do I request data?

Other programs request data by sending HTTP requests to the microservice.

Register request example:

```python
import json
from urllib import request

url = "http://localhost:8000/auth/register"
data = {
    "name": "Bob",
    "email": "bob@example.com",
    "password": "SecurePassword123",
    "role": "user"
}

body = json.dumps(data).encode("utf-8")

req = request.Request(
    url,
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST"
)
```

Login request example:

```python
import json
from urllib import request

url = "http://localhost:8000/auth/login"
data = {
    "email": "bob@example.com",
    "password": "SecurePassword123"
}

body = json.dumps(data).encode("utf-8")

req = request.Request(
    url,
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST"
)
```

Role check request example:

```python
from urllib import request

user_id = "the-user-id-from-login"
req = request.Request(
    f"http://localhost:8000/auth/role/{user_id}",
    method="GET"
)
```

## How to programmatically receive data

The microservice responds with JSON. Other programs receive the response, decode it, and then read values like `status`, `message`, `userID`, and `role`.

Receive response example:

```python
import json
from urllib import request

with request.urlopen(req) as response:
    response_body = response.read().decode("utf-8")
    data = json.loads(response_body)

print(data["status"])
print(data["message"])

if data["status"] == "success":
    print(data["userID"])
    print(data["role"])
```

Example successful registration response:

```json
{
  "status": "success",
  "message": "Account created successfully.",
  "userID": "generated-user-id",
  "role": "user",
  "user": {
    "id": "generated-user-id",
    "name": "Bob",
    "email": "bob@example.com",
    "role": "user"
  }
}
```

Example successful login response:

```json
{
  "status": "success",
  "message": "Login successful.",
  "userID": "generated-user-id",
  "role": "user",
  "user": {
    "id": "generated-user-id",
    "name": "Bob",
    "email": "bob@example.com",
    "role": "user"
  }
}
```

## UML Sequence Diagram:
<img width="960" height="720" alt="UML User Authentication" src="https://github.com/user-attachments/assets/2ef49e4f-8906-4e19-a518-e67c9b489a61" />

