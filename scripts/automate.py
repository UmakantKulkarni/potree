#!/usr/bin/env python3
import os
import sys
import time
import json
import argparse
from multiprocessing import Process
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

CHROME_DRIVER = '/usr/local/bin/chromedriver'
#Chrome options - https://chromedriver.chromium.org/capabilities & https://peter.sh/experiments/chromium-command-line-switches/


def chrome_renderer(download_dir="", example_uri="", sleep_duration=10):
    # enable browser logging
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--enable-gpu')
    #chrome_options.add_argument("--headless=new")
    #https://stackoverflow.com/questions/57599776/download-file-through-google-chrome-in-headless-mode
    chrome_options.add_experimental_option("excludeSwitches",
                                           ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    params = {'behavior': 'allow', 'downloadPath': download_dir}
    #chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("window-size=1080,720")
    chrome_options.add_experimental_option("prefs", { \
    #"profile.default_content_settings.popups": 0,

    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    #"profile.default_content_setting_values.media_stream_mic": 1,
    #"profile.default_content_setting_values.media_stream_camera": 1,
    #"profile.default_content_setting_values.geolocation": 1,
    #"profile.default_content_setting_values.notifications": 1
    })
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--allow-file-access")

    chrome_service = Service(CHROME_DRIVER, log_path=os.path.devnull)
    driver = Chrome(options=chrome_options,
                    service=chrome_service,
                    service_log_path=None)

    #get method to launch the URL
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    driver.get(example_uri)
    time.sleep(sleep_duration)
    driver.execute_script(
        'el = document.elementFromPoint(440, 120); el.click();')

    driver.execute_script(
        'document.querySelector("#potree_annotation_container > div:nth-child(1) > div.annotation-titlebar > span").click()'
    )
    time.sleep(sleep_duration)

    driver.execute_script(
        'document.querySelector("#potree_annotation_container > div:nth-child(2) > div.annotation-titlebar > span").click()'
    )
    time.sleep(sleep_duration)

    driver.execute_script(
        'document.querySelector("#potree_annotation_container > div:nth-child(3) > div.annotation-titlebar > span").click()'
    )
    time.sleep(sleep_duration)

    driver.execute_script(
        'document.querySelector("#potree_annotation_container > div:nth-child(4) > div.annotation-titlebar > span").click()'
    )
    time.sleep(sleep_duration)

    driver.execute_script(
        'document.querySelector("#potree_annotation_container > div:nth-child(5) > div.annotation-titlebar > span").click()'
    )
    time.sleep(sleep_duration)

    #to refresh the browser
    #driver.refresh()
    #time.sleep(SLEEP_TIME)

    #to close the browser
    driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        __doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--server_ip', '-i')
    parser.add_argument('--server_port', '-p', type=int, default=3000)
    parser.add_argument('--example', '-e', default="dc_static")
    parser.add_argument('--sleep_duration', '-w', type=int, default=10)
    parser.add_argument('--download_dir', '-d', default="/tmp")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    example_uri = "http://{}:{}/examples/{}.html".format(
        args.server_ip, str(args.server_port), args.example)
    chrome_renderer(args.download_dir, example_uri, args.sleep_duration)
