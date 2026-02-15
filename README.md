# Description

A blog application in python using flask.
You can create and delete posts. You can like the posts and leave comments.
You will need to create an account in order to see or create post.
There is no email verification, but the email has to be in a proper email format.
The website uses argon2 for password hashing. All data is made persistent using SQLAlchemy.


# Build

### Install UV

Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Check the command for your system at https://docs.astral.sh/uv/getting-started/installation/

## Sync

```
uv sync
```

Create .env file inside website folder and provide `SECRET_KEY` variable.

## Run

```
uv run app.py
```
