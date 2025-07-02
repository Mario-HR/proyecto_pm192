from fastapi import FastAPI
from db.connection import engine,Base

from fastapi.middleware.cors import CORSMiddleware
from routers.users import usersRouter

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='Lana APP API',
    version='1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
Base.metadata.create_all(bind=engine)

app.include_router(usersRouter)