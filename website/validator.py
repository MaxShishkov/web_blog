import re

EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

class Validator():
    def validate_email(self, email: str) -> bool:
        return EMAIL_RE.fullmatch(email) is not None


