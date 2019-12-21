from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import item, Base, User

engine = create_engine('sqlite:///todolist.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)


def add_item(user_id, items):
    session = Session()
    newitem = item(items=items, user_id=user_id)
    session.add(newitem)
    session.commit()


def show_items(user_id):
    session = Session()
    items = session.query(item).filter_by(user_id=user_id).all()
    return items


def show_item(user_id, item_id):
    session = Session()
    one_item = session.query(item).filter_by(user_id=user_id, id = item_id).one()
    return one_item


def login_verification(email, password):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email, password=password).one()
        return user
    except :
        print('Didnot get any result')
        return None


def create_account(first_name, last_name, email, password):
    session = Session()
    oldUser = session.query(User).filter_by(email=email).all()
    if len(oldUser) == 0:
        newUser = User(first_name=first_name, last_name=last_name,
                       email=email,
                       password=password)
        session.add(newUser)
        session.commit()
        return True
    else:
        return False


def delete_item(user_id, id):
    session = Session()
    items = session.query(item).filter_by(user_id=user_id, id=id).one()
    session.delete(items)
    session.commit()


def edit_item(user_id, id, edit_item):
    session = Session()
    items = session.query(item).filter_by(id=id, user_id=user_id).one()
    items.items = edit_item
    session.add(items)
    session.commit()
