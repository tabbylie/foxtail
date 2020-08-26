from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import LoginForm, SignUpForm, CancelForm, BasicAppForm, ComplexAppForm, FrontEndForm, DatabaseForm, CMSForm, CDForm, SupportForm, ProductsFormAdmin, OrdersFormAdmin, EditForm
from app.models import User, Products, Orders
from app.email import send_mail
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
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
		send_mail(form.order_name.data, current_user.email, ['officialfoxtail@gmail.com'], f"Client Email: {current_user.email}\nName of project: {form.order_name.data}\nDescription of project: {form.order_description.data}\nExamples: {form.order_examps.data}")
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
	cancelform = CancelForm(prefix="a")
	editform = EditForm(request.form, prefix="b")
	if current_user.email not in ['dyoung8765@gmail.com', 'officialfoxtail@gmail.com', '']: 
		if cancelform.submit.data and cancelform.validate():
			order = user.orders.filter_by(order_name=cancelform.confirm.data).first_or_404()
			order.order_flag = 'cancelled'
			db.session.add(order)
			db.session.commit()
			send_mail(f"{cancelform.confirm.data} cancelled", current_user.email, ['officialfoxtail@gmail.com'], f"{cancelform.confirm.data} has been cancelled")

		if editform.submit2.data and editform.validate():
			if editform.name.data:
				user.username = editform.name.data
			if editform.profileimg.data:
				file = request.files.get(editform.profileimg.name)
				filename = secure_filename(file.filename)

				file.save(app.config['UPLOAD_FOLDER'] + filename)

				
				user.profile_img = '/static/profile_imgs/' + filename
				db.session.add(user)
				db.session.commit()

		ordered = user.orders.filter_by(order_flag='open')
		cancels = user.orders.filter_by(order_flag='cancelled')
		completed = user.orders.filter_by(order_flag='completed')

		return render_template('user.html', user=user, opens=ordered, cancels=cancels, completed=completed, cancelform=cancelform, editform=editform, isAdmin=False)
	else:
		if cancelform.submit.data and cancelform.validate():
			order = user.orders.filter_by(order_name=cancelform.confirm.data).first_or_404()
			order.order_flag = 'cancelled'
			db.session.add(order)
			db.session.commit()
			send_mail(f"{cancelform.confirm.data} cancelled", current_user.email, ['officialfoxtail@gmail.com'], f"{cancelform.confirm.data} has been cancelled")
		if editform.submit2.data and editform.validate():
			if editform.name.data:
				user.username = editform.name.data
			print(editform.profileimg.data)
			if editform.profileimg.data:
				file = request.files.get(editform.profileimg.name)
				filename = secure_filename(file.filename)

				file.save(app.config['UPLOAD_FOLDER'] + filename)

				user.profile_img = '/static/profile_imgs/' + filename
				db.session.add(user)
				db.session.commit()
				print(user.profile_img)
		ordered = user.orders.filter_by(order_flag='open')
		cancels = user.orders.filter_by(order_flag='cancelled')
		completed = user.orders.filter_by(order_flag='completed')

		return render_template('user.html', user=user, opens=ordered, cancels=cancels, completed=completed, cancel_form=cancelform, edit_form=editform, isAdmin=True)

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

@app.route('/termsofservice')
def tos():
	return render_template('tos.html', title="Terms of Service")

@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
	print(current_user.email)
	if current_user.email in ['dyoung8765@gmail.com', 'officialfoxtail@gmail.com']:
		productsform = ProductsFormAdmin()
		ordersform = OrdersFormAdmin()
		if productsform.submit1.data and productsform.validate():
			if productsform.type_.data == 'list_':
				products = Products.query.all()
				arr = []
				for product in products:
					arr.append(product)
				return render_template('admin_panel.html', title="Admin Panel", products=productsform, products_arr=arr, orders=ordersform)
			if productsform.type_.data == 'add_':
				try:
					int(productsform.price.data)
				except:
					return render_template('admin_panel.html', title='Admin Panel', products=productsform, products_arr=[f'Error! {productsform.price.data} is not an integer!'], orders=ordersform)
				product = Products(name=productsform.name.data, desc=productsform.desc.data, price=int(productsform.price.data))
				db.session.add(product)
				db.session.commit()
				return redirect('/admin_panel')
			if productsform.type_.data == 'del_':
				Product = Products.query.filter_by(name=productsform.name.data).first()
				if Product != None:
					db.session.delete(Product)
					db.session.commit()
					return redirect('/admin_panel')
				else:
					return render_template('admin_panel.html', title='Admin Panel', products=productsform, products_arr=[f'Error! {productsform.name.data} does not exist'], orders=ordersform)
			
		if ordersform.submit2.data and ordersform.validate():
			if ordersform.types.data == 'list':
				orders = Orders.query.all()
				arr = []
				for order in orders:
					arr.append(order)
				return render_template('admin_panel.html', title="Admin Panel", products=productsform, orders=ordersform, orders_arr=arr)
			if ordersform.types.data == 'del':
				order = Orders.query.filter_by(order_name=ordersform.name.data).first()
				if order != None:
					db.session.delete(order)
					db.session.commit()
					return redirect('/admin_panel')
				else:
					return render_template('admin_panel.html', title='Admin Panel', products=productsform, orders_arr=[f'Error! {ordersform.name.data} does not exist'], orders=ordersform)
			if ordersform.types.data == 'complete':
				order = Orders.query.filter_by(order_name=ordersform.name.data).first()
				if order != None:
					order.order_flag = 'completed'
					db.session.add(order)
					db.session.commit()
				else:
					return render_template('admin_panel.html', title='Admin Panel', products=productsform, orders_arr=[f'Error! {ordersform.name.data} does not exist'], orders=ordersform)

		return render_template('admin_panel.html', title="Admin Panel", products=productsform, orders=ordersform)
	else:
		return render_template('404.html'), 404