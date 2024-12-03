from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String, nullable=False)
    role_type = db.Column(db.String, nullable=False)  # Can be 'admin', 'staff', or 'student'
    is_active = db.Column(db.Boolean, default=True)
    
    
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    staff = db.relationship('Staff', backref='user', lazy='joined')
    roles = db.relationship('Role', secondary='user_roles', backref='users')
    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)    

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)    

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    syllabus = db.Column(db.String, nullable=True)  # E.g., CBSE, ICSE, State Board
    status = db.Column(db.Boolean, default=True)    

class AcademicYear(db.Model):
    __tablename__ = 'academic_years'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default=False)   
    

class SchoolSubscription(db.Model):
    __tablename__ = 'school_subscription'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'), nullable=True)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    no_of_students_subscription = db.Column(db.String, nullable=True)
    subscription_amount = db.Column(db.String, nullable=True)
    payment_status = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, default=True)
    subscription_date = db.Column(db.Date, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)

    school = db.relationship('School')
    subscription = db.relationship('Subscription')
    offer = db.relationship('Offer')
    academic_year = db.relationship('AcademicYear')    

class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String, nullable=False)
    menu_name = db.Column(db.String, nullable=False)
    module_link = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)  # Allow null for parent_id
    is_active = db.Column(db.Boolean, default=True)
    is_visible_in_app = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer)  # Allow null for parent_id

    parent = db.relationship('Module', remote_side=[id], backref=db.backref('children', lazy='dynamic'))

class SchoolSubscriptionModuleRolePermission(db.Model):
    __tablename__ = 'school_subscription_module_role_permission'

    id = db.Column(db.Integer, primary_key=True)
    school_subscription_id = db.Column(db.Integer, db.ForeignKey('school_subscription.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)

    school_subscription = db.relationship('SchoolSubscription')
    module = db.relationship('Module')
    role = db.relationship('Role')
    permission = db.relationship('Permission')        

class StaffType(db.Model):
    __tablename__ = 'staff_types'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)    

class Staff(db.Model):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    staff_type_id = db.Column(db.Integer, db.ForeignKey('staff_types.id'), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String, nullable=False)
    permanent_address = db.Column(db.String)
    communication_address = db.Column(db.String)
    blood_group = db.Column(db.String)
    qualification = db.Column(db.String)
    is_section_in_charge = db.Column(db.Boolean, default=False)
    section_details = db.Column(db.String)
    is_transport_in_charge = db.Column(db.Boolean, default=False)
    transport_details = db.Column(db.String)
    joining_date = db.Column(db.Date)
    relieving_date = db.Column(db.Date)
    relieving_comment = db.Column(db.String)
    status = db.Column(db.Boolean, default=True)

    school = db.relationship('School', backref='staffs')
    staff_type = db.relationship('StaffType', backref='staffs')

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    status = db.Column(db.Boolean, default=True)

    school = db.relationship('School', backref='clubs')




class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    student_code = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=True)
    aadhar_number = db.Column(db.String, nullable=True)
    photo = db.Column(db.String, nullable=True)
    date_of_admission = db.Column(db.Date, nullable=True)
    admission_number = db.Column(db.String, nullable=True)
    identification_mark = db.Column(db.String, nullable=True)
    interests = db.Column(db.String, nullable=True)
    hobbies = db.Column(db.String, nullable=True)
    student_email = db.Column(db.String, nullable=True)
    religion = db.Column(db.String, nullable=True)
    caste = db.Column(db.String, nullable=True)
    permanent_address = db.Column(db.String, nullable=True)
    communication_address = db.Column(db.String, nullable=True)
    mother_name = db.Column(db.String, nullable=True)
    father_name = db.Column(db.String, nullable=True)
    father_qualification = db.Column(db.String, nullable=True)
    mother_qualification = db.Column(db.String, nullable=True)
    father_occupation = db.Column(db.String, nullable=True)
    mother_occupation = db.Column(db.String, nullable=True)
    father_mobile = db.Column(db.String, nullable=True)
    mother_mobile = db.Column(db.String, nullable=True)
    father_email = db.Column(db.String, nullable=True)
    mother_email = db.Column(db.String, nullable=True)
    annual_income = db.Column(db.String, nullable=True)
    blood_group = db.Column(db.String, nullable=True)
    mother_tongue = db.Column(db.String, nullable=True)
    is_single_girl = db.Column(db.Boolean, default=False)
    is_minority = db.Column(db.Boolean, default=False)
    sibling_status = db.Column(db.Boolean, default=False)
    relieving_date = db.Column(db.Date, nullable=True)
    relieving_comment = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=True)

    # Relationships
    school = db.relationship('School', backref='students')  # Relates to the `schools` table

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.first_name} {self.last_name}, school_id={self.school_id})>"
