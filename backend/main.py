from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, static_folder='../frontend/dist')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    sku = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(255), nullable=True)  # Путь к изображению


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), nullable=False)
    cardholder_name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.String(5), nullable=False)  # Формат MM/YY
    cvv = db.Column(db.String(3), nullable=False)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class PaymentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey(
        'payment.id'), nullable=False)


def format_data(model, query_result, exclude_columns=[]):
    headers = [
        column.name for column in model.__table__.columns if column.name not in exclude_columns]
    rows = [[getattr(item, column) for column in headers]
            for item in query_result]
    return {"head": headers, "rows": rows}


# with app.app_context():
#     db.create_all()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    print(os.listdir(app.static_folder))
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        user_data = request.json
        new_user = User(name=user_data['name'], email=user_data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201
    users = User.query.all()
    response_data = format_data(User, users)
    return jsonify(response_data)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        product_data = request.json
        new_product = Product(
            name=product_data['name'],
            description=product_data.get('description'),
            price=product_data['price'],
            quantity=product_data['quantity'],
            category=product_data.get('category'),
            sku=product_data.get('sku'),
            image=product_data.get('image')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'id': new_product.id, 'name': new_product.name, 'price': new_product.price}), 201
    products = Product.query.all()
    return jsonify(format_data(Product, products))


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200


@app.route('/cards', methods=['GET', 'POST'])
def manage_cards():
    if request.method == 'POST':
        card_data = request.json
        new_card = Card(
            card_number=card_data['card_number'],
            cardholder_name=card_data['cardholder_name'],
            expiration_date=card_data['expiration_date'],
            cvv=card_data['cvv']
        )
        db.session.add(new_card)
        db.session.commit()
        return jsonify({'id': new_card.id, 'card_number': new_card.card_number}), 201
    cards = Card.query.all()
    return jsonify(format_data(Card, cards))


@app.route('/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    db.session.delete(card)
    db.session.commit()
    return jsonify({'message': 'Card deleted successfully'}), 200


@app.route('/payments', methods=['GET', 'POST'])
def manage_payments():
    if request.method == 'POST':
        payment_data = request.json
        new_payment = Payment(
            amount=payment_data['amount'],
            payment_method=payment_data['payment_method'],
            transaction_id=payment_data['transaction_id'],
            user_id=payment_data['user_id']
        )
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({'id': new_payment.id, 'amount': new_payment.amount, 'payment_method': new_payment.payment_method, 'transaction_id': new_payment.transaction_id, 'user_id': new_payment.user_id}), 201
    payments = Payment.query.all()
    return jsonify(format_data(Payment, payments))


@app.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully'}), 200


@app.route('/payment_history', methods=['GET'])
def get_payment_history():
    history = PaymentHistory.query.all()
    return jsonify(format_data(PaymentHistory, history))


if __name__ == '__main__':
    app.run(debug=True)
