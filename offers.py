from flask import Flask, render_template, request, redirect, url_for
from models import db, Offer, Subscription

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/schoopledb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
db.init_app(app)

# Route: List Offers with Pagination
@app.route('/')
def list_offers():
    page = request.args.get('page', 1, type=int)  # Get current page number
    per_page = 5  # Number of items per page

    # Fetch offers with pagination
    pagination = Offer.query.paginate(page=page, per_page=per_page)
    return render_template('offers.html', offers=pagination.items, pagination=pagination)

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
        return redirect(url_for('list_offers'))

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
        return redirect(url_for('list_offers'))

    subscriptions = Subscription.query.all()  # Fetch all subscriptions for dropdown
    return render_template('offer_form.html', offer=offer, subscriptions=subscriptions)

# Route: Delete Offer
@app.route('/delete/<int:id>', methods=['POST'])
def delete_offer(id):
    offer = Offer.query.get_or_404(id)
    db.session.delete(offer)
    db.session.commit()
    return redirect(url_for('list_offers'))

if __name__ == '__main__':
    app.run(debug=True)
