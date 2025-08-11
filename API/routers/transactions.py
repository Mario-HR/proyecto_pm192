from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import Session as SessionLocal
from models.db import Transactions
from models.pydantic import Transaction
from typing import List
from utils import getIdFromToken
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime as Datetime

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Transaction)
def create_transaction(transaction: Transaction, db: Session = Depends(get_db), user_id:int = Depends(getIdFromToken)):
    db_transaction = Transactions(**transaction.dict(), user=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[Transaction])
def get_transactions(db: Session = Depends(get_db), user_id:int = Depends(getIdFromToken)):
    return db.query(Transactions).filter(Transactions.user==user_id).all()

@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transactions).get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    datetime: Optional[Datetime] = None
    description: Optional[str] = None
    category: Optional[int] = None
    
@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    updated_data: TransactionUpdate,        # ← usa el esquema opcional
    db: Session = Depends(get_db),
):
    transaction = db.query(Transactions).get(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Solo campos enviados; jamás tocar id ni user
    data = updated_data.model_dump(exclude_unset=True)
    data.pop("id", None)
    data.pop("user", None)

    for field, value in data.items():
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
