from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")
weatherstack_api_key = "003a87c533f4f9a8e434d480dd4c1c997"



cities = {
    "New York": "40.7128  -74.0060",
    "London": "51.5074  -0.1278",
    "Paris": "48.8566  2.3522",
    "Tokyo": "35.6762  139.6503",
    "Sydney": "-33.8651  151.2093",
    "Rio de Janeiro": "-22.9068  -43.1729",
    "Dubai": "25.2048  55.2708",
    "Mumbai": "19.0760  72.8777",
    "Hong Kong": "22.3193  114.1694",
    "Singapore": "1.3521  103.8198",
    "Toronto": "43.6532  -79.3832",
    "Berlin": "52.5200  13.4050",
    "Moscow": "55.7558  37.6173",
    "Beijing": "39.9042  116.4074",
    "Bangkok": "13.7563  100.5018",
    "Cairo": "30.0444  31.2357",
    "Istanbul": "41.0082  28.9784",
    "São Paulo": "-23.5505  -46.6333",
    "Mexico City": "19.4326  -99.1332",
    "New Delhi": "28.6139  77.2090"
}



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "cities": cities})


@app.get("/manual", response_class=HTMLResponse)
async def manual(request: Request):
    return templates.TemplateResponse("manual.html", {"request": request})

@app.get("/famous", response_class=HTMLResponse)
async def famous(request: Request):
    return templates.TemplateResponse("famous.html", {"request": request, "cities": cities})


@app.post("/weather", response_class=HTMLResponse)
async def weather(request: Request, location: str = Form(...), units: str = "m"):
    # Create the API url with the location and units parameters
    url = f"http://api.weatherstack.com/forecast?access_key={weatherstack_api_key}&query={location}&units={units}"
    # Send a GET request to the API url
    response = requests.get(url)

    if response.status_code == 200:
        # If the response status code is 200, then retrieve the JSON data from the response
        data = response.json()

        # Extract the required weather data from the JSON object and store it in a dictionary
        weather = {
            "location": data["location"]["name"],
            "temperature": data["current"]["temperature"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_speed"],
            "description": data["current"]["weather_descriptions"][0],
            "icon": data["current"]["weather_icons"][0],
            "forecast": data.get("forecast", {}).get("forecastday", [{}])[0].get("day", {}).get("condition", {}).get("text", ""),
            "forecast_icon": data.get("forecast", {}).get("forecastday", [{}])[0].get("day", {}).get("condition", {}).get("icon", {}).get("url", "")

        }

        # Render the weather.html template with the weather data dictionary as context
        return templates.TemplateResponse("weather.html", {"request": request, "weather": weather})

    else:
        # If the response status code is not 200, then render the error.html template with an error message
        return templates.TemplateResponse("error.html",
                                          {"request": request, "error": "Could not retrieve weather data."})

