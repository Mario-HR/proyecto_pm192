from db.connection import Session
from models.db import Budgets, Users
from mail.sender import send_email
from budgets_and_transactions_queries import get_scheduled_sum_for_next_days, get_total_spent
from datetime import datetime

async def check_budgets_and_notify():
    db = Session()
    users = db.query(Users).all()
    today = datetime.utcnow()
    year = today.year
    month = today.month

    for user in users:
        # Obtener presupuestos para ese usuario
        budgets = db.query(Budgets).filter_by(user=user.id, year=year, month=month).all()
        for budget in budgets:
            spent = get_total_spent(db, user.id, year, month, budget.category)
            if spent > budget.amount:
                # Superó presupuesto, enviar mail
                await send_email(
                    user.email,
                    "Alerta: Presupuesto superado",
                    f"Has superado el presupuesto de {budget.description} para {month}/{year}."
                )
            else:
                # Revisar pagos programados próximos
                scheduled_sum = get_scheduled_sum_for_next_days(db, user.id, days_ahead=2)
                available_budget = budget.amount - spent
                if available_budget < scheduled_sum:
                    await send_email(
                        user.email,
                        "Alerta: Presupuesto insuficiente para pagos próximos",
                        f"Tienes pagos programados próximos que superan el presupuesto disponible en {budget.description}."
                    )
    db.close()
