from fastapi import FastAPI
from db.connection import engine,Base

from fastapi.middleware.cors import CORSMiddleware
from routers.users import usersRouter
from routers.transactions import router as transactionsRouter
from routers.scheduled_transactions import router as scheduledTransactionsRouter
from routers.categories import router as categoriesRouter
from routers.charts import router as chartsRouter

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
app.include_router(transactionsRouter)
app.include_router(scheduledTransactionsRouter)
app.include_router(categoriesRouter)
app.include_router(chartsRouter)