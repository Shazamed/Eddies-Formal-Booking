#!/usr/bin/env python3
from dateutil import parser
import datetime
import time
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def launch_webdriver(date):
    script_directory = pathlib.Path().absolute()

    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={script_directory}\\selenium")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://dbs.st-edmunds.cam.ac.uk/secure/meals/Main.aspx")
    time.sleep(5)

    calendar_title = driver.find_element(By.CLASS_NAME, "CalendarTitle")
    current_month_year = calendar_title.text[2:-2]
    current_month = parser.parse(current_month_year)

    while date.month > current_month.month:
        next_month_elem = driver.find_element(By.CSS_SELECTOR, 'a[title="Go to the next month"]')
        next_month_elem.click()
        calendar_title = driver.find_element(By.CLASS_NAME, "CalendarTitle")
        current_month_year = calendar_title.text[2:-2]
        current_month = parser.parse(current_month_year)

    date_elem = driver.find_element(By.CSS_SELECTOR, f'a[title="{date.day} {date.strftime("%B")}"]')
    date_elem.click()
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    date_input = input("Enter a date to book:")
    booking_date = parser.parse(date_input).replace(hour=0, minute=0, second=0, microsecond=0)
    current_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    day_diff = booking_date - current_date

    if day_diff.days > 14:
        print("Not available yet")
    elif day_diff.days < 0:
        print("Your selected date is in the past!")
    else:
        launch_webdriver(booking_date)





