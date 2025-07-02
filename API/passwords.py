from bcrypt import gensalt,hashpw,checkpw

def cypherPassword(plain_password):
    # Convertir a bytes
    password_bytes = plain_password.encode('utf-8')

    # Generar salt y hash
    salt = gensalt()
    hashed = hashpw(password_bytes, salt)
    return hashed

def checkPassword(plain_password,hashed_password) -> bool:
    return checkpw(plain_password.encode('utf-8'),hashed_password)