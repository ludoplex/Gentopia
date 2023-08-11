import requests
import json
import os
from typing import AnyStr, Any
from gentopia.tools.basetool import *


class Weather(BaseTool):
    api_key: str = os.getenv("WEATHER_API_KEY")
    URL_CURRENT_WEATHER = "http://api.weatherapi.com/v1/current.json"
    URL_FORECAST_WEATHER = "http://api.weatherapi.com/v1/forecast.json"


class GetTodayWeatherArgs(BaseModel):
    location: str = Field(..., description="the location to be queried, e.g., San Franciso")


class GetTodayWeather(Weather):
    """Tool that looks up today's weather information"""

    name = "get_today_weather"
    description = (
        "A tool to look up the current weather information for a given location."
        "Input should be a location."
    )
    args_schema: Optional[Type[BaseModel]] = GetTodayWeatherArgs

    def _run(self, location: AnyStr) -> AnyStr:
        param = {
            "key": self.api_key,
            "q": location
        }
        res_completion = requests.get(self.URL_CURRENT_WEATHER, params=param)
        data = json.loads(res_completion.text.strip())
        try:
            output = {
                "overall": f"{data['current']['condition']['text']},\n",
                "name": f"{data['location']['name']},\n",
                "region": f"{data['location']['region']},\n",
                "country": f"{data['location']['country']},\n",
                "localtime": f"{data['location']['localtime']},\n",
                "temperature": f"{data['current']['temp_c']}(C), {data['current']['temp_f']}(F),\n",
                "percipitation": f"{data['current']['precip_mm']}(mm), {data['current']['precip_in']}(inch),\n",
                "pressure": f"{data['current']['pressure_mb']}(milibar),\n",
                "humidity": f"{data['current']['humidity']},\n",
                "cloud": f"{data['current']['cloud']},\n",
                "body temperature": f"{data['current']['feelslike_c']}(C), {data['current']['feelslike_f']}(F),\n",
                "wind speed": f"{data['current']['gust_kph']}(kph), {data['current']['gust_mph']}(mph),\n",
                "visibility": f"{data['current']['vis_km']}(km), {data['current']['vis_miles']}(miles),\n",
                "UV index": f"{data['current']['uv']},\n",
            }
        except Exception as e:
            return f"Error occured: {e}\n The response fetched: {str(data)}"

        return (
            f"Today's weather report for {data['location']['name']} is:\n"
            + "".join([f"{key}: {output[key]}" for key in output])
        )

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class GetFutureWeatherArgs(BaseModel):
    location: str = Field(..., description="the location to be queried, e.g., San Franciso")
    days: int = Field(..., description="weather of the upcoming days, the value should be <= 3, e.g., 2")


class GetFutureWeather(Weather):
    """Tool that looks up the weather information in the future"""

    name = "get_future_weather"
    description = (
        "A tool to look up the overall weather information in the upcoming days for a given location"
    )
    args_schema: Optional[Type[BaseModel]] = GetFutureWeatherArgs

    def _run(self, location: AnyStr, days: int) -> AnyStr:
        param = {"key": self.api_key, "q": location, "days": days}
        res_completion = requests.get(self.URL_FORECAST_WEATHER, params=param)
        res_completion = json.loads(res_completion.text.strip())
        MAX_DAYS = 3
        try:
            res_completion = res_completion["forecast"]["forecastday"][
                days - 1 if days < MAX_DAYS else MAX_DAYS - 1
            ]
            output_dict = dict(res_completion["day"].items())
            for k, v in res_completion["astro"].items():
                output_dict[k] = v

            output = {
                "over all weather": f"{output_dict['condition']['text']},\n",
                "max temperature": f"{output_dict['maxtemp_c']}(C), {output_dict['maxtemp_f']}(F),\n",
                "min temperature": f"{output_dict['mintemp_c']}(C), {output_dict['mintemp_f']}(F),\n",
                "average temperature": f"{output_dict['avgtemp_c']}(C), {output_dict['avgtemp_f']}(F),\n",
                "max wind speed": f"{output_dict['maxwind_kph']}(kph), {output_dict['maxwind_mph']}(mph),\n",
                "total precipitation": f"{output_dict['totalprecip_mm']}(mm), {output_dict['totalprecip_in']}(inch),\n",
                "will rain today": f"{output_dict['daily_will_it_rain']},\n",
                "chance of rain": f"{output_dict['daily_chance_of_rain']},\n",
                "total snow": f"{output_dict['totalsnow_cm']}(cm),\n",
                "will snow today": f"{output_dict['daily_will_it_snow']},\n",
                "chance of snow": f"{output_dict['daily_chance_of_snow']},\n",
                "average visibility": f"{output_dict['avgvis_km']}(km), {output_dict['avgvis_miles']}(miles),\n",
                "average humidity": f"{output_dict['avghumidity']},\n",
                "UV index": f"{output_dict['uv']},\n",
                "sunrise time": f"{output_dict['sunrise']},\n",
                "sunset time": f"{output_dict['sunset']},\n",
                "moonrise time": f"{output_dict['moonrise']},\n",
                "moonset time": f"{output_dict['moonset']},\n",
            }
            text_output = (
                f"The weather forecast for {param['q']} at {param['days']} days later is: \n"
                + "".join([f"{key}: {output[key]}" for key in output])
            )
        except Exception as e:
            return f"Error occured: {e}. \nThe response fetched is: {str(res_completion)}"
        return text_output

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = GetTodayWeather()._run("San francisco")
    # ans = GetFutureWeather()._run("San francisco", 2)
    print(ans)
