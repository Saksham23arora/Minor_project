from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)
current_Values = {}

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    global current_Values
    if request.method == 'POST':
        # implement send sms here
        pass
    #db.session.query(User).get(current_user.id).amount = 67   
    return render_template("home.html", user=current_user , data = db.session.query(User).get(current_user.id))

