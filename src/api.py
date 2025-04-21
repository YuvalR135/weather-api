from fastapi import FastAPI, Path, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated
from .utils import query_weather
app = FastAPI()


@app.get("/get-weather")
def get_item():
    return JSONResponse(content="Hello to weather API, you can look at /docs for Swagger UI", status_code=200)


@app.get("/get-weather/{city}")
def get_weather(city: Annotated[str, Path(title="City", description="Name of a city anywhere in the world.")]):
    weather = query_weather(city)
    if not weather:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City does not exists.")
    return weather
