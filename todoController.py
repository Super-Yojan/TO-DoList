from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import item, Base

app = Flask('__name__')
engine = create_engine('sqlite:///todolist.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)


@app.route('/')
def new_todo():
    return render_template('main.html')


@app.route('/addItem' , methods=['GET', 'POST'])
def add_item():
    session = Session()
    newitem = item(items = request.form['item'])
    session.add(newitem)
    session.commit()
    return redirect(url_for('new_todo'))


@app.route('/showItem', methods=['GET','POST'])
def show_item():
    session = Session()
    items = session.query(item).all()
    return render_template('show.html', items=items)


@app.route('/editItem/<int:id>/' , methods=['GET', 'POST'])
def edit_item(id):
    session = Session()
    items = session.query(item).filter_by(id = id).one()
    if request.method == 'POST':
        if request.form['item']:
            items.items = request.form['item']
            session.add(items)
            session.commit()
        return redirect(url_for('show_item'))
    else:
        return render_template('edit.html', item = items)

@app.route('/deleteItem/<int:id>/')
def delete_item(id):

    session = Session()
    items = session.query(item).filter_by(id = id).one()
    session.delete(items)
    session.commit()
    return redirect(url_for('show_item'))

if __name__ == '__main__':
    app.debug = False
    app.run()

