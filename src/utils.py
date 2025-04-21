import requests
import redis
import json
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv('API_KEY')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_USERNAME = os.getenv('REDIS_USERNAME')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
    decode_responses=True)


def query_redis(city: str):
    if redis_client.exists(city):
        return json.loads(redis_client.get(city))
    logger.warning(f'City {city} does not exists in redis')
    return None


def update_redis(city: str, json_data):
    redis_client.setex(name=city, time=36000, value=json.dumps(json_data))
    logger.info(f'Update {city} in redis')


base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
def query_weather(city: str):
    weather = query_redis(city)
    if weather:
        logging.info(f'Weather data about {city} already exists in redis')
        return weather

    logging.info(f'Going to query API to get weather information about {city}')
    response = requests.get(f'{base_url}/{city}?unitGroup=metric&key={API_KEY}&contentType=json')
    if response.status_code != 200:
        logger.warning(f'Unexpected Status code: {response.status_code}')
        return None

    json_data = response.json()
    update_redis(city, json_data)
    return json_data

