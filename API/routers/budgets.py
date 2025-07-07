from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from db.connection import Session
from models.db import Budgets
from models.pydantic import Budget

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("/add", response_model=Budget)
def create_budget(budget: Budget):
    db=Session()
    try:
        query = Budgets(**budget.model_dump())
        db.add(query)
        db.commit()
        return JSONResponse(status_code=200,content={"message": "Presupuesto guardado", "budget": budget.model_dump})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,content={"message": "Error al guardar el presupuesto", "Exception": str(e)})
    finally:
        db.close()

@router.get("/", response_model=List[Budget])
def get_budgets():
    db=Session()
    try:
        query = db.query(Budgets).all()
        if query:
            return JSONResponse(status_code=200, content=jsonable_encoder(query))
        else:
            return JSONResponse(status_code=404, content={"mensaje": "No se han encontrado presupuestos"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener los presupuestos", "Exception": str(e)})
    finally:
        db.close()

@router.get("/{budget_id}", response_model=Budget)
def get_budget(budget_id: int):
    db=Session()
    try:
        query = db.query(Budgets).get(budget_id)
        if query:
            return JSONResponse(status_code=200, content=jsonable_encoder(query))
        else:
            return JSONResponse(status_code=404, content="Presupuesto no encontrado")
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al obtener el presupuesto", "Exception": str(e)})
    finally:
        db.close()

@router.put("/{budget_id}", response_model=Budget)
def update_budget(budget_id: int, updated_data: Budget):
    db=Session()
    try:
        query = db.query(Budgets).get(budget_id)
        if not query:
            return JSONResponse(status_code=404, content="Presupuesto no encontrado")
        for field, value in updated_data.dict().items():
            setattr(query, field, value)
        db.commit()
        return JSONResponse(content={"message": "Presupesto actualizado", "presupuesto": updated_data.model_dump()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al modificar el presupuesto", "Exception": str(e)})
    finally:
        db.close()

@router.delete("/{budget_id}")
def delete_budget(budget_id: int):
    db=Session()
    try:
        query = db.query(Budgets).get(budget_id)
        if not query:
            return JSONResponse(status_code=404, content="Presupuesto no encontrada")
        db.delete(query)
        db.commit()
        return {"message": "Presupuesto eliminada correctamente"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar el presupuesto", "Exception": str(e)})
    finally:
        db.close()
