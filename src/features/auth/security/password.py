import bcrypt


def hash_password(password: str) -> str:
    encoded_pwd = password.encode("utf-8")
    return bcrypt.hashpw(encoded_pwd, bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
