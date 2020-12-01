from flask import render_template, flash, redirect, url_for, Markup
from linkedary import app
from linkedary.forms import LoginForm
from linkedary.linkedin_con import LinkeDary

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        result_html = LinkeDary(form.fbusername.data, form.fbpassword.data,form.fb_url.data,form.max_scrolldown.data,form.liusername.data, form.lipassword.data,form.first_row.data, form.last_row.data,form.text_whith_company.data, form.text_whithout_company.data,form.dryrun.data,form.min_wait.data, form.max_wait.data)
        print('Result:<br>{}'.format(result_html.replace("\n","<br>")))
        flash(Markup('Result:<br>{}'.format(result_html.replace("\\r","").replace("\\n","<br>"))))
        return redirect(url_for('index'))
    return render_template('form.html', title='Get More Connections', form=form)

