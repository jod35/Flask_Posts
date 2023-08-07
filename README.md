# Flask_Posts
Sure! Below is a sample README.md file for a Flask RESTful API project:

This project is a Flask RESTful API that provides endpoints for various tasks. It is built using Python and Flask, and it follows the RESTful API principles to provide a straightforward and efficient way to interact with the application.

## Getting Started

Follow the instructions below to set up and run the API on your local machine.

### Prerequisites

- Python 3.7 or higher
- Virtualenv (recommended)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jod35/Flask_Posts.git
cd Flask_Posts
```

2. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

### Configuration

You may need to configure certain settings based on your environment or requirements. Create a `.env` file in the project root and specify the necessary environment variables, such as database connection details, API keys, etc.

```plaintext
FLASK_SECRET_KEY=your-secret-key
FLASK_SQLALCHEMY_DATABASE_URI=your-sqlalchemy-uri
FLASK__DEBUG=debug-value

```

### Running the API

To start the Flask development server, run the following command:

```bash
python app.py
```

The API will be accessible at `http://127.0.0.1:5000/`.

### API Endpoints

The API provides the following endpoints:
| Endpoint         | Method | Description                              | Query Parameters       | Path Parameters | 
|------------------|--------|------------------------------------------|------------------------|-----------------|
| /v1/posts       | GET    | Get a paginated list of all posts        | page , posts      |                      |
| /v1/posts/:id   | GET    | Get a specific post by its ID            |                        | id
| /v1/new/post       | POST   | Create a new post                        |                        |        |
| /v1/posts/:id   | PATCH    | Update an existing post                |                        | id |
| /v1/posts/:id   | DELETE | Delete a post by its ID                  |                        | id |
| /v1/post/:post_id/invite_user/:username| POST |Invite a user to view a post |                |post_id , username |
| /v1//posts/:invitation_id/accept| PUT |Accept invite to view post |                | invitation_id |
| /v1/post/:post_id/invite_user/:username| POST |Invite a user to view a post |                | post_id , username|
| /post/:post_id/revoke_user_invite/:username/| PUT |Revoke a user invite to a post |                | post_id ,username |
| /v1/users       | GET    | Get a paginated list of all users                  |   page , users           |
| /v1/users/login   | POST | Create a JWT token pair (Login)          |                         |
| /v1/users/register| POST   | Create a new user                      |                        |


The api documentation will be found at `http://127.0.0.1:5000/docs`

### Authentication

Some API endpoints will require you provide a JWT in the ```Authentication``` header using ```Bearer <JWT>```

