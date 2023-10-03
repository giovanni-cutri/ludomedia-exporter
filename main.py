import re
import time
import requests
import bs4
import os
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    profile_url = get_profile()
    games = get_games(profile_url)
    data = get_data(games)
    dump(data)
    print("Done.")


def get_profile():
    pattern = re.compile("^https://www\.ludomedia\.it/[a-zA-Z]+-[0-9]+$")
    while 1:
        profile_url = input("Please enter a valid Ludomedia profile: ")
        if re.match(pattern, profile_url):
            return profile_url
        else:
            print("Invalid URL. Try again.\n")


def get_games(profile_url):
    print("Getting profile...")
    driver = webdriver.Firefox()
    driver.get(profile_url + "?v=giochi")
    scroll_webpage(driver)
    print("Gathering games...")
    games = [elem.get_attribute("href") for elem in driver.find_elements(By.CSS_SELECTOR, "a.giocoLink")]
    global username
    username = driver.find_elements(By.CSS_SELECTOR, "title")[0].get_attribute("innerHTML").split("Collezione di ")[-1].split(" - Ludomedia")[0]
    driver.quit()
    return games


def scroll_webpage(driver):
    print("Scrolling webpage...")

    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def get_data(games):

    data = []

    for index, game in enumerate(games):

        print(f"Getting games data [{index + 1}/{len(games)}]...")

        res = requests.get(game)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "lxml")
        
        game_dict = {}

        title = soup.select("meta[property='og:title']")[0].attrs["content"]
        platform = soup.select("title")[0].getText().split(" - ")[1]
        game_dict["Titolo"] = title
        game_dict["Piattaforma"] = platform

        metadata = soup.select("dt")
        for i in metadata:
            type = i.getText()
            if type == "Genere":
                value = i.find_all_next("a")[0].getText()
            elif type == "Link":
                value = i.find_all_next("a")[0].attrs["href"]
            else:
                value = i.find_all_next("dd")[0].getText().strip()
            game_dict[type] = value
        
        data.append(game_dict)

    return data
    

def dump(data):
    print("Dumping data to CSV file...")
    try:
        os.makedirs("data")
    except FileExistsError:
        pass
    keys = list(dict.fromkeys([key for game in data for key in list(game.keys())]))    # flat list, then remove duplicates
    with open(f"data/{username}.csv", "w", newline="", encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


if __name__ == "__main__":
    main()
