from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from data import db_session
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class User(db_session.SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)


class LoginForm(FlaskForm):
    name = StringField('Имя')
    surname = StringField('Фамилия')
    submit = SubmitField('Отправить')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    session = db_session.create_session()
    users = session.query(User).all()
    for x in users:
        k = x.id
    k += 1
    if form.validate_on_submit():
        user = User(
            id=k,
            name=form.name.data,
            surname=form.surname.data
        )
        session.add(user)
        session.commit()
        return redirect('/')

    users = session.query(User).all()
    return render_template('add_name.html', form=form, users=users)


def main():
    db_session.global_init("db/test.db")
    app.run()


if __name__ == '__main__':
    main()
