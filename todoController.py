from flask import Flask, render_template, request, url_for, redirect, session, escape
import todo
import os

app = Flask('__name__')

app.secret_key = os.urandom(24)


@app.route('/')
def new_todo():
    if 'user_id' in session:
        return redirect(url_for('show_item'))
    else:
        return render_template('login.html')


@app.route('/addItem/', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            todo.add_item(user_id=user_id, items=request.form['item'])
        return render_template('main.html')
    else:
        return render_template('main.html')


@app.route('/editItem/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    if request.method == 'POST':
        if request.form['item']:
            if 'user_id' in session:
                user_id = session['user_id']
                todo.edit_item(user_id=user_id, id=id, edit_item=request.form['item'])

        return redirect(url_for('show_item', user_id=session['user_id']))
    else:
        if 'user_id' in session:
            user_id = session['user_id']
            item = todo.show_item(user_id=user_id , item_id=id)
            return render_template('edit.html', user_id=user_id, item=item)
        else:
            return redirect(url_for('new_todo'))


@app.route('/deleteItem/<int:id>')
def delete_item(id):
    if 'user_id' in session:
        user_id = session['user_id']
        todo.delete_item(user_id=user_id, id=id)
        return redirect(url_for('show_item', user_id=user_id))
    else:
        return render_template('login.html')


@app.route('/showItem/', methods=['GET', 'POST'])
def show_item():
    if 'user_id' in session:
        user_id = session['user_id']
        items = todo.show_items(user_id=user_id)
        return render_template('show.html', items=items, user_id=user_id)
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user_id', None)

    user = todo.login_verification(email=request.form['email'], password=request.form['password'])

    if user is not None:
        session['user_id'] = user.id
        return redirect(url_for('show_item'))
    else:
        return render_template('login.html')


@app.route('/createacc', methods=['GET', 'POST'])
def create_acc():
    if request.method == 'POST':
        if todo.create_account(first_name=request.form['first_name'], last_name=request.form['last_name'],
                               email=request.form['email'],
                               password=request.form['password']) == True:
            return redirect(url_for('login'))
        else:
            return render_template('createacc.html', error="Email already exists. Please use a different one")
    else:
        return render_template('createacc.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('new_todo'))


if __name__ == '__main__':
    app.debug = True
    app.run()
