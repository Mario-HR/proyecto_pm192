from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime

from db.connection import Session
from models.db import Budgets
from models.pydantic import Budget, BudgetCreate
from utils import getIdFromToken

router = APIRouter(prefix="/budgets", tags=["Budgets"])

# ---------- CREATE ----------
@router.post("/", response_model=Budget)
def create_budget(budget: BudgetCreate, user_id: int = Depends(getIdFromToken)):
    db = Session()
    try:
        # Defaults para columnas NOT NULL que no mandas desde el cliente
        row = Budgets(
            user=user_id,
            amount=float(budget.amount),
            month=int(budget.month),          # 1..12
            category=int(budget.category),    # id de categoría
            description="",                   # <- evita NOT NULL
            year=datetime.utcnow().year       # <- evita NOT NULL (si no usas año, guarda el actual)
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row
    finally:
        db.close()

# ---------- LIST ----------
@router.get("/", response_model=List[Budget])
def get_budgets(user_id: int = Depends(getIdFromToken)):
    db = Session()
    try:
        rows = db.query(Budgets).filter(Budgets.user == user_id).all()
        return rows or []   # siempre 200
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener los presupuestos", "Exception": str(e)})
    finally:
        db.close()

# ---------- GET BY ID ----------
@router.get("/{budget_id}", response_model=Budget)
def get_budget(budget_id: int):
    db = Session()
    try:
        row = db.query(Budgets).get(budget_id)
        if row:
            return row
        return JSONResponse(status_code=404, content="Presupuesto no encontrado")
    finally:
        db.close()

# ---------- UPDATE ----------
@router.put("/{budget_id}", response_model=Budget)
def update_budget(budget_id: int, updated: BudgetCreate):
    db = Session()
    try:
        row = db.query(Budgets).get(budget_id)
        if not row:
            return JSONResponse(status_code=404, content="Presupuesto no encontrado")

        data = updated.model_dump()
        # Sólo actualizamos los 3 campos que editas desde la app
        if "amount" in data and data["amount"] is not None:
            row.amount = float(data["amount"])
        if "month" in data and data["month"] is not None:
            row.month = int(data["month"])
        if "category" in data and data["category"] is not None:
            row.category = int(data["category"])

        db.commit()
        db.refresh(row)
        return row
    finally:
        db.close()

# ---------- DELETE ----------
@router.delete("/{budget_id}")
def delete_budget(budget_id: int):
    db = Session()
    try:
        row = db.query(Budgets).get(budget_id)
        if not row:
            return JSONResponse(status_code=404, content="Presupuesto no encontrada")
        db.delete(row)
        db.commit()
        return {"message": "Presupuesto eliminada correctamente"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar el presupuesto", "Exception": str(e)})
    finally:
        db.close()
