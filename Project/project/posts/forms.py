from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    patient = StringField('Patient', validators=[DataRequired()])
    condition = StringField('Condition', validators=[DataRequired()])
    medication = StringField('Medication', validators=[DataRequired()])
    description = TextAreaField('Description of Condition/Treatment', validators=[DataRequired()])
    submit = SubmitField('Post')
