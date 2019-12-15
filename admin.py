from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import User, Base

app = Flask('__name__')

engine = create_engine('sqlite:///todolist.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

@app.route("/")
def userController():
    session = Session()
    Users = session.query(User).all()
    #deluser= session.query(User).filter_by(id = 2).one()
    #session.delete(deluser)
    #session.commit()
    return render_template('admin.html' , users = Users)


if __name__ == '__main__':
    app.run(port=8080)