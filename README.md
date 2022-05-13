# python_weather_app
A Desktop Weather App Using Python  
What the project uses,  
  1) Reads a config file to determine what zip codes to get the weather foirecast for. This is so the citys to forecast chan be changed withoput having to change the code in any way.
  2) Calls the "https://api.weatherapi.com/v1/forecast.json" data in JSON format and parses out the forecast Temperature and Wind data by hour for 3 days.  
  3) Plots the data by day with two matplotlib plots.  
  4) Uses PySimpleGui for a nice simple user interface.
  NOTE: You have to go to www.weatherapi.com and register for yor free KEY. Once you get yourr key, place it in this variable inside the script.  
  WEATHER_API_KEY = "-your-key-here-"


![Main GUI](https://github.com/Hagtronics/python_weather_app/blob/main/pictures/weather_app_gui.PNG)
