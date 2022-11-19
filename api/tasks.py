import time

import requests
from celery import Celery
from crud import crud_add_user, crud_add_weather
from schemas import UserIn, WeatherIn

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="sqla+postgresql://user:password@database:5432/alpha",
)


@app.task
def task_add_user(count: int, delay: int):
    url = "https://randomuser.me/api"
    response = requests.get(f"{url}?results={count}").json()["results"]
    time.sleep(delay)
    result = []
    for item in response:
        user = UserIn(
            first_name=item["name"]["first"],
            last_name=item["name"]["last"],
            mail=item["email"],
            age=item["dob"]["age"],
        )
        if crud_add_user(user):
            result.append(user.dict())
    return {"success": result}


@app.task
def task_add_weather(city: str, delay: int):
    url = "https://api.collectapi.com/weather/getWeather?data.lang=tr&data.city="
    headers = {
        "content-type": "application/json",
        "authorization": "apikey 4HKS8SXTYAsGz45l4yIo9P:0NVczbcuJfjQb8PW7hQV48",
    }
    response = requests.get(f"{url}{city}", headers=headers).json()["result"]
    time.sleep(delay)
    result = []
    for item in response:
        weather = WeatherIn(
            city=city.lower(),
            date=item["date"],
            day=item["day"],
            description=item["description"],
            degree=item["degree"],
        )
        if crud_add_weather(weather):
            result.append(weather.dict())
    return {"success": result}
