from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DeliveryRequest(db.Model):
    """
    Модель базы данных
    id- идентификатор заказа
    details- описание заказа
    status- статус заказа
    """
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)
