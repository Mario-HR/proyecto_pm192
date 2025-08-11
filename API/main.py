from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.connection import engine,Base
from fastapi.middleware.cors import CORSMiddleware
from routers.users import usersRouter
from routers.transactions import router as transactionsRouter
from routers.scheduled_transactions import router as scheduledTransactionsRouter
from routers.categories import router as categoriesRouter
from routers.charts import router as chartsRouter
from routers.budgets import router as budgetsRouter
from budgets_checker import check_budgets_and_notify

#Personalizacuón del encabezado de la documentación
app=FastAPI(
    title='Lana APP API',
    version='1.0'
)

scheduler = AsyncIOScheduler()

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
app.include_router(budgetsRouter)

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(check_budgets_and_notify, "interval", hours=24)
    scheduler.start()