from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    amount_per_student = db.Column(db.String)
    min_student_count = db.Column(db.String)
    launch = db.Column(db.Date)
    expiry = db.Column(db.Date)  # Assuming expiry is stored as a date
    type = db.Column(db.String)
    status = db.Column(db.Boolean)

class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    offer_percentage = db.Column(db.String)
    discount_amount = db.Column(db.String)
    additional_amount = db.Column(db.String)
    launch = db.Column(db.Date)
    expiry = db.Column(db.Date)
    is_school_secific = db.Column(db.Boolean)
    status = db.Column(db.Boolean)

    subscription = db.relationship('Subscription', backref='offers', lazy=True)
