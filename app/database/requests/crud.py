from sqlalchemy.orm import Session
from app.database.models.users import User


def add_or_update_user(db: Session, user_id: int, username: str):
        new_user = User(user_id=user_id, name=username)
        db.add(new_user)
        db.commit()
        print("Пользователь добавлен")


def get_all_user_ids(db: Session) -> list:
    all_users = db.query(User).all()
    user_ids = [user.user_id for user in all_users]
    return user_ids
