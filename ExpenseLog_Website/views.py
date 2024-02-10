from flask import Blueprint, render_template,request ,flash, jsonify, redirect, url_for
from flask_login import  login_required,current_user
from .models import Entry, Category
from . import db
import json
from datetime import datetime, date
from decimal import Decimal


views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    category = Category.query.first()
    if not category:
        categoryItemList = ['Food','Travel']
        for itemList in categoryItemList:
            addtolist = Category(categoryType = itemList)
            db.session.add(addtolist)
            db.session.commit()
    return render_template("home.html",user=current_user)

@views.route('/expense_entry', methods=['GET','POST'])
@login_required
def expense_entry():
    categorylist = Category.query.all()
    todayDate = date.today() 
    if request.method == 'POST':
        dateChosen = datetime.strptime(
                     request.form.get('date'),
                     '%Y-%m-%d')
        description = request.form.get('description')
        categorySelected = request.form.get('categorySelection')
        category = Category.query.filter_by(categoryType=categorySelected).first()
        amount = float(request.form.get('amount'))*100

        if len(description)< 1:
            flash('Description is too short', category='error')
        elif amount <= 0:
            flash('Amount should be more than 0', category='error')
        else:
            new_entry = Entry(date=dateChosen,description=description,category=category, amount=amount,user_id=current_user.id)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry added',category='success')
    return render_template("expense_entry.html",user=current_user,categorylist=categorylist,todayDate=todayDate)

@views.route('/add-category', methods=['POST'])
@login_required
def add_category():
    #if request.method == 'POST':
    categoryentered = request.form.get('category')
    new_entry = Category(categoryType = categoryentered)
    db.session.add(new_entry)
    db.session.commit()
    flash('New category added',category='success')

    categorylist = Category.query.all()
    return render_template("expense_entry.html",user=current_user,categorylist=categorylist)

@views.route('/delete-entry', methods=['POST'])
@login_required
def delete_entry():
    entry = json.loads(request.data)
    entryId = entry['entryId']
    print(entryId)
    entry = Entry.query.filter_by(id = entryId).first()
    print(entry)
    if entry:
        if entry.user_id == current_user.id:
            db.session.delete(entry)
            db.session.commit()
            flash('Entry deleted!',category='success')
    return jsonify({})

# @views.route('/delete_category', methods=['GET','POST'])
# @views.route('/delete_category/<action>/<item_id>', methods=['GET', 'POST'])
# @login_required
# def delete_category(action=None, item_id=None):

#     categorylist = Category.query.all()

#     if request.method == "POST":
#         if action == 'delete':
#             # Get specific row user wants to delete
#             Category_row_to_delete = Category.query.get(item_id)

#             # Delete row
#             db.session.delete(Category_row_to_delete)
#             db.session.commit()
#             #delete_entry1()
#             categorylist = Category.query.all()
#             #return redirect(url_for('delete_category'))
#     return jsonify({})
    #return render_template("expense_entry.html",user=current_user,categorylist=categorylist)


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
       flash('Category deleted!',category='success')
   return jsonify({})