from database import db_context
import models
import schemas


def crud_add_user(user: schemas.UserIn):
    db_user = models.User(**user.dict())
    with db_context() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


def crud_get_user(user_id: int):
    with db_context() as db:
        user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return schemas.UserOut(**user.__dict__)
    return None


def crud_add_weather(weather: schemas.WeatherIn):
    db_weather = models.Weather(**weather.dict())
    with db_context() as db:
        exist = db.query(models.Weather).filter(
            models.Weather.city == weather.city,
            models.Weather.date == weather.date).first()
        if exist:
            return None
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)
    return db_weather


def crud_get_weather(city: str):
    with db_context() as db:
        weather = db.query(models.Weather).filter(
            models.Weather.city == city).order_by(
            models.Weather.date.desc()).limit(7).all()
    if weather:
        result = []
        for item in weather:
            result.append(schemas.WeatherOut(**item.__dict__))
        return {city: result[::-1]}
    return None


def crud_error_message(message):
    return {'error': message}
