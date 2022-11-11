from flask import Flask,session,redirect,render_template,flash, request, url_for
from jinja2 import StrictUndefined
from model import connect_to_db,db, Formula
import crud 
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms import FormulaForm, LoginForm
import os
# from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'unlikely_to_decode'
app.jinja_env.undefined = StrictUndefined

###################################### LOGIN MANAGER #####################################
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return crud.User.query.filter_by(user_id = user_id).first()
####################################  LOG-IN---LOG-OUT ###################################

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    email = login_form.email.data
    password = login_form.password.data
    if login_form.validate_on_submit():
        user = crud.find_user(email)
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("No user found. Check your credentials and try again!")
                return redirect(url_for('homepage'))
        else:
                flash("No user found. Check your credentials and try again!")
                return redirect(url_for('homepage'))
    else:
        return redirect(url_for("homepage"))


@app.route("/logout")
@login_required
def logout():    
    logout_user()
    flash("Successfully logged out. Thanks for stopping by... :) ")
    return redirect((url_for('homepage')))

###################################################################################

@app.route("/")
def homepage():
    login_form = LoginForm()
    return render_template("login.html", login_form=login_form)


@app.route("/dashboard")
@login_required
def dashboard():
    query = Formula.query.order_by(Formula.formula_id.desc()).limit(10).all()
    return render_template("dashboard.html", query=query)


@app.route("/formulae")
@login_required
def formulas():
    new_formula = FormulaForm()
    return render_template("create_f.html", nf=new_formula)


@app.route("/add-formula", methods=["GET", "POST"])
@login_required
def add_formula():
    f_form = FormulaForm()
    if f_form.validate_on_submit():
        user_id = current_user.user_id
        code = f_form.formula_code.data
        name = f_form.name.data
        description = f_form.description.data
        customer = f_form.customer.data
        init_visc = f_form.init_visc.data
        init_pH = f_form.init_pH.data
        init_sg = f_form.init_sg.data
        new_formula = Formula(user_id, code, name, description, customer, init_visc, init_pH, init_sg)
        db.session.add(new_formula)
        db.session.commit()
        flash("Formula added successfully!!")
        return redirect("/formulae")
    else:
        flash("Revise your inputs.")
        return redirect("/formulae")


@app.route("/formulae/search", methods=['POST', 'GET'])
@login_required
def formula_search():
    search_f = request.form.get("searched")
    result = crud.find_formula(search_f)
    if len(result) == 0:
        flash("Not found. Revise your input and try again")
        print (result)
        return redirect("/formulae")
    else:
        print (result)    
        return render_template("search_f.html", formulas=result)


@app.route("/details/<formula_id>")
@login_required
def details_f(formula_id):
    detailed_f = Formula.query.filter_by(formula_id = formula_id).first()
    return render_template("details_f.html", df=detailed_f)


@app.route("/update/<formula_id>")
@login_required
def update(formula_id):
    formula_form = FormulaForm() 
    detailed_f = Formula.query.filter_by(formula_id = formula_id).first()
    session['formula_code'] = detailed_f.formula_code
    return render_template("update_f.html", df=detailed_f, nf=formula_form, name=detailed_f.name)


@app.route("/update-enforce", methods=['POST', 'GET'])
@login_required
def update_enforce():
    f_form = FormulaForm()
    if f_form.validate_on_submit():
        f_to_update = Formula.query.filter_by(formula_code = session['formula_code']).first()
        f_to_update.user_id = current_user.user_id
        f_to_update.formula_code = f_form.formula_code.data
        f_to_update.name = f_form.name.data
        f_to_update.customer = f_form.customer.data
        f_to_update.init_visc = f_form.init_visc.data
        f_to_update.init_pH = f_form.init_pH.data
        f_to_update.init_sg = f_form.init_sg.data
        f_to_update.description = request.form.get("description")
        db.session.commit()
        flash(f"{f_to_update.formula_code} Successfully updated!")
        session['formula_code'] = ""
        return render_template("details_f.html", df=f_to_update)
    else:
        flash("Make sure all the information is correct and try again")
        return redirect(f"/update/{f_to_update.formula_id}")


#################################### ERROR HANDLERS ####################################

@app.errorhandler(404)
def notfound(e):
   return render_template('404.html')

@app.errorhandler(401)
def unauthorized(e):
   return render_template('401.html')

#######################################  TRIGGER  ########################################
if __name__== '__main__':
    app.env = 'development'
    connect_to_db(app)
    app.run()
    