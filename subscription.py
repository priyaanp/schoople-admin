from flask import Flask, render_template, request, redirect, url_for, jsonify,session
from flask import session as flask_session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import text 
from models import Club, db, Offer,Subscription,Role,User,UserRole,Permission,School,AcademicYear,SchoolSubscription,Module,SchoolSubscriptionModuleRolePermission,StaffType,Staff

from config import DevelopmentConfig, TestingConfig, ProductionConfig

app = Flask(__name__)

# Choose the configuration based on an environment variable or hardcoded value
env = 'development'  # Change to 'testing' or 'production' as needed

if env == 'development':
    app.config.from_object(DevelopmentConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)
elif env == 'production':
    app.config.from_object(ProductionConfig)

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
    
    
    
    
ROLE_TYPES = ['admin', 'staff', 'student','superadmin']


@app.route('/roles/list')
def roles():
    return render_template('roles_datatable.html')


@app.route('/api/roles', methods=['GET'])
def api_roles():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)
    order_column_index = request.args.get('order[0][column]', type=int)
    order_column_name = request.args.get(f'columns[{order_column_index}][data]', default='id')
    order_dir = request.args.get('order[0][dir]', default='asc')

    # Validate the column name
    valid_columns = ['id', 'role_name', 'role_type', 'is_active']
    if order_column_name not in valid_columns:
        order_column_name = 'id'

    # Query total records
    total_records = Role.query.count()

    # Search functionality
    query = Role.query
    if search_value:
        query = query.filter(
            Role.role_name.ilike(f'%{search_value}%') |
            Role.role_type.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Sorting
    if order_dir == 'asc':
        query = query.order_by(getattr(Role, order_column_name).asc())
    else:
        query = query.order_by(getattr(Role, order_column_name).desc())

    # Pagination
    roles = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": role.id,
            "role_name": role.role_name,
            "role_type": role.role_type,
            "is_active": "Active" if role.is_active else "Inactive"
        }
        for role in roles
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })


@app.route('/roles/add', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        role_name = request.form['role_name']
        role_type = request.form['role_type']
        is_active = request.form.get('is_active') == 'on'

        new_role = Role(role_name=role_name, role_type=role_type, is_active=is_active)
        db.session.add(new_role)
        db.session.commit()
        return redirect(url_for('roles'))

    return render_template('role_form.html', role=None, role_types=ROLE_TYPES)


@app.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
def edit_role(id):
    role = Role.query.get_or_404(id)

    if request.method == 'POST':
        role.role_name = request.form['role_name']
        role.role_type = request.form['role_type']
        role.is_active = request.form.get('is_active') == 'on'

        db.session.commit()
        return redirect(url_for('roles'))

    return render_template('role_form.html', role=role, role_types=ROLE_TYPES)


@app.route('/roles/delete/<int:id>', methods=['POST'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({"success": True, "message": "Role deleted successfully!"})
    
@app.route('/users/list')
def users():
    return render_template('users_datatable.html')


@app.route('/api/users', methods=['GET'])
def api_users():
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    # Query total records
    total_records = User.query.count()

    # Search functionality
    query = User.query
    if search_value:
        query = query.filter(
            User.username.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Pagination
    users = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": user.id,
            "username": user.username,
            "roles": ", ".join([role.role_name for role in user.roles]),
            "is_active": "Active" if user.is_active else "Inactive"
        }
        for user in users
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })    
@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_active = request.form.get('is_active') == 'on'
        role_ids = request.form.getlist('roles')

        # Create a new user
        new_user = User(username=username, password=password, is_active=is_active)
        db.session.add(new_user)
        db.session.commit()

        # Assign roles
        for role_id in role_ids:
            user_role = UserRole(user_id=new_user.id, role_id=role_id)
            db.session.add(user_role)
        db.session.commit()

        return redirect(url_for('users'))

    roles = Role.query.all()
    return render_template('user_form.html', user=None, roles=roles)
@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.is_active = request.form.get('is_active') == 'on'
        role_ids = request.form.getlist('roles')

        # Clear existing roles
        UserRole.query.filter_by(user_id=user.id).delete()

        # Assign new roles
        for role_id in role_ids:
            user_role = UserRole(user_id=user.id, role_id=role_id)
            db.session.add(user_role)
        db.session.commit()

        return redirect(url_for('users'))

    roles = Role.query.all()
    assigned_roles = [role.id for role in user.roles]
    return render_template('user_form.html', user=user, roles=roles, assigned_roles=assigned_roles)
@app.route('/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    UserRole.query.filter_by(user_id=user.id).delete()  # Remove user roles
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "message": "User deleted successfully!"})

@app.route('/permissions/list')
def permission():
    return render_template('permissions_datatable.html')


@app.route('/api/permissions', methods=['GET'])
def api_permissions():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    # Query total records
    total_records = Permission.query.count()

    # Search functionality
    query = Permission.query
    if search_value:
        query = query.filter(
            Permission.permission_name.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Pagination
    permissions = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": permission.id,
            "permission_name": permission.permission_name,
            "is_active": "Active" if permission.is_active else "Inactive"
        }
        for permission in permissions
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })

@app.route('/permissions/add', methods=['GET', 'POST'])
def add_permission():
    if request.method == 'POST':
        permission_name = request.form['permission_name']
        is_active = request.form.get('is_active') == 'on'

        # Create a new permission
        new_permission = Permission(permission_name=permission_name, is_active=is_active)
        db.session.add(new_permission)
        db.session.commit()

        return redirect(url_for('permission'))

    return render_template('permission_form.html', permission=None)
@app.route('/permissions/edit/<int:id>', methods=['GET', 'POST'])
def edit_permission(id):
    permission = Permission.query.get_or_404(id)

    if request.method == 'POST':
        permission.permission_name = request.form['permission_name']
        permission.is_active = request.form.get('is_active') == 'on'

        db.session.commit()
        return redirect(url_for('permission'))

    return render_template('permission_form.html', permission=permission)
@app.route('/permissions/delete/<int:id>', methods=['POST'])
def delete_permission(id):
    permission = Permission.query.get_or_404(id)
    db.session.delete(permission)
    db.session.commit()
    return jsonify({"success": True, "message": "Permission deleted successfully!"})

@app.route('/schools/list')
def schools():
    return render_template('schools_datatable.html')


@app.route('/api/schools', methods=['GET'])
def api_schools():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    # Query total records
    total_records = School.query.count()

    # Search functionality
    query = School.query
    if search_value:
        query = query.filter(
            School.code.ilike(f'%{search_value}%') |
            School.title.ilike(f'%{search_value}%') |
            School.syllabus.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Pagination
    schools = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": school.id,
            "code": school.code,
            "title": school.title,
            "syllabus": school.syllabus,
            "status": "Active" if school.status else "Inactive"
        }
        for school in schools
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })
@app.route('/schools/add', methods=['GET', 'POST'])
def add_school():
    if request.method == 'POST':
        code = request.form['code']
        title = request.form['title']
        description = request.form['description']
        address = request.form['address']
        phone = request.form['phone']
        syllabus = request.form['syllabus']
        status = request.form.get('status') == 'on'

        # Create a new school
        new_school = School(
            code=code,
            title=title,
            description=description,
            address=address,
            phone=phone,
            syllabus=syllabus,
            status=status
        )
        db.session.add(new_school)
        db.session.commit()

        return redirect(url_for('schools'))

    return render_template('school_form.html', school=None)
@app.route('/edit/schools/<int:id>', methods=['GET', 'POST'])
def edit_school(id):
    school = School.query.get_or_404(id)

    if request.method == 'POST':
        school.code = request.form['code']
        school.title = request.form['title']
        school.description = request.form['description']
        school.address = request.form['address']
        school.phone = request.form['phone']
        school.syllabus = request.form['syllabus']
        school.status = request.form.get('status') == 'on'

        db.session.commit()
        return redirect(url_for('schools'))

    return render_template('school_form.html', school=school)
@app.route('/delete/schools/<int:id>', methods=['POST'])
def delete_school(id):
    school = School.query.get_or_404(id)
    db.session.delete(school)
    db.session.commit()
    return jsonify({"success": True, "message": "School deleted successfully!"})

@app.route('/academic_years/list')
def academicYear():
    return render_template('academic_years_datatable.html')


@app.route('/api/academic_years', methods=['GET'])
def api_academic_years():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    # Query total records
    total_records = AcademicYear.query.count()

    # Search functionality
    query = AcademicYear.query
    if search_value:
        query = query.filter(
            AcademicYear.start_date.ilike(f'%{search_value}%') |
            AcademicYear.end_date.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Pagination
    academic_years = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": year.id,
            "start_date": year.start_date.strftime('%Y-%m-%d'),
            "end_date": year.end_date.strftime('%Y-%m-%d'),
            "active": "Active" if year.active else "Inactive"
        }
        for year in academic_years
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })

@app.route('/academic_years/add', methods=['GET', 'POST'])
def add_academic_year():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        active = request.form.get('active') == 'on'

        # Create a new academic year
        new_year = AcademicYear(
            start_date=start_date,
            end_date=end_date,
            active=active
        )
        db.session.add(new_year)
        db.session.commit()

        return redirect(url_for('academicYear'))

    return render_template('academic_year_form.html', year=None)

@app.route('/academic_years/edit/<int:id>', methods=['GET', 'POST'])
def edit_academic_year(id):
    year = AcademicYear.query.get_or_404(id)

    if request.method == 'POST':
        year.start_date = request.form['start_date']
        year.end_date = request.form['end_date']
        year.active = request.form.get('active') == 'on'

        db.session.commit()
        return redirect(url_for('academicYear'))

    return render_template('academic_year_form.html', year=year)

@app.route('/academic_years/delete/<int:id>', methods=['POST'])
def delete_academic_year(id):
    year = AcademicYear.query.get_or_404(id)
    db.session.delete(year)
    db.session.commit()
    return jsonify({"success": True, "message": "Academic year deleted successfully!"})


@app.route('/school_subscriptions/list')
def schoolSubscriptions():
    return render_template('school_subscription_datatable.html')


@app.route('/api/school_subscriptions', methods=['GET'])
def api_school_subscriptions():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    # Query total records
    total_records = SchoolSubscription.query.count()

    # Search functionality
    query = SchoolSubscription.query.outerjoin(School).outerjoin(Subscription).outerjoin(Offer).outerjoin(AcademicYear)
    if search_value:
        query = query.filter(
            School.title.ilike(f'%{search_value}%') |
            Subscription.title.ilike(f'%{search_value}%') |
            Offer.title.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Pagination
    school_subscriptions = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": sub.id,
            "school": sub.school.title,
            "subscription": sub.subscription.title,
            "offer": sub.offer.title if sub.offer else "N/A",
            "academic_year": f"{sub.academic_year.start_date} - {sub.academic_year.end_date}",
            "subscription_amount": sub.subscription_amount,
            "status": "Active" if sub.status else "Inactive"
        }
        for sub in school_subscriptions
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })

@app.route('/school_subscriptions/add', methods=['GET', 'POST'])
def add_school_subscription():
    if request.method == 'POST':
        title = request.form['title']
        school_id = request.form['school_id']
        subscription_id = request.form['subscription_id']
        offer_id = request.form.get('offer_id')  # Optional
        offer_id = offer_id if offer_id else None
        academic_year_id = request.form['academic_year_id']
        no_of_students_subscription = request.form['no_of_students_subscription']
        subscription_amount = request.form['subscription_amount']
        payment_status = request.form['payment_status']
        payment_date = request.form['payment_date']
        status = request.form.get('status') == 'on'
        subscription_date = request.form['subscription_date']
        expiry_date = request.form['expiry_date']

        # Create a new school subscription
        new_subscription = SchoolSubscription(
            title = title,
            school_id=school_id,
            subscription_id=subscription_id,
            offer_id=offer_id,
            academic_year_id=academic_year_id,
            no_of_students_subscription=no_of_students_subscription,
            subscription_amount=subscription_amount,
            payment_status=payment_status,
            payment_date=payment_date,
            status=status,
            subscription_date=subscription_date,
            expiry_date=expiry_date
        )
        db.session.add(new_subscription)
        db.session.commit()

        return redirect(url_for('schoolSubscriptions'))

    schools = School.query.all()
    subscriptions = Subscription.query.all()
    offers = Offer.query.all()
    academic_years = AcademicYear.query.all()

    return render_template(
        'school_subscription_form.html',
        subscription=None,
        schools=schools,
        subscriptions=subscriptions,
        offers=offers,
        academic_years=academic_years
    )


@app.route('/school_subscriptions/edit/<int:id>', methods=['GET', 'POST'])
def edit_school_subscription(id):
    subscription = SchoolSubscription.query.get_or_404(id)

    if request.method == 'POST':
        subscription.title = request.form['title']
        subscription.school_id = request.form['school_id']
        subscription.subscription_id = request.form['subscription_id']
        offer_id = request.form.get('offer_id')  # Optional, may be empty
        subscription.offer_id = offer_id if offer_id else None  # Insert NULL if no offer selected
        subscription.academic_year_id = request.form['academic_year_id']
        subscription.no_of_students_subscription = request.form['no_of_students_subscription']
        subscription.subscription_amount = request.form['subscription_amount']
        subscription.payment_status = request.form['payment_status']
        subscription.payment_date = request.form['payment_date']
        subscription.status = request.form.get('status') == 'on'
        subscription.subscription_date = request.form['subscription_date']
        subscription.expiry_date = request.form['expiry_date']

        db.session.commit()
        return redirect(url_for('schoolSubscriptions'))

    schools = School.query.all()
    subscriptions = Subscription.query.all()
    offers = Offer.query.all()
    academic_years = AcademicYear.query.all()

    return render_template(
        'school_subscription_form.html',
        subscription=subscription,
        schools=schools,
        subscriptions=subscriptions,
        offers=offers,
        academic_years=academic_years
    )


@app.route('/school_subscriptions/delete/<int:id>', methods=['POST'])
def delete_school_subscription(id):
    subscription = SchoolSubscription.query.get_or_404(id)
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({"success": True, "message": "School subscription deleted successfully!"})


@app.route('/ssmrp/list')
def ssmrp():
    return render_template('ssmrp_datatable.html')


@app.route('/api/ssmrp', methods=['GET'])
def api_ssmrp():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    # Query total records
    total_records = SchoolSubscriptionModuleRolePermission.query.count()

    # Search functionality
    query = SchoolSubscriptionModuleRolePermission.query.outerjoin(SchoolSubscription).outerjoin(Module).outerjoin(Role).outerjoin(Permission)
    if search_value:
        query = query.filter(
            SchoolSubscription.title.ilike(f'%{search_value}%') |
            Module.module_name.ilike(f'%{search_value}%') |
            Role.role_name.ilike(f'%{search_value}%') |
            Permission.permission_name.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Pagination
    records = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": record.id,
            "title": record.school_subscription.title,
            "module": record.module.module_name,
            "role": record.role.role_name,
            "permission": record.permission.permission_name
        }
        for record in records
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })

@app.route('/ssmrp/add', methods=['GET', 'POST'])
def add_ssmrp():
    if request.method == 'POST':
        school_subscription_id = request.form['school_subscription_id']
        module_id = request.form['module_id']
        role_id = request.form['role_id']
        permission_id = request.form['permission_id']

        # Create a new record
        new_record = SchoolSubscriptionModuleRolePermission(
            school_subscription_id=school_subscription_id,
            module_id=module_id,
            role_id=role_id,
            permission_id=permission_id
        )
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('ssmrp'))

    # Fetch dropdown data
    school_subscriptions = SchoolSubscription.query.all()
    modules = Module.query.all()
    roles = Role.query.all()
    permissions = Permission.query.all()

    return render_template(
        'ssmrp_form.html',
        record=None,
        school_subscriptions=school_subscriptions,
        modules=modules,
        roles=roles,
        permissions=permissions
    )

@app.route('/ssmrp/edit/<int:id>', methods=['GET', 'POST'])
def edit_ssmrp(id):
    record = SchoolSubscriptionModuleRolePermission.query.get_or_404(id)

    if request.method == 'POST':
        record.school_subscription_id = request.form['school_subscription_id']
        record.module_id = request.form['module_id']
        record.role_id = request.form['role_id']
        record.permission_id = request.form['permission_id']

        db.session.commit()
        return redirect(url_for('ssmrp'))

    # Fetch dropdown data
    school_subscriptions = SchoolSubscription.query.all()
    modules = Module.query.all()
    roles = Role.query.all()
    permissions = Permission.query.all()

    return render_template(
        'ssmrp_form.html',
        record=record,
        school_subscriptions=school_subscriptions,
        modules=modules,
        roles=roles,
        permissions=permissions
    )

@app.route('/ssmrp/delete/<int:id>', methods=['POST'])
def delete_ssmrp(id):
    record = SchoolSubscriptionModuleRolePermission.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"success": True, "message": "Record deleted successfully!"})

@app.route('/modules/list')
def modules():
    return render_template('modules_datatable.html')


@app.route('/api/modules', methods=['GET'])
def api_modules():
    # DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    # Query total records
    total_records = Module.query.count()

    # Search functionality
    query = Module.query
    if search_value:
        query = query.filter(
            Module.module_name.ilike(f'%{search_value}%') |
            Module.menu_name.ilike(f'%{search_value}%')
        )

    # Filtered records count
    filtered_records = query.count()

    # Pagination
    modules = query.offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": module.id,
            "module_name": module.module_name,
            "menu_name": module.menu_name,
            "parent": module.parent.module_name if module.parent else "None",
            "is_active": "Active" if module.is_active else "Inactive",
            "is_visible_in_app": "Yes" if module.is_visible_in_app else "No"
        }
        for module in modules
    ]

    return jsonify({
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": filtered_records,
        "data": data
    })
@app.route('/modules/add', methods=['GET', 'POST'])
def add_module():
    if request.method == 'POST':
        module_name = request.form['module_name']
        menu_name = request.form['menu_name']
        module_link = request.form['module_link']
        parent_id = request.form.get('parent_id')  # Optional
        parent_id = parent_id if parent_id else None  # Set to NULL if not provided
        is_active = request.form.get('is_active') == 'on'
        is_visible_in_app = request.form.get('is_visible_in_app') == 'on'

        # Create a new module
        new_module = Module(
            module_name=module_name,
            menu_name=menu_name,
            module_link=module_link,
            parent_id=parent_id,
            is_active=is_active,
            is_visible_in_app=is_visible_in_app
        )
        db.session.add(new_module)
        db.session.commit()

        return redirect(url_for('modules'))

    # Fetch all modules for parent selection
    modules = Module.query.all()

    return render_template('module_form.html', module=None, modules=modules)

@app.route('/modules/edit/<int:id>', methods=['GET', 'POST'])
def edit_module(id):
    module = Module.query.get_or_404(id)

    if request.method == 'POST':
        module.module_name = request.form['module_name']
        module.menu_name = request.form['menu_name']
        module.module_link= request.form['module_link']
        parent_id = request.form.get('parent_id')  # Optional
        module.parent_id = parent_id if parent_id else None  # Set to NULL if not selected
        module.is_active = request.form.get('is_active') == 'on'
        module.is_visible_in_app = request.form.get('is_visible_in_app') == 'on'

        db.session.commit()
        return redirect(url_for('modules'))

    # Fetch all modules for parent selection
    modules = Module.query.all()

    return render_template('module_form.html', module=module, modules=modules)

@app.route('/modules/delete/<int:id>', methods=['POST'])
def delete_module(id):
    module = Module.query.get_or_404(id)
    db.session.delete(module)
    db.session.commit()
    return jsonify({"success": True, "message": "Module deleted successfully!"})

@app.route('/api/school_subscriptions1', methods=['GET'])
@app.route('/api/school_subscriptions1/<int:school_id>', methods=['GET'])
def api_school_subscriptions1(school_id=None):
    if school_id is None:
        # If no school_id is provided, return all subscriptions
        subscriptions = SchoolSubscription.query.all()
    else:
        # If school_id is provided, filter by the specific school
        subscriptions = SchoolSubscription.query.filter_by(school_id=school_id).all()

    # Now you can return the subscriptions as required
    data = [
        {
            "id": sub.id,
            "subscription": sub.title,
            "academic_year": f"{sub.academic_year.start_date} - {sub.academic_year.end_date}",
            "subscription_amount": sub.subscription_amount,
            "status": "Active" if sub.status else "Inactive"
        }
        for sub in subscriptions
    ]

    return jsonify({
        "data": data
    })
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
  
        if user :
            session['user_id'] = user.id
            session['role'] = user_role(user.id)  # Fetch user's role dynamically
            session['role_id'] = user_role_id(user.id)  # Fetch user's role dynamically
            session['is_superadmin'] = is_superadmin(user.id) 

            if(user.staff_id): 
                get_subscription(user.staff_id) 
            
            return redirect('/dashboard')
        else:
            return "Invalid username or password", 401
    return render_template('login.html')

def user_role(user_id):
    # Fetch user role from UserRoles table
    user_role = db.session.query(Role.role_name).join(UserRole, Role.id == UserRole.role_id).filter(UserRole.user_id == user_id).first()
    return user_role[0] if user_role else None
def user_role_id(user_id):
    # Fetch user role from UserRoles table
    user_roles = (
        db.session.query(Role.id)
        .join(UserRole, Role.id == UserRole.role_id)
        .filter(UserRole.user_id == user_id)
        .all()
    )

    # Store all roles in the session as a list
    session['user_roles'] = [role[0] for role in user_roles]  # Extract role IDs

    # Example return for verification
    return session['user_roles']
def is_superadmin(user_id):
    """Check if the logged-in user is a superadmin."""
    
    if not user_id:
        return False    
    user_roles = UserRole.query.filter_by(user_id=user_id).all()
    for user_role in user_roles:
        role = Role.query.get(user_role.role_id)
        if role and role.id == 3:
            return True
    return False
def get_subscription(staff_id):
    # Fetch user role from UserRoles table
    query = """
        select t1.id,t2.id from school_subscription t1 inner join schools t2 on t2.id = t1.school_id inner join staffs t3  on t3.school_id = t2.id  and t1.status = true and t3.id = :staff_id
    """
    with Session(db.engine) as db_session: 
        result = db_session.execute(
            text(query), 
            {"staff_id": staff_id}
        ).fetchall()
    session['subscription_id'] = result[0][0]
    session['school_id'] = result[0][1]    
     
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    role = session.get('role', 'guest')
    return render_template('dashboard.html', user_role=role)
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return redirect('/login')

@app.route('/api/get_menu_items', methods=['GET'])
def get_menu_items():
    school_id = request.args.get('school_id', type=int)
    session['school_id'] = school_id 

    querySchool = """
        select id from school_subscription where school_id = :school_id and status = true
    """
    with Session(db.engine) as db_session: 
        result = db_session.execute(
            text(querySchool), 
            {"school_id": school_id}
        ).fetchall()
    school_subscription_id = result[0][0]
    if not school_subscription_id:
        school_subscription_id = 1
 
    user_role_id = flask_session.get('role_id')

    if not user_role_id:
        return jsonify({"error": "User not authenticated"}), 403

    if not school_subscription_id:
        return jsonify({"error": "School subscription ID is required"}), 400

    # Fetch menu items based on the school subscription and role
    query = """
        SELECT distinct m.id, m.module_link, m.menu_name, m.parent_id, m.is_active, m.is_visible_in_app,p.permission_name
        FROM modules m
        INNER JOIN school_subscription_module_role_permission ssmrp
            ON m.id = ssmrp.module_id
        INNER JOIN permissions p on p.id = ssmrp.permission_id    
        WHERE ssmrp.school_subscription_id = :school_subscription_id        
        AND m.is_active = TRUE
        AND m.is_visible_in_app = TRUE
        
    """
    if not session.get('is_superadmin'):
        query += " AND ssmrp.role_id IN :role_id"

    # Add ordering
    query += " ORDER BY m.id"
    print(user_role_id)
    print(school_subscription_id)
    print(query)

    with Session(db.engine) as db_session: 
        result = db_session.execute(
            text(query), 
            {"school_subscription_id": school_subscription_id, "role_id": tuple(user_role_id)}
        ).fetchall()

    # Convert result to a JSON-friendly format
    seen_menu_names = set()
    menu_items = [
        {"link": row[1], "menu_name": row[2], "parent_id": row[3], "permission_name": row[6]}
        for row in result
        if row[2] not in seen_menu_names and not seen_menu_names.add(row[2])  # Check and add to set
    ]
    print("1111111111111")
    print(menu_items)
    # Create a map (dictionary) with menu_name as key and permission_name as value
    menu_permission_map = {item['menu_name']: item['permission_name'] for item in menu_items}

    # Now you can store the 'menu_permission_map' in session if needed
    session['menu_permission_map'] = menu_permission_map
    print("222222")
    print(menu_permission_map)
    return jsonify(menu_items)


@app.route('/api/get_schools', methods=['GET'])
def get_schools():
    # Check if the user is superadmin
    user_role_id = flask_session.get('role_id')

    if not user_role_id:
        return jsonify({"error": "User not authenticated"}), 403

    # Check if the user has the superadmin role
     # Assuming 1 is the role ID for superadmin
    if not session.get('is_superadmin'):
        return jsonify({"error": "Access denied"}), 403

    # Fetch schools from the database
    query = text("SELECT s.id, s.title,ss.id FROM schools s INNER JOIN school_subscription ss on s.id = ss.school_id WHERE s.status = TRUE and ss.status = TRUE")
    with Session(db.engine) as db_session: 
        result = db_session.execute(query).fetchall()

    # Convert result to a JSON-friendly format
    schools = [{"id": row[0], "title": row[1],"sid": row[2]} for row in result]
    return jsonify(schools)

@app.route('/staff_types/list', methods=['GET'])
def staff_types_list():
    """Render the staff types list page."""
    return render_template('staff_types_datatable.html')


@app.route('/api/staff_types', methods=['GET'])
def get_staff_types():
    """API to fetch staff types for DataTable."""
    staff_types = StaffType.query.all()
    data = [{"id": st.id, "title": st.title} for st in staff_types]
    return jsonify({"data": data})


@app.route('/staff_types/add', methods=['GET', 'POST'])
def add_staff_type():
    """Add a new staff type."""
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            new_staff_type = StaffType(title=title)
            db.session.add(new_staff_type)
            db.session.commit()
            return redirect(url_for('staff_types_list'))
    return render_template('staff_types_form.html')


@app.route('/staff_types/edit/<int:id>', methods=['GET', 'POST'])
def edit_staff_type(id):
    """Edit an existing staff type."""
    staff_type = StaffType.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            staff_type.title = title
            db.session.commit()
            return redirect(url_for('staff_types_list'))
    return render_template('staff_types_form.html', staff_type=staff_type)


@app.route('/staff_types/delete/<int:id>', methods=['POST'])
def delete_staff_type(id):
    """Delete a staff type."""
    staff_type = StaffType.query.get_or_404(id)
    db.session.delete(staff_type)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/staffs/list', methods=['GET'])
def list_staffs():
    selected_school_id = session.get('school_id')
    print(selected_school_id)
    return render_template('staffs_list.html')

@app.route('/api/staffs', methods=['GET'])
def get_staffs():
    """API to fetch staff data for DataTable."""
    staffs = Staff.query.filter_by(school_id=session.get('school_id')).all()

    data = [
        {
            "id": staff.id,
            "school": staff.school.title if staff.school else "Unknown",
            "staff_type": staff.staff_type.title if staff.staff_type else "Unknown",
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "status": "Active" if staff.status else "Inactive",
        }
        for staff in staffs
    ]
    return jsonify({"data": data})

@app.route('/staffs/add', methods=['GET', 'POST'])
def add_staff():
    """Add a new staff member with user and roles."""
    schools = School.query.all()
    staff_types = StaffType.query.all()
    roles = Role.query.all()  # Fetch all available roles

    if request.method == 'POST':
        # Staff details
        school_id = session.get('school_id')
        staff_type_id = request.form.get('staff_type_id')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        permanent_address = request.form.get('permanent_address')
        communication_address = request.form.get('communication_address')
        blood_group = request.form.get('blood_group')
        qualification = request.form.get('qualification')
        is_section_in_charge = request.form.get('is_section_in_charge') == 'true'
        section_details = request.form.get('section_details')
        is_transport_in_charge = request.form.get('is_transport_in_charge') == 'true'
        transport_details = request.form.get('transport_details')
        joining_date = request.form.get('joining_date')
        relieving_date = request.form.get('relieving_date')
        relieving_comment = request.form.get('relieving_comment')
        status = request.form.get('status') == 'true'

        # Create the Staff object
        new_staff = Staff(
            school_id=school_id,
            staff_type_id=staff_type_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            permanent_address=permanent_address,
            communication_address=communication_address,
            blood_group=blood_group,
            qualification=qualification,
            is_section_in_charge=is_section_in_charge,
            section_details=section_details,
            is_transport_in_charge=is_transport_in_charge,
            transport_details=transport_details,
            joining_date=joining_date,
            relieving_date=relieving_date,
            relieving_comment=relieving_comment,
            status=status,
        )
        db.session.add(new_staff)
        db.session.commit()

        # User details
        username = request.form.get('username')
        password = request.form.get('password')  # In real apps, hash the password!
        is_active = request.form.get('is_active') == 'on'
        roles_selected = request.form.getlist('roles')  # List of selected role IDs

        # Create the User object
        new_user = User(
            staff_id=new_staff.id,  # Link the new staff record
            username=username,
            password=password,
            is_active=is_active,
        )
        db.session.add(new_user)
        db.session.commit()

        # Add roles to user_roles table
        for role_id in roles_selected:
            user_role = UserRole(user_id=new_user.id, role_id=role_id)
            db.session.add(user_role)

        db.session.commit()

        return redirect(url_for('list_staffs'))

    return render_template('staffs_form.html', schools=schools, staff_types=staff_types, roles=roles, staff=None, user=None, assigned_roles=[])



@app.route('/staffs/edit/<int:id>', methods=['GET', 'POST'])
def edit_staff(id):
    """Edit an existing staff member with user and roles."""
    staff = Staff.query.get_or_404(id)
    schools = School.query.all()
    staff_types = StaffType.query.all()
    roles = Role.query.all()

    user = User.query.filter_by(staff_id=staff.id).first()
    assigned_roles = [ur.role_id for ur in UserRole.query.filter_by(user_id=user.id).all()] if user else []

    if request.method == 'POST':
        # Staff details
        staff.school_id = session.get('school_id')
        staff.staff_type_id = request.form.get('staff_type_id')
        staff.first_name = request.form.get('first_name')
        staff.middle_name = request.form.get('middle_name')
        staff.last_name = request.form.get('last_name')
        staff.permanent_address = request.form.get('permanent_address')
        staff.communication_address = request.form.get('communication_address')
        staff.blood_group = request.form.get('blood_group')
        staff.qualification = request.form.get('qualification')
        staff.is_section_in_charge = request.form.get('is_section_in_charge') == 'true'
        staff.section_details = request.form.get('section_details')
        staff.is_transport_in_charge = request.form.get('is_transport_in_charge') == 'true'
        staff.transport_details = request.form.get('transport_details')
        staff.joining_date = request.form.get('joining_date')
        staff.relieving_date = request.form.get('relieving_date')
        staff.relieving_comment = request.form.get('relieving_comment')
        staff.status = request.form.get('status') == 'true'

        # User details
        username = request.form.get('username')
        password = request.form.get('password')  # In real apps, hash the password!
        is_active = request.form.get('is_active') == 'on'
        roles_selected = request.form.getlist('roles')

        # Update User object
        if user:
            user.username = username
            user.password = password
            user.is_active = is_active
        else:  # Create a new user if not already linked
            user = User(
                staff_id=staff.id,
                username=username,
                password=password,
                is_active=is_active,
            )
            db.session.add(user)
            db.session.commit()

        # Update user roles
        UserRole.query.filter_by(user_id=user.id).delete()  # Clear existing roles
        for role_id in roles_selected:
            user_role = UserRole(user_id=user.id, role_id=role_id)
            db.session.add(user_role)

        db.session.commit()

        return redirect(url_for('list_staffs'))

    return render_template('staffs_form.html', schools=schools, staff_types=staff_types, roles=roles, staff=staff, user=user, assigned_roles=assigned_roles)



@app.route('/staffs/delete/<int:id>', methods=['POST'])
def delete_staff(id):
    """Delete a staff record."""
    staff = Staff.query.get_or_404(id)
    db.session.delete(staff)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/api/club', methods=['GET'])
def get_clubs():   
    """API to fetch staff data for DataTable."""
    clubs = Club.query.all()
    data = [
        {
            "id": club.id,
            "title": club.title,
            "description": club.description,
            "status": "Active" if club.status else "Inactive",
        }
        for club in clubs
    ]

    return jsonify({"data": data})
@app.route('/clubs/list', methods=['GET'])
def list_clubs():
    """Render the staff list page."""
    return render_template('clubs_list.html')

@app.route('/clubs/add', methods=['GET', 'POST'])
def add_club():
    school_id = session.get('school_id')  # Get school_id from session
    if not school_id:
        return jsonify({'error': 'School ID not found in session'}), 400

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status') == 'on'

        new_club = Club(
            school_id=school_id,
            title=title,
            description=description,
            status=status
        )
        db.session.add(new_club)
        db.session.commit()

        return redirect(url_for('list_clubs'))

    return render_template('clubs_form.html', club=None)

@app.route('/clubs/edit/<int:id>', methods=['GET', 'POST'])
def edit_club(id):
    club = Club.query.get_or_404(id)

    # Ensure the club belongs to the logged-in user's school
    if club.school_id != session.get('school_id'):
        return jsonify({'error': 'Unauthorized access'}), 403

    if request.method == 'POST':
        club.title = request.form.get('title')
        club.description = request.form.get('description')
        club.status = request.form.get('status') == 'on'

        db.session.commit()
        return redirect(url_for('list_clubs'))

    return render_template('clubs_form.html', club=club)

@app.route('/clubs/delete/<int:id>', methods=['POST'])
def delete_club(id):
    club = Club.query.get_or_404(id)

    # Ensure the club belongs to the logged-in user's school
    if club.school_id != session.get('school_id'):
        return jsonify({'error': 'Unauthorized access'}), 403

    db.session.delete(club)
    db.session.commit()
    return redirect(url_for('list_clubs'))





if __name__ == '__main__':
    app.run(debug=True)
