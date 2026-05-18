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

## UML Sequence Diagram:
<img width="960" height="720" alt="UML User Authentication" src="https://github.com/user-attachments/assets/2ef49e4f-8906-4e19-a518-e67c9b489a61" />

