from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField,TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    liusername = StringField('LI Username', validators=[DataRequired()])
    lipassword = PasswordField('LI Password', validators=[DataRequired()])
    fbusername = StringField('FB Username', validators=[DataRequired()])
    fbpassword = PasswordField('FB Password', validators=[DataRequired()])
    fb_url = StringField('FB Group Members URL', validators=[DataRequired()])
    max_scrolldown= IntegerField('Max Scroll down',default=20)
    first_row= IntegerField('First row number',default=0)
    last_row= IntegerField('Last row number',default=10)
    min_wait= IntegerField('Min wait (in seconds)',default=3)
    max_wait= IntegerField('Max wait (in seconds)',default=10)
    text_whith_company = TextAreaField("Text with company name")
    text_whithout_company = TextAreaField("Text without company name")
    csv_data = TextAreaField("Row data (csv content)")
    dryrun = BooleanField('Dry run',default=True)
    submit = SubmitField('Run')