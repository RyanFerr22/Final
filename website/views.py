import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import Event,Stall,Layout

UPLOAD_PATH = 'website\\layoutimages'
UPLOAD_FOLDER = 'layoutimages'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    action = request.form.get('action')
    if request.method == 'POST':
        
        if action == "CREATE AN EVENT":
            new_event = Event(event_planner=current_user.id)
            db.session.add(new_event)
            db.session.commit()
            session['currentEventId'] = new_event.id
            return redirect(url_for('views.add_event'))
        
        elif action == "DELETE AN EVENT":
            
            return redirect(url_for('auth.admin_signup'))
        
    
    return render_template("home.html",user=current_user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if current_user.access_lvl == 1 or current_user.access_lvl == 2:
        action = request.form.get('action')
        if request.method == 'POST':
            
            #region Files
            if action == "upload":
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                    return render_template("add_event.html", user=current_user)
                
                file = request.files['file']
                
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return render_template("add_event.html", user=current_user)
                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_PATH, filename))
                    session['currentFileName'] = filename
                    
                    new_layout = Layout(event_id=session['currentEventId'],layout_image = session['currentFileName'])
                    db.session.add(new_layout)
                    db.session.commit()
                    
                    return render_template("add_event.html",filename=filename,user=current_user, layoutfolder=UPLOAD_FOLDER)
            #endregion     
        
            if action == "CREATE A STALL":
                return render_template("add_event.html",filename=session['currentFileName'],user=current_user, layoutfolder=UPLOAD_FOLDER)
            
        return render_template("add_event.html", user=current_user)
    return redirect(url_for('views.home'))

@views.route('/add_stall', methods=['POST'])
@login_required        
def add_stall():
    data = request.json
    x = data["x"]
    y = data["y"]
    new_stall = Stall(event_id = session['currentEventId'], stall_x = x, stall_y = y)
    db.session.add(new_stall)
    db.session.commit()
    print("stall created successfully")
    return jsonify({"id": new_stall.id})

@views.route('/stalls', methods=['GET'])
@login_required
def get_stalls():
    stalls = Stall.query.filter_by(event_id = session['currentEventId'])
    data = []
    for stall in stalls:
        data.append({
            "id": stall.id,
            "event_id": stall.event_id,
            "x": stall.stall_x,
            "y": stall.stall_y})
  
    return jsonify(data)

@views.route('/next_event')
@login_required
def next_event():
    current_event_id = session.get('currentEventId')  # Get the ID of the current event
    if current_event_id is None:
        return 'Current event not set', 404

    # Query the database to find the next event based on ID
    next_event = Event.query.filter(Event.id > current_event_id).order_by(Event.id).first()
    
    if next_event is None:
        return 'No next event found', 404
    else:
        # Redirect the user to the page of the next event
        session['currentEventId'] = next_event.id
        return redirect(url_for('views.show_event', event_id=next_event.id))
