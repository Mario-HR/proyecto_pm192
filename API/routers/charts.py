from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from db.connection import Session as SessionLocal
from models.db import Transactions, Categories
from decimal import Decimal
from utils import getIdFromToken

router = APIRouter(prefix="/api", tags=["Gráficas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función compartida para ingresos o gastos
def obtener_datos_grafica(tipo: str, db: Session, user_id: int):
    query = (
        db.query(
            func.strftime("%Y-%m", Transactions.datetime).label("mes"),
            Categories.name.label("categoria"),
            func.sum(Transactions.amount).label("total")
        )
        .join(Categories, Transactions.category == Categories.id)
    )
    # Condición según tipo

    if tipo == "ingreso":
        condicion_tipo = Transactions.amount > Decimal(0)
    else:
        condicion_tipo = Transactions.amount < Decimal(0)

    query = query.filter(
        and_(
            condicion_tipo,
            Transactions.user == user_id
        )
    )

    query = query.group_by(
        func.strftime("%Y-%m", Transactions.datetime),
        Categories.name
    ).order_by(
        func.strftime("%Y-%m", Transactions.datetime)
    )

    resultados = [
        {"mes": row.mes, "categoria": row.categoria, "total": float(abs(row.total))}
        for row in query.all()
    ]
    print(resultados)
    return resultados

@router.get("/graficaIngresos", response_model=List)
def grafica_ingresos(db: Session = Depends(get_db), user_id:int = Depends(getIdFromToken)):
    return obtener_datos_grafica("ingreso", db, user_id)

@router.get("/graficaGastos", response_model=List)
def grafica_gastos(db: Session = Depends(get_db), user_id:int = Depends(getIdFromToken)):
    return obtener_datos_grafica("gasto", db, user_id)
