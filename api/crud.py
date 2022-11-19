from database import db_context
from models import User, Weather
from schemas import UserIn, UserOut, WeatherIn, WeatherOut


def crud_add_user(user: UserIn):
    db_user = User(**user.dict())
    with db_context() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


def crud_get_user(user_id: int):
    with db_context() as db:
        user = db.query(User).filter(User.id == user_id).first()
    if user:
        return UserOut(**user.__dict__)
    return None


def crud_add_weather(weather: WeatherIn):
    db_weather = Weather(**weather.dict())
    with db_context() as db:
        exist = (
            db.query(Weather)
            .filter(Weather.city == weather.city, Weather.date == weather.date)
            .first()
        )
        if exist:
            return None
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
    return db_weather


def crud_get_weather(city: str):
    with db_context() as db:
        weather = (
            db.query(Weather)
            .filter(Weather.city == city)
            .order_by(Weather.date.desc())
            .limit(7)
            .all()
        )
    if weather:
        result = []
        for item in weather:
            result.append(WeatherOut(**item.__dict__))
        return {city: result[::-1]}
    return None


def crud_error_message(message):
    return {"error": message}
