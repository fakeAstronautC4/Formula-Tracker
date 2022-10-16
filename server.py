from flask import Flask,session,redirect,render_template,flash, request
from jinja2 import StrictUndefined
from model import connect_to_db,db, Formula
import crud 

app = Flask(__name__)
app.secret_key = 'unlikely_to_decode'
app.jinja_env.undefined = StrictUndefined
##########################################################################################

@app.route("/")
def homepage():
    return render_template("base.html")

@app.route("/formulae")
def formulas():
    query = Formula.query.order_by(Formula.formula_id.desc()).limit(10).all()
    return render_template("create_f.html", query=query)


@app.route("/formulae/search")
def formula_search():
    search_f = request.form.get("searched")
    result = crud.find_formula(search_f)
    return render_template("search_f.html", result =result)


@app.route("/formulae/details/<formula_code>")
def details_f(formula_code):
    detailed_f = crud.find_formula(formula_code)
    return render_template("details_f.html", detailed_f=detailed_f)


##########################################################################################
if __name__== '__main__':
    app.env = 'development'
    connect_to_db(app)
    app.run(debug=True, port = 9000, host= 'localhost')
    