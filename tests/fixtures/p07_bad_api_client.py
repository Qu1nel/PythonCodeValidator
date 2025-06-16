"""A poorly structured API client."""
# Нет константы API_KEY
# Используется запрещенный import
import os

def get_weather(city): # Нет аннотаций типов
    # URL захардкожен
    response = os.system("curl https://api.weather.com/v1/current") 
    return {"temp": 20}