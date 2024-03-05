from sqlalchemy.orm import Session
from app.database.models.users import User
from app.database.models.publics import Publics


def add_or_update_user(db: Session, user_id: int, username: str):
        new_user = User(user_id=user_id, name=username)
        db.add(new_user)
        db.commit()
        print("Пользователь добавлен")


def get_all_user_ids(db: Session) -> list:
    all_users = db.query(User).all()
    user_ids = [user.user_id for user in all_users]
    return user_ids


def add_public(db: Session, id_pub: int, url_pub: str):
    new_public = Publics(id_pub=id_pub, url_pub=url_pub)
    db.add(new_public)
    db.commit()
    print("Паблик добавлен")


def find_public(db: Session):
    all_publics = db.query(Publics).all()
    public_urls = [public.url_pub for public in all_publics]
    return public_urls


def delete_all_publics(db: Session):
    db.query(Publics).delete()
    db.commit()


def find_public_ids(db: Session):
    all_publics = db.query(Publics).all()
    public_ids = [public.id_pub for public in all_publics]
    return public_ids


def find_user(db: Session):
    all_users = db.query(User).all()
    user_details = [f"{user.name}: {user.user_id}" for user in all_users]
    return user_details

