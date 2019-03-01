# google places

import googlemaps
import pyowm
from datetime import datetime, timedelta

class GoogleAPI:
	def __init__(self):
		self.gmaps = googlemaps.Client(key="AIzaSyD1DZ0ssvTSupPVLijR4wn4_9bg0Z5QBE0")

	def getNearby(self, latitude, longitude, radius=20.0):
		print('latitude', latitude, 'longitude', longitude)
		data = self.gmaps.places_nearby((latitude, longitude), radius=radius)

		return data['results']


class WeatherAPI:
	def __init__(self):
		self.weather = pyowm.OWM('dae3a235f3b0b168acec4955c801ca47')
		self.cache = None

	def getCurrentWeather(self):

		if self.cache is not None:
			if self.cache['expire'] > datetime.now():
				return self.cache['result']

		w = self.weather.weather_at_place('Irvine,US').get_weather()
		result = {
			'timestamp': w.get_reference_time(),
			'clouds': w.get_clouds(),
			'rain': w.get_rain(),
			'show': w.get_snow(),
			'wind': w.get_wind(),
			'humidity': w.get_humidity(),
			'pressure': w.get_pressure(),
			'temperature': w.get_temperature('fahrenheit'),
			'status': w.get_status(),
		}

		self.cache = {
			'result': result,
			'expire': datetime.now() + timedelta(minutes=10)
		}

		return result

gmaps = GoogleAPI()
weatherAPI = WeatherAPI()
