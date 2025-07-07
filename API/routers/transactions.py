from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import Session as SessionLocal
from models.db import Transactions
from models.pydantic import Transaction
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Transaction)
def create_transaction(transaction: Transaction, db: Session = Depends(get_db)):
    db_transaction = Transactions(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transactions).all()

@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transactions).get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, updated_data: Transaction, db: Session = Depends(get_db)):
    transaction = db.query(Transactions).get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    for field, value in updated_data.dict().items():
        setattr(transaction, field, value)

    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transactions).get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    db.delete(transaction)
    db.commit()
    return {"message": "Transacción eliminada correctamente"}
