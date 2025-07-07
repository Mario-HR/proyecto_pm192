from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.connection import Session as SessionLocal
from models.db import Categories
from models.pydantic import Category

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

# Actualizar una categoría existente
@router.put("/{categoria_id}", response_model=Category)
def actualizar_categoria(categoria_id: int, categoria_actualizada: Category, db: Session = Depends(get_db)):
    categoria = db.query(Categories).get(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for campo, valor in categoria_actualizada.dict().items():
        setattr(categoria, campo, valor)

    db.commit()
    db.refresh(categoria)
    return categoria

# Eliminar una categoría
@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categories).get(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoría eliminada"}
