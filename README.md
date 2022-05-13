# python_weather_app
A Desktop Weather App Using Python  
What the project does,  
  1) Reads a config file to determine what zip codes to get the weather forecast for. This is so the city's to forecast can be changed withoput having to change the code in any way.
  2) Calls the "https://api.weatherapi.com/v1/forecast.json" data in JSON format and parses out the forecast Temperature and Wind data by hour for 3 days.  
  3) Plots the data by day with two matplotlib sub-plots.  
  4) Uses PySimpleGui for a nice simple user interface.
    
  NOTE: You have to go to www.weatherapi.com and register for yor free KEY. Once you get your key, place it in this variable inside the script,   
       WEATHER_API_KEY = "-your-key-here-"

Example Forecast Data for one day, and the three citie's that I have set in the config file.  
You can press the Previous and Next day buttons to look at all three forecast days.
![Main GUI](https://github.com/Hagtronics/python_weather_app/blob/main/pictures/weather_app_gui.PNG)
