from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.connection import Session as SessionLocal
from models.db import ScheduledTransactions
from models.pydantic import ScheduledTransaction
from utils import getIdFromToken

router = APIRouter(prefix="/scheduled-transactions", tags=["Scheduled Transactions"])

# Obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Obtener todos los pagos fijos
@router.get("/", response_model=List[ScheduledTransaction])
def obtener_pagos_fijos(db: Session = Depends(get_db), user_id:int = Depends(getIdFromToken)):
    return db.query(ScheduledTransactions).filter(ScheduledTransactions.user==user_id).all()

# 2. Registrar un nuevo pago fijo
@router.post("/", response_model=ScheduledTransaction)
def registrar_pago_fijo(pago: ScheduledTransaction, db: Session = Depends(get_db), user_id:int = Depends(getIdFromToken)):
    nuevo_pago = ScheduledTransactions(**pago.dict(), user=user_id)
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

# 3. Obtener un pago fijo por ID
@router.get("/{pago_fijo_id}", response_model=ScheduledTransaction)
def obtener_pago_fijo(pago_fijo_id: int, db: Session = Depends(get_db)):
    pago = db.query(ScheduledTransactions).get(pago_fijo_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago fijo no encontrado")
    return pago

# 4. Editar un pago fijo existente
@router.put("/{pago_fijo_id}", response_model=ScheduledTransaction)
def editar_pago_fijo(pago_fijo_id: int, pago_actualizado: ScheduledTransaction, db: Session = Depends(get_db)):
    pago = db.query(ScheduledTransactions).get(pago_fijo_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago fijo no encontrado")

    for campo, valor in pago_actualizado.dict().items():
        setattr(pago, campo, valor)

    db.commit()
    db.refresh(pago)
    return pago

# 5. Eliminar un pago fijo
@router.delete("/{pago_fijo_id}")
def eliminar_pago_fijo(pago_fijo_id: int, db: Session = Depends(get_db)):
    pago = db.query(ScheduledTransactions).get(pago_fijo_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago fijo no encontrado")
    db.delete(pago)
    db.commit()
    return {"mensaje": "Pago fijo eliminado"}
