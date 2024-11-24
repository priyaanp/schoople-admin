from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Offer,Subscription

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/schoopledb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
db.init_app(app)
'''
@app.route('/')
def list_subscriptions():
    
    prime_active_subscriptions = Subscription.query.filter(
    Subscription.type == 'Prime',
    Subscription.status == True
    ).all()
    

    subscriptions = Subscription.query.all()  # Fetch all subscriptions
    return render_template('subscriptions.html', subscriptions=subscriptions)
    '''
@app.route('/subscription/list')
def subscriptions():
    return render_template('subscriptions_datatable.html')
    
@app.route('/api/subscriptions', methods=['GET'])
def api_subscriptions():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)
    order_column_index = request.args.get('order[0][column]', type=int)
    order_column_name = request.args.get(f'columns[{order_column_index}][data]', default='id')
    order_dir = request.args.get('order[0][dir]', default='asc')

    # Validate the column name
    valid_columns = ['id', 'title', 'description', 'amount_per_student', 'min_student_count', 'launch', 'expiry', 'type', 'status']
    if order_column_name not in valid_columns:
        order_column_name = 'id'  # Default to 'id' if invalid

    # Query total records
    total_records = Subscription.query.count()

    # Filter based on search
    query = Subscription.query
    if search_value:
        query = query.filter(
            Subscription.title.ilike(f'%{search_value}%') |
            Subscription.description.ilike(f'%{search_value}%') |
            Subscription.type.ilike(f'%{search_value}%')
        )

    # Query filtered records count
    filtered_records = query.count()

    # Sorting
    if order_dir == 'asc':
        query = query.order_by(getattr(Subscription, order_column_name).asc())
    else:
        query = query.order_by(getattr(Subscription, order_column_name).desc())

    # Pagination
    subscriptions = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": sub.id,
            "title": sub.title,
            "description": sub.description,
            "amount_per_student": sub.amount_per_student,
            "min_student_count": sub.min_student_count,
            "launch": sub.launch.strftime('%Y-%m-%d') if sub.launch else '',
            "expiry": sub.expiry.strftime('%Y-%m-%d') if sub.expiry else '',
            "type": sub.type,
            "status": "Active" if sub.status else "Inactive"
        }
        for sub in subscriptions
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })


@app.route('/subscription/list/old')
def list_subscriptions():
    # Get the page number from the query parameter, default is page 1
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of items per page

    # Query the subscriptions with pagination
    pagination = Subscription.query.paginate(page=page, per_page=per_page)

    return render_template('subscriptions.html', subscriptions=pagination.items, pagination=pagination)
    
@app.route('/subscription/add', methods=['GET', 'POST'])
def add_subscription():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form['title']
        description = request.form['description']
        amount_per_student = request.form['amount_per_student']
        min_student_count = request.form['min_student_count']
        launch = request.form['launch']
        expiry = request.form['expiry']
        sub_type = request.form['type']
        status = request.form.get('status') == 'on'

        # Add subscription to database
        new_subscription = Subscription(
            title=title,
            description=description,
            amount_per_student=amount_per_student,
            min_student_count=min_student_count,
            launch=launch,
            expiry=expiry,
            type=sub_type,
            status=status
        )
        db.session.add(new_subscription)
        db.session.commit()
        return redirect(url_for('subscriptions'))

    return render_template('subscription_form.html', subscription=None)

@app.route('/subscription/edit/<int:id>', methods=['GET', 'POST'])
def edit_subscription(id):
    subscription = Subscription.query.get_or_404(id)

    if request.method == 'POST':
        subscription.title = request.form['title']
        subscription.description = request.form['description']
        subscription.amount_per_student = request.form['amount_per_student']
        subscription.min_student_count = request.form['min_student_count']
        subscription.launch = request.form['launch']
        subscription.expiry = request.form['expiry']
        subscription.type = request.form['type']
        subscription.status = request.form.get('status') == 'on'

        db.session.commit()
        return redirect(url_for('subscriptions'))

    return render_template('subscription_form.html', subscription=subscription)

@app.route('/subscription/delete/<int:id>', methods=['POST'])
def delete_subscription(id):
    subscription = Subscription.query.get_or_404(id)
    db.session.delete(subscription)
    db.session.commit()
    return redirect(url_for('list_subscriptions'))

@app.route('/offerlist')
def offers():
    return render_template('offers_datatable.html')

@app.route('/api/offers', methods=['GET'])
def api_offers():
    # Get DataTables parameters from the request
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)
    order_column_index = request.args.get('order[0][column]', type=int)
    order_column_name = request.args.get(f'columns[{order_column_index}][data]', default='id')
    order_dir = request.args.get('order[0][dir]', default='asc')

    # Query the total number of rows
    total_records = Offer.query.count()

    # Filter based on search
    query = Offer.query
    if search_value:
        query = query.filter(
            Offer.title.ilike(f'%{search_value}%') |
            Offer.offer_percentage.ilike(f'%{search_value}%') |
            Offer.discount_amount.ilike(f'%{search_value}%')
        )

    # Query total number of filtered records
    filtered_records = query.count()

    # Sorting
    if order_dir == 'asc':
        query = query.order_by(getattr(Offer, order_column_name).asc())
    else:
        query = query.order_by(getattr(Offer, order_column_name).desc())

    # Pagination
    offers = query.offset(start).limit(length).all()

    # Format the data for DataTables
    data = [
        {
            "id": offer.id,
            "title": offer.title,
            "subscription_id": offer.subscription_id,
            "offer_percentage": offer.offer_percentage,
            "discount_amount": offer.discount_amount,
            "additional_amount": offer.additional_amount,
            "launch": offer.launch.strftime('%Y-%m-%d') if offer.launch else '',
            "expiry": offer.expiry.strftime('%Y-%m-%d') if offer.expiry else '',
            "status": "Active" if offer.status else "Inactive"
        }
        for offer in offers
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })


# Route: Add New Offer
@app.route('/add', methods=['GET', 'POST'])
def add_offer():
    if request.method == 'POST':
        # Fetch form data
        subscription_id = request.form['subscription_id']
        title = request.form['title']
        offer_percentage = request.form['offer_percentage']
        discount_amount = request.form['discount_amount']
        additional_amount = request.form['additional_amount']
        launch = request.form['launch']
        expiry = request.form['expiry']
        is_school_specific = request.form.get('is_school_specific') == 'on'
        status = request.form.get('status') == 'on'

        # Add new offer to the database
        new_offer = Offer(
            subscription_id=subscription_id,
            title=title,
            offer_percentage=offer_percentage,
            discount_amount=discount_amount,
            additional_amount=additional_amount,
            launch=launch,
            expiry=expiry,
            is_school_secific=is_school_specific,
            status=status
        )
        db.session.add(new_offer)
        db.session.commit()
        return redirect(url_for('offers'))

    subscriptions = Subscription.query.all()  # Fetch all subscriptions for dropdown
    return render_template('offer_form.html', offer=None, subscriptions=subscriptions)

# Route: Edit Offer
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_offer(id):
    offer = Offer.query.get_or_404(id)

    if request.method == 'POST':
        # Update offer details
        offer.subscription_id = request.form['subscription_id']
        offer.title = request.form['title']
        offer.offer_percentage = request.form['offer_percentage']
        offer.discount_amount = request.form['discount_amount']
        offer.additional_amount = request.form['additional_amount']
        offer.launch = request.form['launch']
        offer.expiry = request.form['expiry']
        offer.is_school_secific = request.form.get('is_school_specific') == 'on'
        offer.status = request.form.get('status') == 'on'

        db.session.commit()
        return redirect(url_for('offers'))

    subscriptions = Subscription.query.all()  # Fetch all subscriptions for dropdown
    return render_template('offer_form.html', offer=offer, subscriptions=subscriptions)

# Route: Delete Offer
@app.route('/delete/<int:id>', methods=['POST'])
def delete_offer(id):
    offer = Offer.query.get_or_404(id)
    db.session.delete(offer)
    db.session.commit()
    return redirect(url_for('offers'))
if __name__ == '__main__':
    app.run(debug=True)
