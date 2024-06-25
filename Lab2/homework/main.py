import json
import os
from statistics import mean
from typing import Optional

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

load_dotenv()
weatherAPI = os.getenv('weatherAPI')
openWeather = os.getenv('openWeather')
weatherbit = os.getenv('weatherbit')
APIKEY = os.getenv('APIKEY')

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.exception_handler(HTTPException)
async def HTTPExceptionHandler(request: Request, error: HTTPException):
    return templates.TemplateResponse("error.html", context={'request': request, "error": error.detail},status_code=400)


@app.exception_handler(Exception)
async def OtherExceptionHandler(request: Request, error: Exception):
    return templates.TemplateResponse("error.html", context={'request': request, "error": str(error)},status_code=400)


def verify_apikey(request: Request) -> bool:
    global APIKEY
    header_apikey = request.headers.get("APIKEY")

    if not header_apikey:
        raise HTTPException(status_code=401, detail="Missing apikey in header")

    if header_apikey != APIKEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return True


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("start.html", context={"request": request})


@app.post("/airquality")
async def result(request: Request, verify: bool = Depends(verify_apikey), city: Optional[str] = Form(None)):
    if city is None:
        raise HTTPException(status_code=401, detail="No city provided")

    context = get_weather(city)
    # context['request'] = request
    # return templates.TemplateResponse("output.html", context=context)
    return JSONResponse(content=context)

class AirInfo:

    def __init__(self, city: str):
        self.city = city
        self.co = []
        self.no2 = []
        self.pm2_5 = []
        self.pm10 = []

    def stats(self) -> dict:
        return {
            'city': self.city,
            'co': self.co,
            'no2': self.no2,
            'pm2_5': self.pm2_5,
            'pm10': self.pm10,
            'average_co': round(mean(self.co), 2),
            'average_no2': round(mean(self.no2), 2),
            'average_pm10': round(mean(self.pm10), 2),
            'average_pm2_5': round(mean(self.pm2_5), 2),
            'difference_co': max(self.co) - min(self.no2),
            'difference_no2': max(self.no2) - min(self.no2),
            'difference_pm2_5': max(self.pm2_5) - min(self.pm2_5),
            'difference_pm10': max(self.pm10) - min(self.pm10)
        }


def get_weather(city: str) -> dict:
    global openWeather, weatherAPI, weatherbit

    air_info = AirInfo(city)
    try:
        location_url = f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={openWeather}'
        response = requests.get(location_url)
        response.raise_for_status()
        data = json.loads(response.content).pop()

        lat = data.get('lat')
        lon = data.get('lon')

        url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={openWeather}'
        response = requests.get(url)
        response.raise_for_status()
        data = json.loads(response.content)

        components = data['list'][0]['components']
        air_info.no2.append(components.get('no2'))
        air_info.co.append(components.get('co'))
        air_info.pm2_5.append(components.get('pm2_5'))
        air_info.pm10.append(components.get('pm10'))

    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException) as er:
        raise HTTPException(status_code=500, detail=f"Error during request to OpenWeather")
    except (KeyError, ValueError) as er:
        raise HTTPException(status_code=501, detail=f"Bad response arguments from API")

    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={weatherAPI}&q={city}&aqi=yes"
        response = requests.get(url)
        response.raise_for_status()
        data = json.loads(response.content)
        data = data['current']['air_quality']

        air_info.no2.append(data.get('no2'))
        air_info.co.append(data.get('co'))
        air_info.pm2_5.append(data.get('pm2_5'))
        air_info.pm10.append(data.get('pm10'))
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException) as er:
        raise HTTPException(status_code=500, detail=f"Error during request to WeatherAPI")

    except (KeyError, ValueError) as er:
        raise HTTPException(status_code=501, detail=f"Bad response arguments from API")

    try:
        url = f"https://api.weatherbit.io/v2.0/current/airquality?city={city}&key={weatherbit}"
        response = requests.get(url)
        data = json.loads(response.content)
        data = data['data'].pop()

        air_info.no2.append(data.get('no2'))
        air_info.co.append(data.get('co'))
        air_info.pm2_5.append(data.get('pm25'))
        air_info.pm10.append(data.get('pm10'))

    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException) as er:
        raise HTTPException(status_code=500, detail=f"Error during request to WeatherBit")

    except (KeyError, ValueError) as er:
        raise HTTPException(status_code=501, detail=f"Bad response arguments from API")

    return air_info.stats()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
