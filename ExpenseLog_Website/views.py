from flask import Blueprint, render_template,request ,flash, jsonify, redirect, url_for
from flask_login import  login_required,current_user
from .models import Entry, Category
from . import db
import json
from datetime import datetime, date
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from wtforms.fields import DateField,DateTimeField 


views = Blueprint('views',__name__)

categoryItemList = ['Food','Grocery','Utility','Travel']

def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True

class ExpenseEntryForm(FlaskForm):
    date = DateField('Transaction date', format= '%Y-%m-%d' )
    description = StringField('Description', validators=[InputRequired(), Length(min=4, max= 15, message="Description should be between 4 to 15 characters.")])
    category = SelectField('Category', choices=categoryItemList)
    amount = StringField('Amount', validators=[InputRequired(message="Enter a dollar amount.")])

    def validate_amount(form, field):
        if field.data:
            if not is_number(field.data):
                raise ValidationError('Enter valid dollar amount')

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    category = Category.query.first()
    if not category:
        for itemList in categoryItemList:
            addtolist = Category(categoryType = itemList)
            db.session.add(addtolist)
            db.session.commit()
    return render_template("home.html",user=current_user)

@views.route('/expense_entry', methods=['GET','POST'])
@login_required
def expense_entry():
    form = ExpenseEntryForm()
    todayDate = date.today() 
    form.category.choices = categoryItemList
    if request.form.get('btn') is not None:
        if form.validate_on_submit():
            #if request.method == 'POST':
            dateChosen = form.date.data #datetime.strptime(request.form.get('date'),'%Y-%m-%d')
            description = form.description.data #request.form.get('description')
            categorySelected = form.category.data #request.form.get('categorySelection')
            category = Category.query.filter_by(categoryType=categorySelected).first()
            amount = float(form.amount.data)*100 #float(request.form.get('amount'))*100

            if amount <= 0:
                flash('Amount should be more than 0', category='error')
            else:
                new_entry = Entry(date=dateChosen,description=description,category=category, amount=amount,user_id=current_user.id)
                db.session.add(new_entry)
                db.session.commit()
                flash('Entry added',category='success')
            
    categorylist = Category.query.all()
    return render_template("expense_entry.html",user=current_user,categorylist=categorylist,todayDate=todayDate, form=form,show_predictions_modal=True)

@views.route('/add-category', methods=['POST'])
@login_required
def add_category():
    #if request.method == 'POST':
    form = ExpenseEntryForm()
    categoryentered = request.form.get('newcategory')
    categoryItemList.append(categoryentered)
    form.category.choices = categoryItemList
    new_entry = Category(categoryType = categoryentered)
    db.session.add(new_entry)
    db.session.commit()
    flash('New category added',category='success')

    categorylist = Category.query.all()
    return render_template("expense_entry.html",user=current_user,categorylist=categorylist, form=form)

@views.route('/delete-entry', methods=['POST'])
@login_required
def delete_entry():
    entry = json.loads(request.data)
    entryId = entry['entryId']
    entry = Entry.query.filter_by(id = entryId).first()
    if entry:
        if entry.user_id == current_user.id:
            db.session.delete(entry)
            db.session.commit()
            flash('Entry deleted!',category='success')
    return jsonify({})

@views.route('/delete-category', methods=['POST'])
@login_required
def delete_category():
   category = json.loads(request.data)
   categoryId = category['categoryId']
   category = Category.query.get(categoryId)
   if category:
        #if category.user_id == current_user.id:
       db.session.delete(category)
       db.session.commit()
       categoryItemList.remove(category.categoryType)
       flash('Category deleted!',category='success')
   return jsonify({})