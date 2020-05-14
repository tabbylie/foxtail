from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import LoginForm, SignUpForm
from app.models import User, Products
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

@app.route('/products/customize/Website')
def website():
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

@app.route('/products/customize/Basic Desktop App')
def basic_desktop_app():
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

@app.route('/products/customize/Complex Desktop App')
def complex_desktop_app():
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

@app.route('/products/customize/Concept Design')
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

@app.route('/account/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)

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