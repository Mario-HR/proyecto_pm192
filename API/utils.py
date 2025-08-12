import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException
from db.connection import Session
from models.db import Users
from bcrypt import gensalt,hashpw,checkpw
from datetime import datetime, time
from decimal import Decimal

def cypherPassword(plain_password):
    # Convertir a bytes
    password_bytes = plain_password.encode('utf-8')

    # Generar salt y hash
    salt = gensalt()
    hashed = hashpw(password_bytes, salt)
    return hashed
#Recibe un password en texto plano y un hash, devuelve True si coinciden
def checkPassword(plain_password,hashed_password) -> bool:
    return checkpw(plain_password.encode('utf-8'),hashed_password)
# Crea un token JWT con los datos del usuario
def createToken(data:dict):
    token:str=jwt.encode(payload=data,key="secretkey",algorithm="HS256")
    return token
# Obtiene el ID del usuario a partir del token JWT
# Si el token es válido, devuelve el ID del usuario, si no, lanza una HTTPException
# Si el token ha expirado, lanza una HTTPException con status 403
def getIdFromToken(token:str):
    db=Session()
    try:
        data:dict=jwt.decode(token, key="secretkey",algorithms="HS256")
        email=data.get("email")
        phone=data.get("phone")
        if email:
            userQuery=db.query(Users).filter(Users.email==email).first()
        elif phone:
            userQuery=db.query(Users).filter(Users.phone==phone).first()
        return userQuery.id
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token invalido")
# Convierte tipos especiales de datos a formatos JSON serializables
# Esta función es útil para serializar objetos que no son directamente serializables por JSON
# como Decimal y datetime.
def convertSpecialTypes(obj):
    if isinstance(obj, dict):
        return {k: convertSpecialTypes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertSpecialTypes(i) for i in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, time):
        return obj.isoformat()
    else:
        return obj