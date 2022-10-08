from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from database import engine
from models import Base
import tasks
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    """
        Developer: Alperen Cubuk
    """
    return {"Alperen": "Cubuk"}


@app.post("/users/{count}/{delay}", status_code=201)
def add_user(count: int, delay: int):
    """
        Get random user data from randomuser.me/api and
        add database using Celery. Uses Redis as Broker
        and Postgres as Backend.
    """
    task = tasks.task_add_user.delay(count, delay)
    return {'task_id': task.id}


@app.post("/users/{count}", status_code=201)
def add_user_default_delay(count: int):
    """
        Get random user data from randomuser.me/api add
        database using Celery. Uses Redis as Broker
        and Postgres as Backend. (Delay = 10 sec)
    """
    return add_user(count, 10)


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
        Get user from database.
    """
    user = crud.crud_get_user(user_id)
    if user:
        return user
    else:
        raise HTTPException(
            404,
            crud.crud_error_message(f'No user found for id: {user_id}'))


@app.post("/weathers/{city}/{delay}", status_code=201)
def add_weather(city: str, delay: int):
    """
        Get weather data from api.collectapi.com/weather
        and add database using Celery. Uses Redis as Broker
        and Postgres as Backend.
    """
    task = tasks.task_add_weather.delay(city, delay)
    return {'task_id': task.id}


@app.post("/weathers/{city}", status_code=201)
def add_weather_default_delay(city: str):
    """
        Get weather data from api.collectapi.com/weather
        and add database using Celery. Uses Redis as Broker
        and Postgres as Backend. (Delay = 10 sec)
    """
    return add_weather(city, 10)


@app.get("/weathers/{city}")
def get_weather(city: str):
    """
        Get weather from database.
    """
    weather = crud.crud_get_weather(city.lower())
    if weather:
        return weather
    else:
        raise HTTPException(
            404,
            crud.crud_error_message(f'No weather found for city: {city}'))


@app.get("/tasks/{task_id}")
def task_status(task_id: str):
    """
        Get task status.
        PENDING (waiting for execution or unknown task id)
        STARTED (task has been started)
        SUCCESS (task executed successfully)
        FAILURE (task execution resulted in exception)
        RETRY (task is being retried)
        REVOKED (task has been revoked)
    """
    task = AsyncResult(task_id)
    state = task.state

    if state == 'FAILURE':
        error = str(task.result)
        response = {
            'state': state,
            'error': error,
        }
    else:
        response = {
            'state': state,
        }
    return response
