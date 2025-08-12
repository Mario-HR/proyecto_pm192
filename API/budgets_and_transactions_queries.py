from db.connection import Session
from models.db import Budgets,Transactions,ScheduledTransactions
from sqlalchemy import func
from datetime import datetime, timedelta
# Queries para presupuestos y transacciones
def get_total_spent(user_id: int, year: int, month: int, category_id: int):
    db=Session()
    # Suma transacciones normales del mes
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    #Funciones para transacciones normales y programadas
    normal_sum = db.query(func.coalesce(func.sum(Transactions.amount), 0)).filter(
        Transactions.user == user_id,
        Transactions.category == category_id,
        Transactions.datetime >= start_date,
        Transactions.datetime < end_date,
    ).scalar()

    # Suma transacciones programadas ya ejecutadas en el mes
    scheduled_sum = db.query(func.coalesce(func.sum(ScheduledTransactions.amount), 0)).filter(
        ScheduledTransactions.user == user_id,
        ScheduledTransactions.category == category_id,
        # Aquí podrías agregar lógica para fechas ya ejecutadas si tienes registros de ejecución
    ).scalar()

    # Por simplicidad asumimos sólo transacciones normales ya hechas, ajustar según esquema
    return normal_sum + scheduled_sum

# Obtiene el presupuesto para un usuario, año, mes y categoría específicos
def get_budget(user_id: int, year: int, month: int, category_id: int):
    db=Session()
    budget = db.query(Budgets).filter_by(
        user=user_id, year=year, month=month, category=category_id
    ).first()
    return budget.amount if budget else 0

# Obtiene el total de transacciones programadas para un usuario en un rango de días
def get_scheduled_sum_for_next_days(user_id: int, days_ahead: int = 2):
    db=Session()
    today = datetime.utcnow().date()
    limit_date = today + timedelta(days=days_ahead)

    # Suma monto de transacciones programadas próximas (sin control de ejecución)
    # Aquí puedes afinar si tienes fecha de ejecución real
    scheduled_sum = db.query(func.coalesce(func.sum(ScheduledTransactions.amount), 0)).filter(
        ScheduledTransactions.user == user_id,
        ScheduledTransactions.day >= today.day,
        ScheduledTransactions.day <= limit_date.day,
    ).scalar()
    return scheduled_sum
