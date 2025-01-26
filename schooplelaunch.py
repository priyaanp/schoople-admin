from flask import Flask, render_template, request, redirect, url_for, jsonify,session
from flask import session as flask_session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql import text 
from models import Club, Grade, House, SchoolStudent, SchoolsGradesSections, Section, StaffsGrades, Student, Subject, Transport, db, Offer,Subscription,Role,User,UserRole,Permission,School,AcademicYear,SchoolSubscription,Module,SchoolSubscriptionModuleRolePermission,StaffType,Staff,ExamMarks,ExamMarkDetails
from werkzeug.security import check_password_hash
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
@app.route('/subscriptions/list')
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
    
@app.route('/subscriptions/add', methods=['GET', 'POST'])
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

@app.route('/subscriptions/edit/<int:id>', methods=['GET', 'POST'])
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

@app.route('/subscriptions/delete/<int:id>', methods=['POST'])
def delete_subscription(id):
    subscription = Subscription.query.get_or_404(id)
    db.session.delete(subscription)
    db.session.commit()
    return redirect(url_for('list_subscriptions'))

@app.route('/offers/list')
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
@app.route('/offers/add', methods=['GET', 'POST'])
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
@app.route('/offers/edit/<int:id>', methods=['GET', 'POST'])
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
@app.route('/offers/delete/<int:id>', methods=['POST'])
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
        new_user = User(username=username, is_active=is_active)
        new_user.set_password(password)
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
        user.is_active = request.form.get('is_active') == 'on'
        role_ids = request.form.getlist('roles')
        new_password = request.form['password']
        if new_password:
            user.set_password(new_password) 
        # Clear existing roles
        

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
    modules = query.order_by(Module.priority).offset(start).limit(length).all()

    # Format data for DataTables
    data = [
        {
            "id": module.id,
            "module_name": module.module_name,
            "menu_name": module.menu_name,
            "parent": module.parent.module_name if module.parent else "None",
            "is_active": "Active" if module.is_active else "Inactive",
            "is_visible_in_app": "Yes" if module.is_visible_in_app else "No",
            "priority": module.priority,
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
        priority =  request.form['priority']

        # Create a new module
        new_module = Module(
            module_name=module_name,
            menu_name=menu_name,
            module_link=module_link,
            parent_id=parent_id,
            is_active=is_active,
            is_visible_in_app=is_visible_in_app,
            priority=priority
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
        module.priority = request.form['priority']

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
  
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = username
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
def checkLoggedin():
    
    if not session.get('user_id'):  # 'logged_in' is the session key for login status
        return render_template('login.html')
 # Redirect to login page if not logged in     
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    role = session.get('role', 'guest')
    return render_template('dashboard.html', user_role=role)

@app.route('/')
def index():
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
        SELECT distinct m.id, m.module_link, m.menu_name, m.parent_id, m.is_active, m.is_visible_in_app,p.permission_name,m.priority
        FROM modules m
        INNER JOIN school_subscription_module_role_permission ssmrp
            ON m.id = ssmrp.module_id
        INNER JOIN permissions p on p.id = ssmrp.permission_id    
        WHERE ssmrp.school_subscription_id = :school_subscription_id        
        AND m.is_active = TRUE       
        
    """
    if not session.get('is_superadmin'):
        query += " AND ssmrp.role_id IN :role_id"

    # Add ordering
    query += " ORDER BY m.priority"


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

    # Create a map (dictionary) with menu_name as key and permission_name as value
    menu_permission_map = {item['menu_name']: item['permission_name'] for item in menu_items}

    # Now you can store the 'menu_permission_map' in session if needed
    session['menu_permission_map'] = menu_permission_map

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
    login_redirect = checkLoggedin()
    if login_redirect:
        return login_redirect 
    selected_school_id = session.get('school_id')

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
            is_active=is_active,
        )
        new_user.set_password(password)
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
            new_password = request.form['password']
            user.is_active = is_active
            if new_password:
                user.set_password(new_password)    
            
        else:  # Create a new user if not already linked
            user = User(
                staff_id=staff.id,
                username=username,                
                is_active=is_active,
            )
            user.set_password(password)

                
        db.session.add(user)
        db.session.commit()

        # Update user roles
        
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

@app.route('/api/students1', methods=['GET'])
def get_students1():
    """API to fetch staff data for DataTable."""
    students = Student.query.filter_by(school_id=session.get('school_id')).all()

    data = [
        {
            "id": student.id,
            "student_code": student.student_code,            
            "first_name": student.first_name,
            "last_name": student.last_name,
            "dob":student.dob,
            "status": student.status,
        }
        for student in students
    ]
    return jsonify({"data": data})
@app.route('/api/students', methods=['GET'])
def get_students():
    """Fetch students based on grade and section filters."""
    school_id = session.get('school_id')  # Ensure school_id is fetched from the session
    grade_id = request.args.get('grade_id')
    section_id = request.args.get('section_id')
    academic_year_id = request.args.get('academic_year_id')

    # Query students based on filters
    query = db.session.query(
        Student.id.label("id"),
        Student.student_code.label("student_code"),     
        Student.first_name.label("first_name"),
        Student.last_name.label("last_name"),
        Student.dob.label("dob"),
        Grade.title.label("grade"),
        Section.title.label("section"),
        School.title.label("school"),
        db.case(
        (Student.status == 1, "Passed"),
        else_="Failed"
    ).label("status")
    ).join(
        SchoolStudent, SchoolStudent.student_id == Student.id
    ).join(
        SchoolsGradesSections, SchoolsGradesSections.id == SchoolStudent.school_grade_section_id
    ).join(
        Grade, Grade.id == SchoolsGradesSections.grade_id
    ).join(
        Section, Section.id == SchoolsGradesSections.section_id
    ).join(
        School, School.id == Student.school_id
    ).filter(
        Student.school_id == school_id
    )

    # Apply grade filter
    if grade_id:
        query = query.filter(SchoolsGradesSections.grade_id == grade_id)

    # Apply section filter
    if section_id:
        query = query.filter(SchoolsGradesSections.section_id == section_id)

    if academic_year_id:
       query = query.filter(SchoolsGradesSections.academic_year_id == academic_year_id)     

    students = query.all()

    # Format data for DataTables
    data = [
        {
           
            "id": student.id,
            "student_code":student.student_code,
            "name": f"{student.first_name} {student.last_name}",
            "grade": student.grade,
            "section": student.section,
            "dob":student.dob,
            "school": student.school,
            "status": student.status,
        }
        for student in students
    ]

    return jsonify({"data": data})



@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        school_id = session.get('school_id')  # Get school_id from session
        if not school_id:
            return jsonify({'error': 'School ID is not set in the session'}), 400

        # Retrieve student details from form
        student_data = {
            'school_id': school_id,
            'student_code': request.form.get('student_code'),
            'first_name': request.form.get('first_name'),
            'middle_name': request.form.get('middle_name'),
            'last_name': request.form.get('last_name'),
            'dob': request.form.get('dob'),
            'aadhar_number': request.form.get('aadhar_number'),
            'photo': request.form.get('photo'),
            'date_of_admission': request.form.get('date_of_admission'),
            'admission_number': request.form.get('admission_number'),
            'identification_mark': request.form.get('identification_mark'),
            'interests': request.form.get('interests'),
            'hobbies': request.form.get('hobbies'),
            'student_email': request.form.get('student_email'),
            'religion': request.form.get('religion'),
            'caste': request.form.get('caste'),
            'permanent_address': request.form.get('permanent_address'),
            'communication_address': request.form.get('communication_address'),
            'mother_name': request.form.get('mother_name'),
            'father_name': request.form.get('father_name'),
            'father_qualification': request.form.get('father_qualification'),
            'mother_qualification': request.form.get('mother_qualification'),
            'father_occupation': request.form.get('father_occupation'),
            'mother_occupation': request.form.get('mother_occupation'),
            'father_mobile': request.form.get('father_mobile'),
            'mother_mobile': request.form.get('mother_mobile'),
            'father_email': request.form.get('father_email'),
            'mother_email': request.form.get('mother_email'),
            'annual_income': request.form.get('annual_income'),
            'blood_group': request.form.get('blood_group'),
            'mother_tongue': request.form.get('mother_tongue'),
            'is_single_girl': request.form.get('is_single_girl') == 'on',
            'is_minority': request.form.get('is_minority') == 'on',
            'sibling_status': request.form.get('sibling_status') == 'on',
            'status': request.form.get('status')
        }

        # Insert into `students` table
        new_student = Student(**student_data)
        db.session.add(new_student)
        db.session.commit()

        # Create a corresponding user entry in the `users` table
        user_data = {
            'student_id': new_student.id,
            'username': request.form.get('username'),
            'password': request.form.get('password'),  # Hash the password
            'is_active': request.form.get('is_active') == 'on',
        }
        new_user = User(**user_data)
        new_user.set_password(new_user.password)
        db.session.add(new_user)
        db.session.commit()

# Insert into school_student table
        new_school_student = SchoolStudent(
            student_id=new_student.id,
            house_id=request.form['house_id'] or None,
            clubs=request.form['clubs'],
            school_grade_section_id=request.form['school_grade_section_id'],
            academic_year_id=request.form['academic_year_id'],
            transport_id=request.form['transport_id'] or None,
            status=request.form.get('status') == '1'
        )
        db.session.add(new_school_student)
        db.session.commit()

        return redirect('/students/list')
    houses = House.query.filter_by(school_id=session['school_id']).all()
    grade_sections = SchoolsGradesSections.query.filter_by(school_id=session['school_id']).all()
    academic_years = AcademicYear.query.all()
    transports = Transport.query.filter_by(school_id=session['school_id']).all()

    return render_template(
        'student_form.html',
        student=None,
        school_student=None,
        houses=houses,
        grade_sections=grade_sections,
        academic_years=academic_years,
        transports=transports
    )
    return render_template('student_form.html', student=None, user=None)

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    user = User.query.filter_by(student_id=id).first()
    school_student = SchoolStudent.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        # Update student details
        student.student_code = request.form.get('student_code')
        student.first_name = request.form.get('first_name')
        student.middle_name = request.form.get('middle_name')
        student.last_name = request.form.get('last_name')
        student.dob = request.form.get('dob')
        student.aadhar_number = request.form.get('aadhar_number')
        student.photo = request.form.get('photo')
        student.date_of_admission = request.form.get('date_of_admission')
        student.admission_number = request.form.get('admission_number')
        student.identification_mark = request.form.get('identification_mark')
        student.interests = request.form.get('interests')
        student.hobbies = request.form.get('hobbies')
        student.student_email = request.form.get('student_email')
        student.religion = request.form.get('religion')
        student.caste = request.form.get('caste')
        student.permanent_address = request.form.get('permanent_address')
        student.communication_address = request.form.get('communication_address')
        student.mother_name = request.form.get('mother_name')
        student.father_name = request.form.get('father_name')
        student.father_qualification = request.form.get('father_qualification')
        student.mother_qualification = request.form.get('mother_qualification')
        student.father_occupation = request.form.get('father_occupation')
        student.mother_occupation = request.form.get('mother_occupation')
        student.father_mobile = request.form.get('father_mobile')
        student.mother_mobile = request.form.get('mother_mobile')
        student.father_email = request.form.get('father_email')
        student.mother_email = request.form.get('mother_email')
        student.annual_income = request.form.get('annual_income')
        student.blood_group = request.form.get('blood_group')
        student.mother_tongue = request.form.get('mother_tongue')
        student.is_single_girl = request.form.get('is_single_girl') == 'on'
        student.is_minority = request.form.get('is_minority') == 'on'
        student.sibling_status = request.form.get('sibling_status') == 'on'
        student.status = request.form.get('status')

        # Update the corresponding user entry

        username = request.form.get('username')
        password = request.form.get('password')  # In real apps, hash the password!
        is_active = request.form.get('is_active') == 'on'
        roles_selected = request.form.getlist('roles')

        # Update User object
        if user:
            user.username = username
            new_password = request.form['password']
            user.is_active = is_active
            if new_password:
                user.set_password(new_password)    
            
        else:  # Create a new user if not already linked
            user = User(               
                username=username,                
                is_active=is_active,
            )
            user.set_password(password)                
        db.session.add(user)
        db.session.commit()

        if school_student:
            school_student.house_id = request.form['house_id'] or None
            school_student.clubs = request.form['clubs']
            school_student.school_grade_section_id = request.form['school_grade_section_id']
            school_student.academic_year_id = request.form['academic_year_id']
            school_student.transport_id = request.form['transport_id'] or None
            school_student.status = request.form.get('status') == '1'
        else:
            # Create a new SchoolStudent record
            school_student = SchoolStudent(
                student_id=id,
                house_id=request.form['house_id'] or None,
                clubs=request.form['clubs'],
                school_grade_section_id=request.form['school_grade_section_id'],
                academic_year_id=request.form['academic_year_id'],
                transport_id=request.form['transport_id'] or None,
                status=request.form.get('status') == '1'
            )
            db.session.add(school_student)
        db.session.commit()
        return redirect('/students/list')
    houses = House.query.filter_by(school_id=session['school_id']).all()
    users = User.query.filter_by(student_id=id).first()
    grade_sections = SchoolsGradesSections.query.filter_by(school_id=session['school_id']).all()
    academic_years = AcademicYear.query.all()
    transports = Transport.query.filter_by(school_id=session['school_id']).all()
    houses = House.query.filter_by(school_id=session['school_id']).all()
    print(users)
    return render_template(
        'student_form.html',
        student=student,
        users=users,
        school_student=school_student,
        houses=houses,
        grade_sections=grade_sections,
        academic_years=academic_years,
        transports=transports
    )
    return render_template('student_form.html', student=student, user=user)

@app.route('/students/list')
def list_students(): 
    school_id = session.get('school_id')   
    grades = Grade.query.join(
        SchoolsGradesSections, Grade.id == SchoolsGradesSections.grade_id
    ).filter(SchoolsGradesSections.school_id == school_id).all()

    sections = Section.query.join(
        SchoolsGradesSections, Section.id == SchoolsGradesSections.section_id
    ).filter(SchoolsGradesSections.school_id == school_id).all()
    academic_years = AcademicYear.query.all()
    active_academic_year = AcademicYear.query.filter_by(active=True).first()

    return render_template(
        'students_list.html',
        grades=grades,
        sections=sections,
        academic_years=academic_years,
        active_academic_year_id=active_academic_year.id if active_academic_year else None
    )


@app.route('/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    try:
        # Find the user associated with the student
        user = User.query.filter_by(student_id=id).first()
        if user:
            db.session.delete(user)  # Delete the user record first
        
        # Find the student and delete it
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/grades/list', methods=['GET'])
def grades_list():
    """Render the grades list page."""
    return render_template('grades_list.html')


@app.route('/api/grades', methods=['GET'])
def grades_data():
    """Fetch and return grades data for DataTables."""
    grades = Grade.query.join(School, Grade.school_id == School.id).all()
    data = [
        {
            "id": grade.id,
            "school": grade.school.title,  # Assuming a relationship to the `School` table
            "title": grade.title
        }
        for grade in grades
    ]
    return jsonify({"data": data})


@app.route('/grades/add', methods=['GET', 'POST'])
def add_grade():
    """Add a new grade."""
    if request.method == 'POST':
        grade = Grade(
            school_id=session.get('school_id'),  # Fetch the current school ID from the session
            title=request.form['title']
        )
        db.session.add(grade)
        db.session.commit()
        return redirect('/grades/list')

    return render_template('grades_form.html', grade=None)


@app.route('/grades/edit/<int:id>', methods=['GET', 'POST'])
def edit_grade(id):
    """Edit an existing grade."""
    grade = Grade.query.get_or_404(id)

    if request.method == 'POST':
        grade.title = request.form['title']
        db.session.commit()
        return redirect('/grades/list')

    return render_template('grades_form.html', grade=grade)


@app.route('/grades/delete/<int:id>', methods=['POST'])
def delete_grade(id):
    """Delete a grade."""
    grade = Grade.query.get_or_404(id)
    db.session.delete(grade)
    db.session.commit()
    return jsonify({"message": "Grade deleted successfully"})


@app.route('/sections/list', methods=['GET'])
def sections_list():
    """Render the sections list page."""
    return render_template('sections_list.html')


@app.route('/api/sections', methods=['GET'])
def sections_data():
    """Fetch and return sections data for DataTables."""
    sections = Section.query.join(School, Section.school_id == School.id).all()
    data = [
        {
            "id": section.id,
            "school": section.school.title,  # Assuming a relationship to the `School` table
            "title": section.title
        }
        for section in sections
    ]
    return jsonify({"data": data})


@app.route('/sections/add', methods=['GET', 'POST'])
def add_section():
    """Add a new section."""
    if request.method == 'POST':
        section = Section(
            school_id=session.get('school_id'),  # Fetch the current school ID from the session
            title=request.form['title']
        )
        db.session.add(section)
        db.session.commit()
        return redirect('/sections/list')

    return render_template('sections_form.html', section=None)


@app.route('/sections/edit/<int:id>', methods=['GET', 'POST'])
def edit_section(id):
    """Edit an existing section."""
    section = Section.query.get_or_404(id)

    if request.method == 'POST':
        section.title = request.form['title']
        db.session.commit()
        return redirect('/sections/list')

    return render_template('sections_form.html', section=section)


@app.route('/sections/delete/<int:id>', methods=['POST'])
def delete_section(id):
    """Delete a section."""
    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "Section deleted successfully"})


@app.route('/schools-grades-sections/list', methods=['GET'])
def schools_grades_sections_list():
    """Render the list page for schools_grades_sections."""
    return render_template('schools_grades_sections_list.html')


@app.route('/api/schools-grades-sections', methods=['GET'])
def schools_grades_sections_data():
    """Fetch and return data for the schools_grades_sections table."""
    sections = (
        db.session.query(
            SchoolsGradesSections.id,
            School.title.label('school'),
            Grade.title.label('grade'),
            Section.title.label('section'),
            AcademicYear.start_date,
            AcademicYear.end_date
        )
        .join(School, SchoolsGradesSections.school_id == School.id)
        .join(Grade, SchoolsGradesSections.grade_id == Grade.id)
        .join(Section, SchoolsGradesSections.section_id == Section.id)
        .join(AcademicYear, SchoolsGradesSections.academic_year_id == AcademicYear.id)
        .all()
    )

    data = [
        {
            "id": section.id,
            "school": section.school,
            "grade": section.grade,
            "section": section.section,
            "academic_year": f"{section.start_date} - {section.end_date}"
        }
        for section in sections
    ]

    return jsonify({"data": data})


@app.route('/schools-grades-sections/add', methods=['GET', 'POST'])
def add_schools_grades_sections():
    """Add a new record to schools_grades_sections."""
    if request.method == 'POST':
        new_section = SchoolsGradesSections(
            school_id=session.get('school_id'),
            grade_id=request.form['grade_id'],
            section_id=request.form['section_id'],
            academic_year_id=request.form['academic_year_id']
        )
        db.session.add(new_section)
        db.session.commit()
        return redirect('/schools-grades-sections/list')

    schools = School.query.all()
    grades = Grade.query.all()
    sections = Section.query.all()
    academic_years = AcademicYear.query.all()

    return render_template(
        'schools_grades_sections_form.html',
        schools=schools,
        grades=grades,
        sections=sections,
        academic_years=academic_years,
        section=None
    )


@app.route('/schools-grades-sections/edit/<int:id>', methods=['GET', 'POST'])
def edit_schools_grades_sections(id):
    """Edit an existing record in schools_grades_sections."""
    section = SchoolsGradesSections.query.get_or_404(id)

    if request.method == 'POST':
        
        section.grade_id = request.form['grade_id']
        section.section_id = request.form['section_id']
        section.academic_year_id = request.form['academic_year_id']
        db.session.commit()
        return redirect('/schools-grades-sections/list')

    schools = School.query.all()
    grades = Grade.query.all()
    sections = Section.query.all()
    academic_years = AcademicYear.query.all()

    return render_template(
        'schools_grades_sections_form.html',
        schools=schools,
        grades=grades,
        sections=sections,
        academic_years=academic_years,
        section=section
    )


@app.route('/schools-grades-sections/delete/<int:id>', methods=['POST'])
def delete_schools_grades_sections(id):
    """Delete a record from schools_grades_sections."""
    section = SchoolsGradesSections.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully"})


@app.route('/houses/list', methods=['GET'])
def houses_list():
    """Render the houses list page."""
    return render_template('houses_list.html')


@app.route('/api/houses', methods=['GET'])
def houses_data():
    """Fetch and return data for the houses table."""
    school_id = session.get('school_id')
    if not school_id:
        return jsonify({"error": "School ID not found in session"}), 400

    houses = House.query.filter_by(school_id=school_id).all()
    data = [
        {
            "id": house.id,
            "title": house.title,
            "description": house.description,
            "color": house.color,
            "status": "Active" if house.status else "Inactive",
        }
        for house in houses
    ]
    return jsonify({"data": data})


@app.route('/houses/add', methods=['GET', 'POST'])
def add_house():
    """Add a new house."""
    if request.method == 'POST':
        school_id = session.get('school_id')
        if not school_id:
            return jsonify({"error": "School ID not found in session"}), 400

        new_house = House(
            school_id=school_id,
            title=request.form['title'],
            description=request.form['description'],
            color=request.form['color'],
            status=request.form.get('status') == 'on',  # Convert checkbox value to boolean
        )
        db.session.add(new_house)
        db.session.commit()
        return redirect('/houses/list')

    return render_template('houses_form.html', house=None)


@app.route('/houses/edit/<int:id>', methods=['GET', 'POST'])
def edit_house(id):
    """Edit an existing house."""
    house = House.query.get_or_404(id)

    if request.method == 'POST':
        house.title = request.form['title']
        house.description = request.form['description']
        house.color = request.form['color']
        house.status = request.form.get('status') == 'on'
        db.session.commit()
        return redirect('/houses/list')

    return render_template('houses_form.html', house=house)


@app.route('/houses/delete/<int:id>', methods=['POST'])
def delete_house(id):
    """Delete a house."""
    house = House.query.get_or_404(id)
    db.session.delete(house)
    db.session.commit()
    return jsonify({"message": "House deleted successfully"})

@app.route('/transports/list', methods=['GET'])
def transports_list():
    """Render the transports list page."""
    return render_template('transports_list.html')


@app.route('/api/transports', methods=['GET'])
def transports_data():
    """Fetch and return data for the transports table."""
    school_id = session.get('school_id')
    if not school_id:
        return jsonify({"error": "School ID not found in session"}), 400

    transports = Transport.query.filter_by(school_id=school_id).all()
    data = [
        {
            "id": transport.id,
            "driver": f"{transport.driver.first_name} {transport.driver.last_name}" if transport.driver else "N/A",
            "driver_code": transport.driver_code,
            "vehicle_number": transport.vehicle_number,
            "route_number": transport.route_number,
            "route_name": transport.route_name,
            "vehicle_gps_device_id": transport.vehicle_gps_device_id,
            "vehicle_tracking_url": transport.vehicle_tracking_url,
            "in_charge": f"{transport.in_charge.first_name} {transport.in_charge.last_name}" if transport.in_charge else "N/A",
        }
        for transport in transports
    ]
    return jsonify({"data": data})


@app.route('/transports/add', methods=['GET', 'POST'])
def add_transport():
    """Add a new transport."""
    if request.method == 'POST':
        school_id = session.get('school_id')
        if not school_id:
            return jsonify({"error": "School ID not found in session"}), 400

        new_transport = Transport(
            school_id=school_id,
            driver_id=request.form['driver_id'],
            driver_code=request.form['driver_code'],
            vehicle_number=request.form['vehicle_number'],
            route_number=request.form['route_number'],
            route_name=request.form['route_name'],
            vehicle_gps_device_id=request.form['vehicle_gps_device_id'],
            vehicle_tracking_url=request.form['vehicle_tracking_url'],
            in_charge_id=request.form['in_charge_id'],
        )
        db.session.add(new_transport)
        db.session.commit()
        return redirect('/transports/list')

    staffs = Staff.query.filter_by(school_id=session.get('school_id')).all()
    return render_template('transports_form.html', transport=None, staffs=staffs)


@app.route('/transports/edit/<int:id>', methods=['GET', 'POST'])
def edit_transport(id):
    """Edit an existing transport."""
    transport = Transport.query.get_or_404(id)

    if request.method == 'POST':
        transport.driver_id = request.form['driver_id']
        transport.driver_code = request.form['driver_code']
        transport.vehicle_number = request.form['vehicle_number']
        transport.route_number = request.form['route_number']
        transport.route_name = request.form['route_name']
        transport.vehicle_gps_device_id = request.form['vehicle_gps_device_id']
        transport.vehicle_tracking_url = request.form['vehicle_tracking_url']
        transport.in_charge_id = request.form['in_charge_id']
        db.session.commit()
        return redirect('/transports/list')

    staffs = Staff.query.filter_by(school_id=session.get('school_id')).all()
    return render_template('transports_form.html', transport=transport, staffs=staffs)


@app.route('/transports/delete/<int:id>', methods=['POST'])
def delete_transport(id):
    """Delete a transport."""
    transport = Transport.query.get_or_404(id)
    db.session.delete(transport)
    db.session.commit()
    return jsonify({"message": "Transport deleted successfully"})

@app.route('/staff_assignment/list', methods=['GET'])
def staffs_grades_list():
    """Render the list page."""
    return render_template('staffs_grades_list.html')

@app.route('/api/staff_assignment', methods=['GET'])
def get_staffs_grades():
    """Fetch Staff Grades data, filtered by school."""
    school_id = session.get('school_id')
    print("school_id")
    print(school_id)
    if not school_id:
        return jsonify({"error": "School ID not found in session"}), 400

    # Get all schools_grades_sections filtered by school_id
    schools_grades_sections = SchoolsGradesSections.query.filter_by(school_id=school_id).all()

    # Create a mapping of schools_grades_sections by id for easy lookup
    sgs_mapping = {sgs.id: sgs for sgs in schools_grades_sections}

    # Fetch staff grades
    staff_grades = StaffsGrades.query.filter(
        StaffsGrades.schools_grades_sections_id.in_(sgs_mapping.keys())
    ).all()

    data = [
        {
            "id": sg.id,
            "staff": f"{sg.staff.first_name} {sg.staff.last_name}" if sg.staff else "N/A",
            "grade": sgs_mapping[sg.schools_grades_sections_id].grade.title if sg.schools_grades_sections_id in sgs_mapping else "N/A",
            "division": sgs_mapping[sg.schools_grades_sections_id].section.title if sg.schools_grades_sections_id in sgs_mapping else "N/A",
            "subject": sg.subject.title if sg.subject else "N/A",
            "is_class_in_charge": sg.is_class_in_charge,
            "is_class_in_charge_second": sg.is_class_in_charge_second,
            "transport": sg.transport.route_name if sg.transport else "N/A",
        }
        for sg in staff_grades
    ]

    return jsonify({"data": data})




@app.route('/staff_assignment/add', methods=['GET', 'POST'])
@app.route('/staff_assignment/edit/<int:id>', methods=['GET', 'POST'])
def add_edit_staffs_grades(id=None):
    """Add or Edit Staff Grade."""
    # Fetch existing data for editing if an ID is provided
    print("Received ID:", id)

    staff_grade = StaffsGrades.query.get(id) if id else None

    # Fetch dropdown data for form rendering


    # Ensure school_id is available in session
    school_id = session.get('school_id')
    if not school_id:
        return jsonify({"error": "School ID not found in session"}), 400

    # Initialize variables
    staff_grade = StaffsGrades.query.get(id) if id else None

    # Fetch dropdown data
    staffs = Staff.query.filter_by(school_id=school_id).all()  # Filter by school
    grades = Grade.query.all()  # Retrieve all grades
    divisions = Section.query.all()  # Retrieve all divisions
    subjects = Subject.query.filter_by(school_id=school_id).all()  # Filter by school
    transports = Transport.query.filter_by(school_id=school_id).all()  # Filter by school



    # Handle POST request (save the data)
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        is_class_in_charge = request.form.get('is_class_in_charge') == 'true'
        is_class_in_charge_second = request.form.get('is_class_in_charge_second') == 'true'
        is_transport_in_charge = request.form.get('is_transport_in_charge') == 'true'

        transport_id = request.form.get('transport_id') or None

        grades_list = request.form.getlist('grades[]')
        divisions_list = request.form.getlist('divisions[]')
        subjects_list = request.form.getlist('subjects[]')
        class_in_charge_grade = request.form['class_in_charge_grade']
        class_in_charge_division = request.form['class_in_charge_division']
        class_in_charge_second_grade = request.form['class_in_charge_second_grade']
        class_in_charge_second_division = request.form['class_in_charge_second_division']



        # Handle Edit
        if id:
            for grade_id, division_id, subject_id in zip(grades_list, divisions_list, subjects_list):
                sgs = SchoolsGradesSections.query.filter_by(
                    school_id=school_id,
                    grade_id=grade_id,
                    section_id=division_id
                ).first()

                if not sgs:
                    return jsonify({"error": "Invalid grade or division selection"}), 400
                sgs1 = SchoolsGradesSections.query.filter_by(
                    school_id=school_id,
                    grade_id=class_in_charge_grade,
                    section_id=class_in_charge_division
                ).first()
                sgs2 = SchoolsGradesSections.query.filter_by(
                    school_id=school_id,
                    grade_id=class_in_charge_second_grade,
                    section_id=class_in_charge_second_division
                ).first()  

            if staff_grade:
 
    
                staff_grade.schools_grades_sections_id=sgs.id
                staff_grade.subject_id=subject_id
                staff_grade.staff_id=staff_id
                staff_grade.is_class_in_charge=bool(is_class_in_charge)
                staff_grade.class_in_charge_id=sgs1.id
                staff_grade.is_class_in_charge_second=bool(is_class_in_charge_second)
                staff_grade.is_transport_in_charge = bool(is_transport_in_charge)
                staff_grade.class_in_charge_second_id=sgs2.id
                staff_grade.transport_id=transport_id
                db.session.commit()

        # Handle Add
        else:
            print("222222222222222222222222222222")
            for grade_id, division_id, subject_id in zip(grades_list, divisions_list, subjects_list):
                sgs = SchoolsGradesSections.query.filter_by(
                    school_id=school_id,
                    grade_id=grade_id,
                    section_id=division_id
                ).first()

                if not sgs:
                    return jsonify({"error": "Invalid grade or division selection"}), 400
                sgs1 = SchoolsGradesSections.query.filter_by(
                    school_id=school_id,
                    grade_id=class_in_charge_grade,
                    section_id=class_in_charge_division
                ).first()
                sgs2 = SchoolsGradesSections.query.filter_by(
                    school_id=school_id,
                    grade_id=class_in_charge_second_grade,
                    section_id=class_in_charge_second_division
                ).first()   
          
                new_staff_grade = StaffsGrades(
                    schools_grades_sections_id=sgs.id,
                    subject_id=subject_id,
                    staff_id=staff_id,
                    is_class_in_charge=is_class_in_charge,
                    class_in_charge_id=sgs1.id,
                    is_class_in_charge_second=is_class_in_charge_second,
                    is_transport_in_charge=is_transport_in_charge,
                    class_in_charge_second_id=sgs2.id,
                    transport_id=transport_id
                )
                db.session.add(new_staff_grade)
                

        db.session.commit()

        return redirect(url_for('staffs_grades_list'))



    # Render the form with the existing data if editing
    # Prepare rows for edit form (if editing)
    rows = []
    if staff_grade:
        rows = [
            {
                "subject_id": sg.subject_id,
                "grade_id": sg.schools_grades_sections.grade_id,
                "division_id": sg.schools_grades_sections.section_id,
            }
           # for sg in StaffsGrades.query.filter_by(staff_id=staff_grade.staff_id).all()
           for sg in StaffsGrades.query.filter_by(id=id).all()
        ]
    print("aaaaaaaaaaaaaaaaaaaaaaaa00",rows)
    return render_template(
        'staffs_grades_form.html',
        staffs_grades=staff_grade,
        rows=rows,
        staffs=staffs,
        grades=grades,
        divisions=divisions,
        subjects=subjects,
        transports=transports
    )


@app.route('/staff_assignment/delete/<int:id>', methods=['POST'])
def delete_staffs_grades(id):
    """Delete a Staff Grade entry."""
    staff_grade = StaffsGrades.query.get(id)
    if staff_grade:
        db.session.delete(staff_grade)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404



@app.route('/subjects', methods=['GET'])
def subjects_list():
    """Render the list page."""
    return render_template('subjects_list.html')


@app.route('/subjects/add', methods=['GET', 'POST'])
@app.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
def subjects_add_edit(id=None):
    """Add or Edit a Subject."""
    subject = Subject.query.get(id) if id else None
    school_id = session.get('school_id')  # School is taken from the session

    if request.method == 'POST':
        title = request.form['title']

        if subject:
            # Edit existing subject
            subject.title = title
        else:
            # Add a new subject
            subject = Subject(
                school_id=school_id,
                title=title
            )
            db.session.add(subject)

        db.session.commit()
        return redirect(url_for('subjects_list'))

    return render_template('subjects_form.html', subject=subject)


@app.route('/subjects/delete/<int:id>', methods=['POST'])
def subjects_delete(id):
    """Delete a Subject."""
    subject = Subject.query.get(id)
    if subject:
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Subject not found'}), 404


@app.route('/api/subjects', methods=['GET'])
def api_subjects_list():
    """API for fetching the subjects list."""
    school_id = session.get('school_id')  # Filter subjects by the current school
    subjects = Subject.query.filter_by(school_id=school_id).all()

    data = [
        {
            "id": subject.id,
            "title": subject.title,
            "school": subject.school.title if subject.school else "N/A",
        }
        for subject in subjects
    ]
    return jsonify({"data": data})

@app.route('/exam-marks', methods=['GET'])
def exam_marks():
    school_id = session.get('school_id')
    academic_years = AcademicYear.query.all()
    grades = Grade.query.join(SchoolsGradesSections, Grade.id == SchoolsGradesSections.grade_id).filter(
        SchoolsGradesSections.school_id == school_id).all()
    sections = Section.query.join(SchoolsGradesSections, Section.id == SchoolsGradesSections.section_id).filter(
        SchoolsGradesSections.school_id == school_id).all()
    subjects = Subject.query.filter_by(school_id=school_id).all()

    return render_template('exam_marks.html', academic_years=academic_years, grades=grades, sections=sections,
                           subjects=subjects, terms=['First', 'Second', 'Third'])


@app.route('/exam-marks/students', methods=['POST'])
def get_students_marks():
    school_id = session.get('school_id')
    grade_id = request.form.get('grade_id')
    section_id = request.form.get('section_id')
    academic_year_id = request.form.get('academic_year_id')
    term = request.form.get('term')
    subject_id = request.form.get('subject_id')

    # Fetch the appropriate SchoolsGradesSections entry
    schools_grades_section = SchoolsGradesSections.query.filter_by(
        school_id=school_id,
        grade_id=grade_id,
        section_id=section_id,
        academic_year_id=academic_year_id
    ).first()

    if not schools_grades_section:
        return jsonify([])

    # Query to fetch students and marks
    query = db.session.query(
        Student.id.label("id"),
        Student.first_name.label("first_name"),
        Student.last_name.label("last_name"),
        ExamMarkDetails.marks_obtained.label("marks_obtained"),
        ExamMarkDetails.marks_out_of.label("marks_out_of"),
        ExamMarkDetails.weightage.label("weightage"),
    ).join(
        SchoolStudent, SchoolStudent.student_id == Student.id
    ).join(
        SchoolsGradesSections, SchoolsGradesSections.id == SchoolStudent.school_grade_section_id
    ).outerjoin(
        ExamMarks, (ExamMarks.student_id == Student.id) &
                   (ExamMarks.subject_id == subject_id) &
                   (ExamMarks.term == term)
    ).outerjoin(
        ExamMarkDetails, ExamMarkDetails.exam_mark_id == ExamMarks.id
    ).filter(
        SchoolsGradesSections.id == schools_grades_section.id
    )

    # Fetch the students
    students = query.all()
    marks_out_of = None
    weightage = None
    for student in students:
        if student.marks_out_of is not None:
            marks_out_of = student.marks_out_of
        if student.weightage is not None:
            weightage = student.weightage
        if marks_out_of and weightage:
            break
    # Prepare the response data
    students_data = []
    for student in students:
        students_data.append({
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "marks_obtained": student.marks_obtained if student.marks_obtained is not None else "",
            "marks_out_of": student.marks_out_of if student.marks_out_of is not None else "",
            "weightage": student.weightage if student.weightage is not None else "",
        })

    return jsonify({
        "students": students_data,
        "marks_out_of": marks_out_of if marks_out_of is not None else "",
        "weightage": weightage if weightage is not None else ""
    })



@app.route('/exam-marks/save', methods=['POST'])
def save_exam_marks():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    term = data.get('term')
    subject_id = data.get('subject_id')
    marks_out_of = data.get('marks_out_of')
    weightage = data.get('weightage')
    students = data.get('students', [])

    for student in students:
        student_id = student.get('id')
        marks_obtained = student.get('marks_obtained')

        exam_mark = ExamMarks.query.filter_by(term=term, student_id=student_id, subject_id=subject_id).first()
        if not exam_mark:
            exam_mark = ExamMarks(term=term, student_id=student_id, subject_id=subject_id, staff_id=session['user_id'])
            db.session.add(exam_mark)
            db.session.commit()

        exam_mark_detail = ExamMarkDetails.query.filter_by(
            exam_mark_id=exam_mark.id
        ).first()

        if exam_mark_detail:
            exam_mark_detail.marks_out_of = marks_out_of
            exam_mark_detail.weightage = weightage
            exam_mark_detail.marks_obtained = marks_obtained
        else:
            exam_mark_detail = ExamMarkDetails(
                exam_mark_id=exam_mark.id, marks_out_of=marks_out_of, weightage=weightage, marks_obtained=marks_obtained
            )
            db.session.add(exam_mark_detail)

    db.session.commit()
    return jsonify({"message": "Marks saved successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
