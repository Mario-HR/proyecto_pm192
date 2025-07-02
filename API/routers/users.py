from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.pydantic import User
from middleware import BearerJWT
from db.connection import Session
from models.db import Users
from fastapi import APIRouter
from passwords import cypherPassword,checkPassword

usersRouter = APIRouter()

# Endpoint de login
@usersRouter.post('/validateUser', tags=['Endpoint de login'])
def validateUser(user:User):
    db=Session()
    try:
        if user.email:
            userQuery=db.query(Users).filter(Users.email==user.email).first()
        elif user.phone:
            userQuery=db.query(Users).filter(Users.phone==user.email).first()
        if checkPassword(user.password,userQuery.password):
            return JSONResponse(status_code=200,content={"message": "Autenticación exitosa"})
        else:
            return JSONResponse(status_code=401,content={"message": "Correo o contraseña incorrectos"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al buscar usuario", "Exception": str(e)})
    finally:
        db.close()
        

# Endpoint de registro de usuario
@usersRouter.post('/registerUser', response_model=User, tags=['Endpoint de registro de usuario'])
def registerUser(user:User):
    db=Session()
    try:
        dbUser=Users(
            name=user.name,
            lastname=user.lastname,
            email=user.email,
            phone=user.phone,
            password=cypherPassword(user.password)
        )
        db.add(dbUser)
        db.commit()
        return JSONResponse(status_code=201,content={"mesage":"Usuario guardado","usuario": user.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,content={"message": "Error al guardar usuario", "Exception": str(e)})
    finally:
        db.close()