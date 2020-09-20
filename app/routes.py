from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import (
    LoginForm,
    SignUpForm,
    ResetPasswordForm,
    CancelForm,
    SupportForm,
    ProductsFormAdmin,
    OrdersFormAdmin,
    UsersFormAdmin,
    EditForm,
    CustomizeForm,
    ResetPasswordVerifiedForm,
)
from app.models import User, Products, Orders
from app.email import (
    send_mail,
    send_password_reset_email,
    send_email_verification_email,
)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
import os
import io
import numpy as np


@app.route("/")
@app.route("/index")
def index():
    basic_app = Products.query.filter_by(name="Basic Desktop App").first()
    front_end = Products.query.filter_by(name="Front End").first()
    database = Products.query.filter_by(name="Database").first()
    return render_template(
        "index.html", title="Home", products=[basic_app, front_end, database]
    )


@app.route("/products")
def products():
    product = Products.query.all()
    return render_template("products.html", title="Products", products=product)


@app.route("/customize/<product>", methods=["GET", "POST"])
@login_required
def customize_product(product):
    form = CustomizeForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=current_user.username).first()
        if not user:
            return render_template("403.html"), 403
        order = Orders(
            order_name=form.order_name.data,
            order_desc=form.order_description.data,
            author=user,
        )
        db.session.add(order)
        db.session.commit()
        files = request.files.getlist(form.order_reference.name)
        if len(files) != 0:
            attachments = []
            for file in files:
                attachments.append(file.stream.read())
        else:
            attachments = None
        send_mail(
            form.order_name.data,
            current_user.email,
            ["officialfoxtail@gmail.com"],
            f"Client Email: {current_user.email}\ndescription of project: {form.order_description.data}",
            None,
            attachments,
        )
        return redirect("/success")
    return render_template(
        "customize_product.html",
        title=product,
        form=form,
    )


@app.route("/success")
def success():
    return """
	<html>
		<head>
			<title>FOXTAIL | Success</title>
		</title>
		<body>
			<h1 style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">Your order has been placed!<br>Click <a href="/">here</a> to go to homepage</h1>
			<script>
				setTimeout(() => {
					window.location.href = '/';
				}, 2000);
			</script>
		</body>
	</html>
	"""


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect("/")
    form = ResetPasswordForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for instructions to reset your password")
        return redirect("/account/login")
    return render_template("reset_password.html", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password_verify(token):
    user = User.verify_reset_token(token)
    if not user:
        return render_template("reset_token_error.html", title="Error!")
    form = ResetPasswordVerifiedForm()
    if form.validate_on_submit():
        user.set_password(form.newPass.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template(
        "reset_password_verified.html", title="Reset Password", form=form
    )


@app.route("/account/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            return render_template(
                "login.html",
                title="login",
                form=form,
                user_error="Invalid username",
            )

        if not user.isVerified:
            return render_template(
                "login.html",
                title="login",
                form=form,
                user_error="Invalid username",
                pass_error="Invalid password",
            )

        if not user.check_password(form.password.data):
            return render_template(
                "login.html", title="login", form=form, pass_error="Invalid password"
            )
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = "/"
        return redirect(next_page)
    return render_template("login.html", title="login", form=form)


@app.route("/account/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/account/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        send_email_verification_email(user)

        return redirect("/account/login")
    return render_template("signup.html", title="sign up", form=form)


@app.route("/email/<token>")
def validate_email(token):
    user = User.verify_reset_token(token)
    if not user:
        return render_template("reset_token_error.html", title="Error!")
    user.isVerified = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/account/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    cancelform = CancelForm(prefix="a")
    editform = EditForm(request.form, prefix="b")

    if cancelform.submit.data and cancelform.validate():
        order = user.orders.filter_by(order_name=cancelform.confirm.data).first_or_404()
        order.order_flag = "cancelled"
        db.session.add(order)
        db.session.commit()
        send_mail(
            f"{cancelform.confirm.data} cancelled",
            current_user.email,
            ["officialfoxtail@gmail.com"],
            f"{cancelform.confirm.data} has been cancelled",
        )

    if editform.submit2.data and editform.validate():
        file = request.files.get(editform.profileimg.name)
        print(file)
        if file:
            filename = secure_filename(file.filename)

            file_extensions = [".jpg", ".jpeg", ".png"]
            good = False
            for file_extension in file_extensions:
                if filename.endswith(file_extension):
                    good = True

            if good:
                file.save(app.config["UPLOAD_FOLDER"] + filename)

                user.profile_img = "/static/profile_imgs/" + filename
                db.session.add(user)
                db.session.commit()
            else:
                flash("Not an image!")

        if editform.name.data:
            user_exists = User.query.filter_by(username=editform.name.data).first()
            if not user_exists:
                user.username = editform.name.data
                db.session.add(user)
                db.session.commit()
                return redirect(f"/account/{user.username}")
            else:
                flash("Username exists!")
        else:
            print("no!")
    ordered = user.orders.filter_by(order_flag="open")
    cancels = user.orders.filter_by(order_flag="cancelled")
    completed = user.orders.filter_by(order_flag="completed")

    if current_user.email in [
        "dyoung8765@gmail.com",
        "officialfoxtail@gmail.com",
        "deadbot247@gmail.com",
    ]:
        return render_template(
            "user.html",
            user=user,
            opens=ordered,
            cancels=cancels,
            completed=completed,
            cancel_form=cancelform,
            edit_form=editform,
            isAdmin=True,
        )
    else:
        return render_template(
            "user.html",
            user=user,
            opens=ordered,
            cancels=cancels,
            completed=completed,
            cancel_form=cancelform,
            edit_form=editform,
            isAdmin=False,
        )


@app.route("/service", methods=["GET", "POST"])
def support():
    form = SupportForm(request.form)
    if request.method == "POST" and form.validate():
        send_mail(
            "Issue!",
            current_user.email,
            ["officialfoxtail@gmail.com"],
            f"Issue: {form.issue.data}",
        )
        flash(f"Your issue has been sent, thank you {current_user.username}")
        return redirect("/service")
    return render_template("support.html", title="Support", form=form)


@app.route("/about_the_devs")
def ATD():
    return render_template("about_the_devs.html", title="about the devs")


@app.route("/termsofservice")
def tos():
    return render_template("tos.html", title="Terms of Service")


@app.route("/admin_panel", methods=["GET", "POST"])
def admin_panel():
    if current_user.email in [
        "dyoung8765@gmail.com",
        "officialfoxtail@gmail.com",
        "deadbot247@gmail.com",
    ]:
        productsform = ProductsFormAdmin()
        ordersform = OrdersFormAdmin()
        usersform = UsersFormAdmin()
        if productsform.submit1.data and productsform.validate():
            if productsform.types.data == "list":
                products = Products.query.all()
                arr = []
                for product in products:
                    arr.append(product)
                return render_template(
                    "admin_panel.html",
                    title="Admin Panel",
                    products=productsform,
                    products_arr=arr,
                    orders=ordersform,
                    users=usersform,
                )
            if productsform.types.data == "add":
                try:
                    int(productsform.price.data)
                except:
                    return render_template(
                        "admin_panel.html",
                        title="Admin Panel",
                        products=productsform,
                        products_arr=[
                            f"Error! {productsform.price.data} is not an integer!"
                        ],
                        orders=ordersform,
                    )
                product = Products(
                    name=productsform.name.data,
                    desc=productsform.desc.data,
                    price=int(productsform.price.data),
                )
                db.session.add(product)
                db.session.commit()
                return redirect("/admin_panel")
            if productsform.types.data == "del":
                Product = Products.query.filter_by(name=productsform.name.data).first()
                if Product != None:
                    db.session.delete(Product)
                    db.session.commit()
                    return redirect("/admin_panel")
                else:
                    return render_template(
                        "admin_panel.html",
                        title="Admin Panel",
                        products=productsform,
                        products_arr=[
                            f"Error! {productsform.name.data} does not exist"
                        ],
                        orders=ordersform,
                        users=usersform,
                    )

        if ordersform.submit2.data and ordersform.validate():
            if ordersform.types.data == "list":
                orders = Orders.query.all()
                arr = []
                for order in orders:
                    arr.append(order)
                return render_template(
                    "admin_panel.html",
                    title="Admin Panel",
                    products=productsform,
                    orders=ordersform,
                    orders_arr=arr,
                    users=usersform,
                )
            if ordersform.types.data == "del":
                order = Orders.query.filter_by(
                    order_name=ordersform.order_name.data
                ).first()
                if order != None:
                    db.session.delete(order)
                    db.session.commit()
                    return redirect("/admin_panel")
                else:
                    return render_template(
                        "admin_panel.html",
                        title="Admin Panel",
                        products=productsform,
                        orders_arr=[
                            f"Error! {ordersform.order_name.data} does not exist"
                        ],
                        orders=ordersform,
                        users=usersform,
                    )
            if ordersform.types.data == "complete":
                order = Orders.query.filter_by(
                    order_name=ordersform.order_name.data
                ).first()
                if order != None:
                    order.order_flag = "completed"
                    db.session.add(order)
                    db.session.commit()
                else:
                    return render_template(
                        "admin_panel.html",
                        title="Admin Panel",
                        products=productsform,
                        orders_arr=[
                            f"Error! {ordersform.order_name.data} does not exist"
                        ],
                        orders=ordersform,
                        users=usersform,
                    )

        if usersform.submit3.data and usersform.validate():
            if usersform.types.data == "search":
                user = User.query.filter_by(username=usersform.username.data).first()
                if not user:
                    return render_template(
                        "admin_panel.html",
                        title="Admin Panel",
                        products=productsform,
                        orders=ordersform,
                        users=usersform,
                        userd=["err", "Error! User not found!"],
                    )
                user = [user]
                return render_template(
                    "admin_panel.html",
                    title="Admin Panel",
                    products=productsform,
                    orders=ordersform,
                    users=usersform,
                    userd=user,
                )
            if usersform.types.data == "list":
                user = User.query.all()
                return render_template(
                    "admin_panel.html",
                    title="Admin Panel",
                    products=productsform,
                    orders=ordersform,
                    users=usersform,
                    userd=user,
                )
            if usersform.types.data == "delete":
                user = User.query.filter_by(username=usersform.username.data).first()
                if not user:
                    return render_template(
                        "admin_panel.html",
                        title="Admin Panel",
                        products=productsform,
                        orders=ordersform,
                        users=usersform,
                        userd=["err", "Error! User not found!"],
                    )
                db.session.delete(user)
                db.session.commit()
                return render_template(
                    "admin_panel.html",
                    title="Admin Panel",
                    products=productsform,
                    orders=ordersform,
                    users=usersform,
                    userd=["err", "${user} has been removed"],
                )
        return render_template(
            "admin_panel.html",
            title="Admin Panel",
            products=productsform,
            orders=ordersform,
            users=usersform,
        )
    else:
        return render_template("404.html"), 404
