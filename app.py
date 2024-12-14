from flask import Flask, request, jsonify

from models import db, DeliveryRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///delivery_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/delivery', methods=['POST'])
def create_delivery():
    """Создание заявки и запись в БД"""
    data = request.json
    new_request = DeliveryRequest(status='Создан', details=data['details'])
    db.session.add(new_request)
    db.session.commit()
    return jsonify({'id': new_request.id, 'status': new_request.status}), 201


@app.route('/delivery/<int:order_id>', methods=['GET'])
def get_request(order_id):
    """Просмотр информации о заявке"""
    delivery_request = DeliveryRequest.query.get_or_404(order_id)
    return jsonify({'id': delivery_request.id, 'status': delivery_request.status, 'details': delivery_request.details}), 200


@app.route('/delivery/<int:order_id>', methods=['DELETE'])
def delete_delivery(order_id):
    """Удаление заявки из БД"""
    delivery = DeliveryRequest.query.get_or_404(order_id)
    if delivery.status != 'Создан':
        return jsonify({"error": f"Невозможно удалить заявку, {delivery.status}"}), 400
    db.session.delete(delivery)
    db.session.commit()
    return jsonify({"message": "Заявка успешно удалена."}), 200


@app.route('/delivery/<int:order_id>/status', methods=['PUT'])
def update_status(order_id):
    """Обновление статуса заявки в БД"""
    delivery_request = DeliveryRequest.query.get_or_404(order_id)
    new_status = request.json.get('status')
    if new_status in ('товар передан в доставку', 'товар доставлен'):
        delivery_request.status = new_status
        db.session.commit()
        return jsonify({'id': delivery_request.id, 'status': delivery_request.status}), 201
    return jsonify({"error": "Неверный статус."}), 400


if __name__ == '__main__':
    app.run(port=5000)
