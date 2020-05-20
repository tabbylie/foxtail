from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import LoginForm, SignUpForm, CancelForm, BasicAppForm, ComplexAppForm, FrontEndForm, DatabaseForm, CMSForm
from app.models import User, Products, Orders
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title="Home")

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
		print('yes')
		db.session.add(order)
		db.session.commit()
		print('commited')
		return redirect('/success')
	return render_template('frontend.html', title='Front End', form=form)

@app.route('/customize/Basic Desktop App', methods=['GET', 'POST'])
@login_required
def basic_desktop_app():
	form = BasicAppForm()
	if form.validate_on_submit():
		order = Order(order_name=form.order_name.data, order_desc=form.order_description.data)
		db.session.add(order)
		db.session.commit()
		redirect('/success')
	return render_template('basicapp.html', title='Basic App', form=form)

@app.route('/customize/Complex Desktop App', methods=['GET', 'POST'])
@login_required
def complex_desktop_app():
	form = ComplexAppForm()
	if form.validate_on_submit():
		order = Order(order_name=form.order_name.data, order_desc=form.order_description.data)
		db.session.add(order)
		db.session.commit()
		redirect('/success')
	return render_template('complexapp.html', title='Complex App', form=form)

@app.route('/customize/Concept Design', methods=['GET', 'POST'])
@login_required
def Concept_Design():
	return '''
	<html>
		<head>
			<title>FOXTAIL | ERROR</title>
		</title>
		<body>
			<center>
				<h1 style="color: #ff0000">404</h1>
				<p>File not Found</p>
				<a href="/">Go Back</a>
			<center>
		</body>
	</html>
	'''

@app.route('/customize/Database', methods=['GET', 'POST'])
@login_required
def database():
	form = DatabaseForm()
	if form.validate_on_submit():
		order = Order(order_name=form.order_name.data, order_desc=form.order_description.data)
		db.session.add(order)
		db.session.commit()
		redirect('/success')
	return render_template('database.html', title='Database', form=form)

@app.route('/customize/Content Management systems', methods=['GET', 'POST'])
@login_required
def CMS():
	form = CMSForm()
	if form.validate_on_submit():
		order = Order(order_name=form.order_name.data, order_desc=form.order_description.data)
		db.session.add(order)
		db.session.commit()
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
		flash(f"Welcome, {form.username.data}! You've been registered!")
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
	ordered = user.orders.filter_by(order_flag='open')
	cancels = user.orders.filter_by(order_flag='cancelled')

	return render_template('user.html', user=user, opens=ordered, cancels=cancels, form=form)

@app.route('/termsofservice')
def terms_of_service():
	return '''
	<html>
		<head>
			<title>FOXTAIL | ERROR</title>
		</title>
		<body>
			<center>
				<h1 style="color: #ff0000">404</h1>
				<p>File not Found</p>
				<a href="/">Go Back</a>
			<center>
		</body>
	</html>
	'''

@app.route('/service')
def service():
	return '''
	<html>
		<head>
			<title>FOXTAIL | ERROR</title>
		</title>
		<body>
			<center>
				<h1 style="color: #ff0000">404</h1>
				<p>File not Found</p>
				<a href="/">Go Back</a>
			<center>
		</body>
	</html>
	'''

@app.route('/aboutus')
def aboutus():
	return '''
	<html>
		<head>
			<title>FOXTAIL | ERROR</title>
		</title>
		<body>
			<center>
				<h1 style="color: #ff0000">404</h1>
				<p>File not Found</p>
				<a href="/">Go Back</a>
			<center>
		</body>
	</html>
	'''

@app.route('/about_the_devs')
def ATD():
	return render_template('about_the_devs.html', title='about the devs')