from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from db.connection import Session as SessionLocal
from models.db import Transactions, Categories
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Gráficas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función compartida para ingresos o gastos
def obtener_datos_grafica(tipo: str, db: Session):
    query = (
        db.query(
            func.strftime("%Y-%m", Transactions.datetime).label("mes"),
            Categories.name.label("categoria"),
            func.sum(Transactions.amount).label("total")
        )
        .join(Categories, Transactions.category == Categories.id)
        .filter(Transactions.amount > 0 if tipo == "ingreso" else Transactions.amount < 0)
        .group_by("mes", "categoria")
        .order_by("mes")
    )
    return [
        {"mes": row.mes, "categoria": row.categoria, "total": float(abs(row.total))}
        for row in query.all()
    ]

@router.get("/graficaIngresos")
def grafica_ingresos(db: Session = Depends(get_db)):
    return obtener_datos_grafica("ingreso", db)

@router.get("/graficaGastos")
def grafica_gastos(db: Session = Depends(get_db)):
    return obtener_datos_grafica("gasto", db)
