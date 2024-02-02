from flask import Blueprint, render_template,request ,flash, jsonify
from flask_login import  login_required,current_user
from .models import Entry
from . import db
import json
from datetime import datetime
from decimal import Decimal


views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        desc = request.form.get('entry')

        if len(desc)< 1:
            flash('Description is too short', category='error')
        else:
            new_entry = Entry(description=desc,user_id=current_user.id)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry added',category='success')
    return render_template("home.html",user=current_user)

@views.route('/expense_entry', methods=['GET','POST'])
@login_required
def expense_entry():
    if request.method == 'POST':
        # date = request.form.get('date')
        date = datetime.strptime(
                     request.form.get('date'),
                     '%Y-%m-%d')
        description = request.form.get('description')
        amount = float(request.form.get('amount'))*100

        if len(description)< 1:
            flash('Description is too short', category='error')
        else:
            new_entry = Entry(date=date,description=description,amount=amount,user_id=current_user.id)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry added',category='success')
    return render_template("expense_entry.html",user=current_user)


@views.route('/delete-entry', methods=['POST'])
def delete_entry():
    entry = json.loads(request.data)
    entryId = entry['entryId']
    entry = Entry.query.get(entryId)
    if entry:
        if entry.user_id == current_user.id:
            db.session.delete(entry)
            db.session.commit()
            flash('Entry deleted!',category='success')
    return jsonify({})