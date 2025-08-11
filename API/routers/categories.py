from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from db.connection import Session as SessionLocal
from models.db import Categories
from models.pydantic import Category
from utils import getIdFromToken

router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todas las categorías
@router.get("/", response_model=List[Category])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categories).all()

# Obtener una categoría por ID
@router.get("/{categoria_id}", response_model=Category)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categories).get(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# Crear una nueva categoría
@router.post("/", response_model=Category)
def crear_categoria(nueva_categoria: Category, db: Session = Depends(get_db)):
    categoria = Categories(**nueva_categoria.dict())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    schedulable: Optional[bool] = None

@router.put("/{category_id}")
def actualizar_categoria(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(getIdFromToken),
):
    cat = db.query(Categories).filter(Categories.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    data = payload.model_dump(exclude_unset=True)
    # 🔒 Nunca tocar la PK
    data.pop("id", None)

    for field, value in data.items():
        setattr(cat, field, value)

    db.commit()
    db.refresh(cat)

    # responde con lo que necesites
    return {
        "id": cat.id,
        "name": cat.name,
        "schedulable": bool(cat.schedulable),
    }

# Eliminar una categoría
@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categories).get(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoría eliminada"}
