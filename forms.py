from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, IntegerField, PasswordField, TextAreaField 
from wtforms.validators import Length, DataRequired



class UserForm(FlaskForm):
# This form will handle addin a new user
    email = StringField("Team Name", validators=[DataRequired(), Length(min=4, max=255)])
    password = PasswordField('User ID', validators=[DataRequired()])
    submit = SubmitField('Add New User')



class LoginForm(FlaskForm):
# This form will handle log in info
    email = StringField("Email", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Submit")



class FormulaForm(FlaskForm):
# This form will handle addin a new formula
    formula_code = StringField("Formula Code", validators=[DataRequired(), Length(min=7, max=7)])
    name = StringField("Formula Name", validators=[DataRequired()]) 
    description = TextAreaField("Description")
    customer = StringField("Formula Name", validators=[Length(max=50)])
    init_visc = IntegerField("Initial Viscosity")
    init_pH = FloatField("Initial pH")
    init_sg = FloatField("Specific Gravity")
    submit = SubmitField("Submit")



class MaterialForm(FlaskForm):
# This form will handle addin a new raw material
    rm_code = StringField("Raw Material Code", validators=[DataRequired(), Length(min=7, max=7)])
    inci = StringField("INCI", validators=[DataRequired(), Length(max=255)])
    vendor = StringField("Vendor", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])