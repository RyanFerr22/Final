from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150),unique = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    access_lvl = db.Column(db.Integer)
    events = db.relationship('Event')

class Admin(User):
     def __init__(self, username, email, password, access_lvl, admin_specific_attribute):
        super().__init__(username, email, password, access_lvl)
        self.admin_specific_attribute = admin_specific_attribute
        access_lvl = 2

     # Method to add a new student
     def add_student(self, student_username, student_email, student_password):
        new_student = User(username=student_username, email=student_email, password=student_password, access_lvl=0)
        db.session.add(new_student)
        db.session.commit()

     # Method to edit an existing student
     def edit_student(self, student_id, new_username, new_email):
        student = User.query.get(student_id)
        if student:
            student.username = new_username
            student.email = new_email
            db.session.commit()
        else:
            print("Student not found.")
    
     # Method to remove a student
     def remove_student(self, student_id):
        student = User.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
        else:
            print("Student not found.")
     
     # Course Management Methods
     def add_course(self, course_name, course_description):
        new_course = Course(name=course_name, description=course_description)
        db.session.add(new_course)
        db.session.commit()

     def edit_course(self, course_id, new_name, new_description):
        course = Course.query.get(course_id)
        if course:
            course.name = new_name
            course.description = new_description
            db.session.commit()
        else:
            print("Course not found.")

     def remove_course(self, course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
        else:
            print("Course not found.")

     def update_course_schedule(self, course_id, new_schedule):
        course = Course.query.get(course_id)
        if course:
            course.schedule = new_schedule
            db.session.commit()
        else:
            print("Course not found.")

     # Faculty Profile Management Methods
     def update_faculty_profile(self, faculty_id, new_contact_info, new_qualifications, new_teaching_assignments):
        faculty = User.query.get(faculty_id)
        if faculty:
            # Update contact information
            faculty.contact_info = new_contact_info
            # Update academic qualifications
            faculty.qualifications = new_qualifications
            # Update teaching assignments
            faculty.teaching_assignments = new_teaching_assignments
            db.session.commit()
        else:
            print("Faculty not found.")

         # Academic Event Scheduling Methods
     def schedule_event(self, event_name, event_type, event_date, event_time, event_location):
        new_event = AcademicEvent(name=event_name, type=event_type, date=event_date, time=event_time, location=event_location)
        db.session.add(new_event)
        db.session.commit()

     def update_event_schedule(self, event_id, new_date, new_time, new_location):
        event = AcademicEvent.query.get(event_id)
        if event:
            event.date = new_date
            event.time = new_time
            event.location = new_location
            db.session.commit()
        else:
            print("Event not found.")

class Faculty(User):
     def __init__(self, username, email, password, access_lvl, faculty_specific_attribute):
        super().__init__(username, email, password, access_lvl)
        self.faculty_specific_attribute = faculty_specific_attribute
        access_lvl = 1

     # Course Management Methods
     def access_course_materials(self, course_id):
        pass

     # Student Progress Tracking Methods
     def track_student_progress(self, student_id):
        pass

     # Assignment and Assessment Methods
     def create_assignment(self, course_id, assignment_name, assignment_description, due_date):
        pass

     def grade_assignment(self, assignment_id, student_id, grade):
        pass

class Student(User):
     def __init__(self, username, email, password, access_lvl, student_specific_attribute):
        super().__init__(username, email, password, access_lvl)
        self.student_specific_attribute = student_specific_attribute
        access_lvl = 0

     # Course Registration Methods
     def register_for_course(self, course_id):
        pass

     # Course Access Methods
     def access_course_materials(self, course_id):
        pass

     # Assignment Submission Methods
     def submit_assignment(self, assignment_id, submission):
        pass

     # Grade Viewing Methods
     def view_grades(self):
        pass












class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    schedule = db.Column(db.String(150))

class AcademicEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(150))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    location = db.Column(db.String(150))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_planner = db.Column(db.String(150), db.ForeignKey('user.id'))
    event_name = db.Column(db.String(150))
    event_type = db.Column(db.String(150))
    event_date = db.Column(db.Date)
    event_time = db.Column(db.Time)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grade = db.Column(db.Float)
    
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submission = db.Column(db.Text)
    submission_date = db.Column(db.DateTime)































    
class Stall(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    stall_x = db.Column(db.Integer)
    stall_y = db.Column(db.Integer)
    
class Layout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    layout_image = db.Column(db.String(150))
    
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    stall_id = db.Column(db.Integer, db.ForeignKey('stall.id'))
    item_name = db.Column(db.String(150))
    item_price = db.Column(db.Float)
    item_quantity = db.Column(db.Integer)