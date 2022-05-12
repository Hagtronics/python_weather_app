"""
Weather Forecast using the weatherapi.com free service.
You will need to signup for a free API key, then place the KEY in the
constant named: WEATHER_API_KEY  below.

Portions of GUI Based on sample code from: 
https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html

Totallyt free code, but beware: "Written by an infinite number of Monkeys in an infinite
amount of time, so this is probably very bad code."

Ver 1.0 - 30April22 - Steve Hageman
"""

# pylint: disable=missing-docstring
# pylint: disable=line-too-long
# pylint: disable=consider-using-dict-items
# pylint: disable=consider-iterating-dictionary
# pylint: disable=broad-except

import PySimpleGUI as sg
from urllib.request import urlopen
from datetime import datetime
from datetime import timedelta
import re
import json
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("tkAgg")



# -----[ Program Configuration Options ]---------------------------------------
# Config file name
FORECAST_CONFIG_FILE_NAME = "WeatherForecastZipCodes.txt"

# Keep this secret!
WEATHER_API_KEY = "875 -- insert your key here ---003"


# -----[ Read in cities list ]-------------------------------------------------
def get_the_forecast_locations() -> dict:
    """Reads the configuration file

    Returns:
        dict: Zipcode, City names dictionary.
    """
    found_locations = {}

    try:
        with open(FORECAST_CONFIG_FILE_NAME, mode="r", encoding="utf-8") as f:
            file_contents = f.readlines()
    except FileNotFoundError:     
        sg.popup(f"File {FORECAST_CONFIG_FILE_NAME} not found.  Aborting")
        exit(-1)

    except OSError:
        sg.popup(f"OS error occurred trying to open {FORECAST_CONFIG_FILE_NAME}")
        exit(-1)
    except Exception as err:
        sg.popup(f"Unexpected error opening {FORECAST_CONFIG_FILE_NAME} is: ",repr(err))


    for line in file_contents:
        if "$$" in line:
            # Look for comment line (Starts with: '$$') and ignore
            continue
        else:
            try:
                parts = line.split(",")

                if len(parts) > 1:
                    # Remove all ASCII Characters that aren't in the range '0' to '9'
                    fixed_zip = re.sub("[^0-9]", "", parts[0])
                    zip_code_checked = int(fixed_zip)

                    if len(parts) >= 2:
                        # Remove all ASCII Characters that aren't in the range 'A' to 'z'
                        city_name = re.sub(r"[^A-z]", r"", parts[1])
                    else:
                        city_name = "Unknown"

                found_locations[zip_code_checked] = city_name
            finally:
                continue
    if len(found_locations) < 1:
        sg.popup(
            "Could not find any 'ZipCode / City' pairs in the configuration file.\nProgram will now end."
        )
        exit(-1)

    return found_locations


# -----[ Weather API ]---------------------------------------------------------

def get_weather_forecast(zip_code_to_lookup: int) -> dict:

    # tic = time.perf_counter()
    # Sample API Call, complete, for 3 days,
    # https://api.weatherapi.com/v1/forecast.json?key=| Your Key Here |&q=95492&days=3&aqi=no&alerts=no

    preamble = (
        "https://api.weatherapi.com/v1/forecast.json?key=" + WEATHER_API_KEY + "&q="
    )
    
    # The free API only allows 3 days of forecast. We don't want AQI or Alerts
    postamble = "&days=3&aqi=no&alerts=no"

    api_url = preamble + str(zip_code_to_lookup) + postamble

    data_read_is_ok = False
    while not data_read_is_ok:
        try:
            with urlopen(api_url, timeout=4) as response:
                source_data = response.read()
                data_read_is_ok = True

        except Exception as err:
            r = sg.popup_ok_cancel(f"Error Reading Weather API = {str(err)}\nTry again?")
            if r == "OK":
                continue
            else:
                exit(-1)

    try:
        raw_data = json.loads(source_data)

        forecast_data = {}
        # The free API only allows 3 days of Forecasts
        for day in (0, 1, 2):

            daily_temp_data = []
            daily_wind_data = []
            nested_dict = {}
            for hour in range(0, 24):
                
                
                temp_at_hour = raw_data["forecast"]["forecastday"][day]["hour"][hour][
                    "temp_f"
                ]
                daily_temp_data.append(temp_at_hour)
                
                wind_at_hour = raw_data["forecast"]["forecastday"][day]["hour"][hour][
                    "wind_mph"
                ]
                daily_wind_data.append(wind_at_hour)

            # t_dict = {"temp": daily_temp_data}
            # w_dict = {"wind": daily_wind_data}
                
            nested_dict['temp'] = daily_temp_data
            nested_dict['wind'] = daily_wind_data
                
            forecast_data.update({day: nested_dict})

    except Exception as err:
        print(f"JSON parse exception = {str(err)}")
        return []

    return forecast_data


# -----[ Plot Functions ]------------------------------------------------------

def create_plots() -> tuple:
    fig = matplotlib.figure.Figure(figsize=(11, 7))
    ax_top = fig.add_subplot(211)
    ax_bot = fig.add_subplot(212)
    ax_top.clear()
    ax_bot.clear()
    return fig, ax_top, ax_bot


def clear_plots(fig_h, ax_top_h, ax_bot_h):
    ax_top_h.clear()
    ax_bot_h.clear()


def label_plots(fig_h, ax_top_h, ax_bot_h):
    # Build x axis data for the hours of the day in AM/PM, 12 Hour format.
    x_ticks_labels = [
        "M","1","2","3","4","5","6","7","8","9","10","11","N","1","2","3","4","5","6","7","8","9","10","11",
        ]

    x = np.linspace(0, 23, 24)

    ax_top_h.set_xticks(x)
    ax_top_h.set_xticklabels(x_ticks_labels, rotation="horizontal", fontsize=14)
    
    ax_bot_h.set_xticks(x)
    ax_bot_h.set_xticklabels(x_ticks_labels, rotation="horizontal", fontsize=14)

    # fig_h.supylabel("Temperature [Deg F]", fontsize=14)
    # ax.set_ylabel('YLabel1 %d' % i)
    ax_top_h.set_ylabel("Temperature [Deg F]", fontsize=14)
    ax_bot_h.set_ylabel("Wind Speed [MPH]", fontsize=14)
    
    fig_h.supxlabel("Hour", fontsize=14)
    # fig_h.suptitle("Title") # This would display the title


def update_plot(fig_h, ax_top_h, ax_bot_h, plot_data_dict):
    """_summary_

    Args:
        fig_h (_type_): _description_
        ax_h (_type_): _description_
        data_dict (dict): Structure  city_name:list_of_temps_for_day
    """

    # There 'should be' only one set of data in the list, so break after first key
    x_list = np.linspace(0, 23, 24)
    for key in plot_data_dict:
        temp_list = plot_data_dict[key]['temp']
        ax_top_h.plot(x_list, temp_list, label=str(key))
        
        wind_list = plot_data_dict[key]['wind']
        ax_bot_h.plot(x_list, wind_list, label=str(key))
        break


def finish_plots(fig_h, ax_top_h, ax_bot_h):
    ax_top_h.legend(loc="upper left")
    ax_top_h.grid()
    ax_bot_h.grid()
    fig_h.tight_layout()
    fig_h.canvas.draw()
    fig_h.canvas.flush_events()


# -----[ MatplotLib Mapper to Window ]-----------------------------------------

def draw_figure(canvas, figure) -> FigureCanvasTkAgg:
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


# -----[ PySimpleGui Layout Code ]---------------------------------------------

# define the window layout
layout = [
    [sg.Text("Forecast for: xx/xx/xxxx", key="-Title-")],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Previous Day", key="-Prev-"), sg.Button("Next Day", key="-Next-")],
]


# -----[ Main ]----------------------------------------------------------------

def main():

    # day_counter bounding
    def bound_day_counter():
        nonlocal day_counter
        
        # Set Prev and Next button state logic
        if day_counter <= 0:
            day_counter = 0
            window["-Prev-"].update(disabled=True)
        else:
            window["-Prev-"].update(disabled=False)

        if day_counter >= 2:
            day_counter = 2
            window["-Next-"].update(disabled=True)
        else:
            window["-Next-"].update(disabled=False)


    # Update the window title to the correct date
    def update_window_title(day: int):
        current_date_info = datetime.now() + timedelta(days=day)
        plot_year = current_date_info.year
        plot_month = current_date_info.month
        plot_day = current_date_info.day
        date_str = "Forecast for: " + str(plot_month) + "/" + str(plot_day) + "/" + str(plot_year)
        window["-Title-"].update(date_str)


    # Update plots for the correct day
    def plots_for_selected_day(day_to_plot: int):
        
        clear_plots(fig, ax_top, ax_bot)

        # update_plot(fig, ax, legend, temp_data)
        for zip_code in forecast_zip_cities.keys():
            forecast_dict = forecast_data_total.get(zip_code)

            day_temp_data = forecast_dict[day_to_plot]

            city_key = forecast_zip_cities[zip_code]
            city_temp_data = {city_key: day_temp_data}
            #city_temp_data.update({city_key: day_temp_data})

            update_plot(fig, ax_top, ax_bot, city_temp_data)

        label_plots(fig, ax_top, ax_bot)
        finish_plots(fig, ax_top, ax_bot)


    # ----- Plot object Creation - 1st time -----------------------------------
    fig, ax_top, ax_bot = create_plots()
    label_plots(fig, ax_top, ax_bot)
    finish_plots(fig, ax_top, ax_bot)


    # ----- Read the configuration file ---------------------------------------
    forecast_zip_cities = get_the_forecast_locations()


    # ----- Read the Weather API and parse out the data -----------------------
    forecast_data_total = {}
    forecast_by_zipcode = []
    for zip_code in forecast_zip_cities:
        # Get the zip code forecast on all days
        # forecast_by_zipcode.clear()
        forecast_by_zipcode = get_weather_forecast(zip_code)

        forecast_data_total.update({zip_code: forecast_by_zipcode})


    # ----- Create the form and show it ---------------------------------------
    window = sg.Window(
        "Weather Forcast",
        layout,
        finalize=True,
        element_justification="center",
        font="Helvetica 14",
        location=(200, 50),
    )


    # Add the 'fig' (the plot handle plot) to the canvas
    #fig_canvas_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)
    draw_figure(window["-CANVAS-"].TKCanvas, fig)


    # ----- Make the first set of plots for day 0 from the config + Weather API data ----
    plots_for_selected_day(0)
    update_window_title(0)


    # ----- GUI Big Loop ------------------------------------------------------

    # Local Variables
    day_counter = 0

    # Initial conditions
    bound_day_counter()
    #day_counter = bound_day_counter(day_counter)

    while True:

        event, values = window.read()

        # Audios Amigo....
        if event == sg.WIN_CLOSED:
            break

        # Handle button clicks
        if event == "-Prev-":
            day_counter -= 1
            bound_day_counter()
            plots_for_selected_day(day_counter)
            update_window_title(day_counter)
            continue

        if event == "-Next-":
            day_counter += 1
            bound_day_counter()
            plots_for_selected_day(day_counter)
            update_window_title(day_counter)
            continue

    window.close()
    print("Normal Exit...")


if __name__ == "__main__":
    main()

# ----- Fini -----
