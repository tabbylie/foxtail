from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import LoginForm, SignUpForm, CancelForm, BasicAppForm, ComplexAppForm, FrontEndForm, DatabaseForm, CMSForm, CDForm, SupportForm, AddProductsForm, DelProductsForm
from app.models import User, Products, Orders
from app.email import send_mail
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import os
import io
import numpy as np

@app.route('/')
@app.route('/index')
def index():
	basic_app = Products.query.filter_by(name="Basic Desktop App").first()
	front_end = Products.query.filter_by(name="Front End").first()
	database = Products.query.filter_by(name="Database").first()
	return render_template('index.html', title="Home", products=[basic_app, front_end, database])

@app.route('/products')
def products():
	product = Products.query.all()
	return render_template('products.html', title="Products", products=product)

@app.route('/customize/Front End', methods=['GET', 'POST'])
@login_required
def front_end():
	form = FrontEndForm(request.form)
	print(f'{form.validate_on_submit()}')
	if request.method == 'POST' and form.validate():
		user = User.query.filter_by(username=current_user.username).first_or_404()
		order = Orders(order_name=form.order_name.data, order_desc=form.order_description.data, author=user)
		db.session.add(order)
		db.session.commit()
		files = request.files.getlist(form.design_or_no.name)
		attachments = []
		for file in files:
			attachments.append(file.stream.read())
		send_mail(form.order_name.data, current_user.email, ['officialfoxtail@gmail.com'], f"Client Email: {current_user.email}\ndescription of project: {form.order_description.data}", None, attachments)
		return redirect('/success')
	return render_template('frontend.html', title='Front End', form=form)

@app.route('/customize/Basic Desktop App', methods=['GET', 'POST'])
@login_required
def basic_desktop_app():
	form = BasicAppForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first_or_404()
		order = Orders(order_name=form.order_name.data, order_desc=form.order_description.data, author=user)
		db.session.add(order)
		db.session.commit()
		send_mail(form.order_name.data, current_user.email, ['officialfoxtail@gmail.com'], f"Client Email: {current_user.email}\nDescription of project: {form.order_description.data}\nExamples: {form.order_examps.data}")
		return redirect('/success')
	return render_template('basicapp.html', title='Basic App', form=form)

@app.route('/customize/Complex Desktop App', methods=['GET', 'POST'])
@login_required
def complex_desktop_app():
	form = ComplexAppForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first_or_404()
		order = Orders(order_name=form.order_name.data, order_desc=form.order_description.data, author=user)
		db.session.add(order)
		db.session.commit()
		send_mail(form.order_name.data, current_user.email, ['officialfoxtail@gmail.com'], f"Client Email: {current_user.email}\nDescription of project: {form.order_description.data}\nExamples: {form.order_examps.data}")
		return redirect('/success')
	return render_template('complexapp.html', title='Complex App', form=form)

@app.route('/customize/Concept Design', methods=['GET', 'POST'])
@login_required
def Concept_Design():
	form = CDForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first_or_404()
		order = Orders(order_name=form.order_name.data, order_desc=form.order_description.data, author=user)
		db.session.add(order)
		db.session.commit()
		files = request.files.getlist(form.order_reference.name)
		attachments = []
		for file in files:
			attachments.append(file.stream.read())
		send_mail(form.order_name.data, current_user.email, ['cierraccontact@gmail.com'], f"Client Email: {current_user.email}\nDescription of project: {form.order_description.data}", None, attachments)
		# time.sleep(80)
		return redirect('/success')
	return render_template('concept.html', title="Concept Design", form=form)

@app.route('/customize/Database', methods=['GET', 'POST'])
@login_required
def database():
	form = DatabaseForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first_or_404()
		order = Orders(order_name=form.order_name.data, order_desc=form.order_description.data, author=user)
		db.session.add(order)
		db.session.commit()
		send_mail(form.order_name.data, current_user.email, ['officialfoxtail@gmail.com'], f"Client Email: {current_user.email}\ndescription of database: {form.order_description.data}")
		return redirect('/success')
	return render_template('database.html', title='Database', form=form)

@app.route('/customize/Content Management systems', methods=['GET', 'POST'])
@login_required
def CMS():
	form = CMSForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first_or_404()
		order = Orders(order_name=form.order_name.data, order_desc=form.order_description.data, author=user)
		db.session.add(order)
		db.session.commit()
		send_mail(form.order_name.data, current_user.email, ['officialfoxtail@gmail.com'], f"Client Email: {current_user.email}\npurpose of CMS: {form.order_description.data}")
		redirect('/success')
	return render_template('cms.html', title='CMS', form=form)


@app.route('/success')
def success():
	return '''
	<html>
		<head>
			<title>FOXTAIL | Success</title>
		</title>
		<body>
			<h1 style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">Your order has been placed!<br>Click <a href="/">here</a> to go to homepage</h1>
		</body>
	</html>
	'''

@app.route('/account/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			flash('[Invalid username]')
			return redirect('/account/login')
		if not user.check_password(form.password.data):
			flash('[Invalid password]')
			return redirect('/account/login')
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = '/'
		return redirect(next_page)
	return render_template('login.html', title="login", form=form)

@app.route('/account/logout')
def logout():
	logout_user()
	return redirect('/')

@app.route('/account/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect('/')
	form = SignUpForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect('/account/login')
	return render_template('signup.html', title="sign up", form=form)

@app.route('/account/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	form = CancelForm()
	if form.validate_on_submit():
		order = user.orders.filter_by(order_name=form.confirm.data).first_or_404()
		order.order_flag = 'cancelled'
		db.session.add(order)
		db.session.commit()
		send_mail(f"{form.confirm.data} cancelled", current_user.email, ['officialfoxtail@gmail.com'], f"{form.confirm.data} has been cancelled")
	ordered = user.orders.filter_by(order_flag='open')
	cancels = user.orders.filter_by(order_flag='cancelled')
	completed = user.orders.filter_by(order_flag='completed')

	return render_template('user.html', user=user, opens=ordered, cancels=cancels, completed=completed, form=form)

@app.route('/service', methods=['GET', 'POST'])
def support():
	form = SupportForm(request.form)
	if request.method == 'POST' and form.validate():
		send_mail('Issue!', current_user.email, ['officialfoxtail@gmail.com'], f"Issue: {form.issue.data}")
		flash(f'Your issue has been sent, thank you {current_user.username}')
		return redirect('/service')
	return render_template('support.html', title="Support", form=form)

@app.route('/about_the_devs')
def ATD():
	return render_template('about_the_devs.html', title='about the devs')

@app.route('/terms of service')
def tos():
	return render_template('tos.html', title="Terms of Service")

@app.route('/add_products', methods=['GET', 'POST'])
def add():
	form = AddProductsForm()
	if request.method == 'POST' and form.validate():
		product = Products(name=form.name.data, desc=form.desc.data, price=form.price.data)
		db.session.add(product)
		db.session.commit()
		return redirect('/add_products')
	return render_template('add_products.html', name="add products", form=form)

@app.route('/del_products', methods=['GET', 'POST'])
def del_products():
	form = DelProductsForm()
	if request.method == 'POST' and form.validate():
		Product = Products.query.filter_by(name=form.name.data).first_or_404()
		db.session.delete(Product)
		db.session.commit()
		return redirect('/del_products')
	return render_template('delete_products.html', name="delete products", form=form)