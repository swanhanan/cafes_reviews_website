from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('location_url', validators=[DataRequired(),URL(require_tld=True)])
    open_time = TimeField('open_time', validators=[DataRequired()])
    closing_time = TimeField('closing time', [DataRequired()])
    coffee_rating = SelectField('coffee_rating', choices=['❌', '☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'], validators=[DataRequired()])
    wifi_rating = SelectField('wifi_rating', choices=['❌', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    power_outlet = SelectField('power_outlet', choices=['❌', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # write a new row into cafe-data.csv
        with open('../cafes_reviews/cafe-data.csv', encoding="utf-8", mode="a") as csv_file:
            new_data = csv_file.write(f"\n{form.cafe.data}, {form.location.data}, {form.open_time.data}, {form.closing_time.data}, {form.coffee_rating.data}, {form.wifi_rating.data}, {form.power_outlet.data}")
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('../cafes_reviews/cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
