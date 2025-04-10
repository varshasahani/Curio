# Curio
A Place where user can ask questions, answer a question and like replies
# Curio

Curio is a Django-based web application that allows users to post questions, reply to questions, and interact with nested replies. The project is designed to demonstrate the functionality of a Q&A platform.

---

## Features

- User authentication (login, logout, and registration)
- Post questions and replies
- Nested replies for discussions
- Like functionality for replies
- Dynamic updates using AJAX

---

## Requirements

The project dependencies are listed in the `requirements.txt` file. To install them, run:

```bash
pip install -r [requirements.txt](http://_vscodecontentref_/0)


Installation
Clone the repository:

git clone <repository-url>
cd Curio
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Apply migrations:

python manage.py migrate
Create a superuser:

python manage.py createsuperuser
Run the development server:

python manage.py runserver
Open the application in your browser:

http://127.0.0.1:8000/

Usage
Register: Create a new account.
Login: Log in to your account.
Post Questions: Add new questions to the platform.
Reply: Reply to questions or other replies.
Like: Like replies to show appreciation.
