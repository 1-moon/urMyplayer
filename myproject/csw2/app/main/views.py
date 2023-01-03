from flask import render_template, redirect, url_for, request, flash,session, g,jsonify 
from flask_login import login_required, current_user,logout_user,login_user
from flask.globals import current_app
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PlayerForm
from .. import db
from ..models import Permission, User, Role, Player,Bid
from flask_admin import Admin
from ..decorators import admin_required, permission_required
from flask_admin.contrib.sqla import ModelView
# from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import exc
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import base64
import logging 



@main.route('/')   
def index(): 
    # logging 
    current_app.logger.info('index route request')
    return render_template('index.html')


def check_upload_file(form):
    fp= form.profile_pic.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(
        BASE_PATH, '..\static\images\\', secure_filename(filename))

    db_upload_path = '..\static\images\\' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

@main.route('/player_regi', methods=['GET','POST'])
@login_required
def player_regi():
    form = PlayerForm() # creation over form instance  
    if request.method == "POST" and form.validate_on_submit():
      db_file_path = check_upload_file(form)

      post = Player(         
                        profile_pic   = db_file_path,  
                        name          = form.name.data,
                        nationality   = form.nationality.data,
                        birth         = form.birth.data,
                        height        = form.height.data,
                        position      = form.position.data,
                        foot          = form.foot.data,
                        club          = form.club.data)

      db.session.add(post)
      db.session.commit()
      # saver.save(os.path.join(current_app.config['UPLOAD_FOLDER']), pic_name)
      flash(f'{form.name.data} has been successfully posted!', 'success')
      return redirect('/player_list')
    return render_template ('player_regi.html',  form=form)

@main.route('/<int:id>', methods=['GET','POST'])
def mark(id):
    markRelease = Player.query.get(id)
    if request.method == "POST":
        markRelease.status = True
        db.session.commit()
    return redirect(url_for('main.market'))

@main.route('/delete/<int:id>', methods=['GET','POST'])
def remove(id):
    retire_player = Player.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(retire_player)
        db.session.commit()
    flash('Your player has been successfully deleted!', 'success')  
    return redirect(url_for('main.player'))

@main.route('/player_list')
def player():
    page = request.args.get('page', type=int, default=1) # page
    player_list = Player.query.paginate(page=page, per_page=10)
    return render_template('player_list.html', player_list = player_list)

@main.route('/market', methods=['GET','POST'])
@login_required
def market():
    # If the status(boolean) is true, This function filter will display 
    # only the player who have transfer-listed
    transfer_list = Player.query.filter_by(status=True).all()
    # POST : new bid!!
    if request.method == "POST":
        club        = request.form.get('bid-club')
        bid_amount  = request.form.get('bid-sum')

        if len(club) < 1 or len(bid_amount) < 1:
            flash("omited club name.", category = "error")
        elif len(club) > 15:
            flash("club name is too long, word limit 15", category = "error")
        elif len(bid_amount) > 15:
            flash("the sum of bid is too big, number limit 15", category="error")
        else :            
           
            new_bid = Bid(
                            club      =club, 
                            bid_amount=bid_amount, 
                            user_id   =current_user.id) 

            db.session.add(new_bid)
            db.session.commit()

            flash("Bid placed!", category="success")
            return redirect(url_for('main.market')) 

    return render_template('market.html', transfer_list = transfer_list)


# delete bid 
@main.route('/delete-bid', methods=['POST'])
def delete_bid():
    # POST : bid delete
    if request.method == "POST":
        bid = request.get_json()
        bid_id = bid.get('bidId')

        select_bid = Bid.query.get(bid_id)
        if select_bid:
            if select_bid.user_id == current_user.id : 
                db.session.delete(select_bid)
                db.session.commit()

        return jsonify({})

# edit bid sum 
@main.route('/update-bid', methods=['PUT'])
def update_bid():
    # PUT : edit bid
    if request.method == "PUT":
        bid = request.get_json()
        bid_id = bid.get('bidId')
        club = bid.get('club')
        bid_amount = bid.get('bid_amount')

        select_bid = bid.query.get(bid_id)
        if select_bid:
            if select_bid.user_id == current_user.id : 
                select_bid.club = club
                select_bid.bid_amount = bid_amount
                db.session.commit()

        return jsonify({})


@main.route('/news')
def news():
        return render_template('news.html')

# ======================================User profile  
@main.route('/user/<username>')
def user(username):
    myPlayer= Player.query.filter_by(status=False).all()
    user = User.query.filter_by(username=username).first_or_404()    
    return render_template('user.html', user=user, myPlayer=myPlayer)

def check_upload_file2(form):
    fp= form.emblem.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(
        BASE_PATH, '..\static\images\\', secure_filename(filename))

    db_upload_path = '..\static\images\\' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

# User profile change 
# User can modify their own account 
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file2(form)

        current_user.emblem     = db_file_path
        current_user.league     = form.league.data
        current_user.stadium    = form.stadium.data
        current_user.capacity   = form.capacity.data
        current_user.location    = form.location.data
        current_user.manager    = form.manager.data
        current_user.founded    = form.founded.data
        current_user.telephone  = form.telephone.data


        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('profile changed.')
        return redirect(url_for('.user', username=current_user.username))

    # db_file_path     = current_user.emblem
    form.league.data     = current_user.league
    form.stadium.data    = current_user.stadium
    form.capacity.data   = current_user.capacity
    form.location.data    = current_user.location
    form.manager.data    = current_user.manager
    form.founded.data    = current_user.founded
    form.telephone.data  = current_user.telephone
    return render_template('edit_profile.html', form=form)

# admin profile modification 
# admin can modify anyone as well as oneself
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email      = form.email.data
        user.username   = form.username.data
        user.role       = Role.query.get(form.role.data)

        user.league     = form.league.data
        user.stadium    = form.stadium.data
        user.capacity   = form.capacity.data
        user.location    = form.location.data
        user.manager    = form.manager.data
        user.founded    = form.founded.data
        user.telephone  = form.telephone.data
        user.emblem     = form.emblem.data

        db.session.add(user)
        db.session.commit()
        flash('profile changed')
        return redirect(url_for('.user', username=user.username))

    form.email.data     = user.email
    form.username.data  = user.username
    form.role.data      = user.role_id

    form.league.data     = user.league
    form.stadium.data   = user.stadium
    form.capacity.data   = user.capacity
    form.location.data    = user.location
    form.manager.data   = user.manager
    form.founded.data  = user.founded
    form.telephone.data  = user.telephone
    form.emblem.data   = user.emblem
    return render_template('edit_profile_admin.html', form=form, user=user)
# ================================ end user profile
@main.route('/qNa')
def qAndA():
    # order by -> sort out inquiry result 
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('qNa.html', question_list = question_list)

@main.route('/detail/<int:question_id>/')
def detail(question_id):
    # 404 page will print out if we cannot find out the page 
    question = Question.query.get_or_404(question_id)
    return render_template('qNa_detail.html', question=question)
