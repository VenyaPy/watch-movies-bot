from sqlalchemy.orm import Session
from app.database.models.users import User, Publics, Admins



def add_or_update_user(db: Session, user_id: int, username: str):
        new_user = User(user_id=user_id, name=username)
        db.add(new_user)
        db.commit()
        print("Пользователь добавлен")


def get_all_user_ids(db: Session) -> list:
    all_users = db.query(User).all()
    user_ids = [user.user_id for user in all_users]
    return user_ids


def get_user_join_date(db: Session, user_id: int) -> str:
    user_data = db.query(User).filter(User.user_id == user_id).first()
    if user_data:
        formatted_date = user_data.join_date.strftime('%d.%m.%Y %H:%M')
        return formatted_date
    else:
        return "Пользователь не найден"


def get_user_count(db: Session) -> int:
    user_count = db.query(User).count()
    return user_count


def get_public_count(db: Session) -> int:
    public_count = db.query(Publics).count()
    return public_count


def add_public(db: Session, id_pub: int, url_pub: str):
    new_public = Publics(id_pub=id_pub, url_pub=url_pub)
    db.add(new_public)
    db.commit()
    print("Паблик добавлен")


def add_admin_bd(db: Session, user_id: int):
    new_admin = Admins(user_id=user_id)
    db.add(new_admin)
    db.commit()
    print("Админ добавлен")


def show_admins(db: Session):
    all_admins = db.query(Admins).all()
    admin_ids = [admins.user_id for admins in all_admins]
    return admin_ids


def del_admins_bd(db: Session, user_id: int):
    db.query(Admins).filter(Admins.user_id == user_id).delete()
    db.commit()


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


def get_user_id(db: Session):
    all_users = db.query(User).all()
    for user in all_users:
        yield user.user_id

