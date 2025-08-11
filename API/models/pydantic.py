from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime as Datetime
from datetime import time as Time
from decimal import Decimal

class User(BaseModel):
    name:str = Field(...,min_length=3,max_length=50,description="Solo letras: min 3 max 50", example="Juan")
    lastname:str = Field(...,min_length=3,max_length=50,description="Solo letras: min 3 max 50",example="Perez")
    email:Optional[EmailStr] = Field(..., description="Solo direcciones de correo electronico validas",example="correo@example.com")
    phone:Optional[str] = Field(...,min_length=10,max_length=10,description="Número telefónico válido a diez dígitos",example="4421234567")
    password:str = Field(...,description="Contraseña del usuario")

class Category(BaseModel):
    id: int | None = None
    name:str = Field(...,description="Nombre de la categoría")
    schedulable:bool = Field(...,description="Booleano")
    model_config = ConfigDict(from_attributes=True)

class Transaction(BaseModel):
    id: int | None = None
    amount:Decimal = Field(...,decimal_places=2,description="Monto de la transacción")
    datetime:Datetime = Field(...,default_factory=Datetime.now,description="Fecha y hora de la transacción")
    description:str = Field(...,description="Descripción de la transacción")
    category:int = Field(...,description="ID de la categoría")
    model_config = ConfigDict(from_attributes=True)

class ScheduledTransaction(BaseModel):
    id: int | None = None
    amount:Decimal = Field(...,decimal_places=2,description="Monto de la transacción")
    day:int = Field(...,description="Día de la transacción")
    time:Time = Field(...,description="Hora de la transacción")
    description:str = Field(...,description="Descripción de la transacción")
    category:int = Field(...,description="ID de la categoría")
    model_config = ConfigDict(from_attributes=True)

class Budget(BaseModel):
    id: int | None = None
    amount:Decimal = Field(...,decimal_places=2,description="Monto del presupuesto")
    description:str = Field(...,description="Descripción del presupuesto")
    year:int = Field(...,description="Año del presupuesto")
    month:int = Field(...,description="Mes del presupuesto")
    category:int = Field(...,description="ID de la categoría")
    model_config = ConfigDict(from_attributes=True)
    
class Login(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

class BudgetBase(BaseModel):
    amount: float
    month: int       # 1..12
    category: int    # id de categoría

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int