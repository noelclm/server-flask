from flask_jwt_extended import create_access_token
from datetime import timedelta

from sqlalchemy import and_

from src.models import db
from src.models.user import User

def generate_unique_data(event):
    identity = {
        "email": event.get('email'),
        "user_id": event.get('user_id')
    }

    user = User.query.get(identity['user_id'])
    if user is None:
        raise PermissionError('Permission Denied')
    unique_data = create_access_token(identity=identity)
    user.unique_data = unique_data
    db.session.merge(user)
    db.commit()
    return {'unique_data': unique_data}


def generate_temp_token(event):
    identity = {
        "email": event.get('email'),
        "user_id": event.get('user_id'),
        "unique_data": event.get('unique_data')
    }
    user = User.query.filter(and_(User.email == identity['email'], User.unique_data == identity['unique_data'])).first()
    if user is None:
        raise PermissionError('Permission Denied')
    token = create_access_token(identity=identity, expires_delta=timedelta(hours=1))
    return {'access_token': token}
