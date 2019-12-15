from flask import Flask, render_template, request, url_for, redirect, g
from flask import session as sn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import item, Base , User
import os

app = Flask('__name__')
engine = create_engine('sqlite:///todolist.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

app.secret_key= os.urandom(24)

@app.route('/')
def new_todo():
    return render_template('login.html')


@app.route('/addItem/<int:user_id>' , methods=['GET', 'POST'])
def add_item(user_id):
    session = Session()
    if request.method == 'POST':
        newitem = item(items = request.form['item'], user_id = user_id)
        session.add(newitem)
        session.commit()
        return render_template('main.html', user_id = user_id)
    else:
        return render_template('main.html', user_id = user_id)

@app.route('/showItem/<int:user_id>', methods=['GET','POST'])
def show_item(user_id):
    session = Session()
    if g.user:
        items = session.query(item).filter_by(user_id = user_id).all()
        return render_template('show.html', items=items , user_id = user_id)
    else:
        return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if sn:
        g.user = sn['user']

@app.route('/editItem/<int:id>/<int:user_id>' , methods=['GET', 'POST'])
def edit_item(id , user_id):
    session = Session()
    items = session.query(item).filter_by(id = id , user_id = user_id).one()
    if request.method == 'POST':
        if request.form['item']:
            items.items = request.form['item']
            session.add(items)
            session.commit()
        return redirect(url_for('show_item' , user_id = user_id))
    else:
        return render_template('edit.html', item = items , user_id = user_id)


@app.route('/deleteItem/<int:user_id>/<int:id>')
def delete_item( user_id, id):
    session = Session()
    items = session.query(item).filter_by(user_id=user_id, id=id).one()
    session.delete(items)
    session.commit()
    return redirect(url_for('show_item' , user_id = user_id ))


@app.route('/login' , methods=['GET' , 'POST'])
def login():
    session = Session()
    sn.pop('user', None)
    try:
        user = session.query(User).filter_by(email = request.form['email'] , password = request.form['password']).one()
        sn['user'] = request.form['email']
        return redirect(url_for('show_item', user_id=user.id))
    except:
        return render_template('login.html')


@app.route('/createacc' , methods=['GET', 'POST'])
def create_acc():
    session = Session()
    if request.method == 'POST':
        oldUser = session.query(User).filter_by(email = request.form['email']).all()
        if len(oldUser) == 0:
            newUser = User(first_name = request.form['first_name'], last_name=request.form['last_name'], email=request.form['email'],
                           password = request.form['password'])
            session.add(newUser)
            session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('createacc.html', error = "Email already exists. Please use a different one")
    else:
        return render_template('createacc.html')

@app.route('/logout')
def logout():
    sn.pop('user', None)
    return redirect(url_for('new_todo'))


if __name__ == '__main__':
    app.debug = True
    app.run()

