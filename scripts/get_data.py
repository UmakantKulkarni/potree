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

pov_2_camera_dict = {
    "soldier_static_old": {
        11: [1, 2, 3, 4, 5, 7],
        14: [1, 2, 3, 5, 6, 7],
        15: [2, 3, 4, 5, 6, 7]
    },
    "soldier_static": {
        10: [1, 2, 3, 4, 5, 6],
        11: [1, 2, 3, 4, 5, 6],
        12: [1, 2, 3, 4, 5, 6],
        13: [1, 2, 3, 4, 5, 6],
        14: [1, 2, 3, 4, 5, 6],
        15: [1, 2, 3, 4, 5, 6],
    },
    "soldier_dynamic": {
        12: [1, 2, 3, 4, 5, 6],
        13: [2, 3, 4, 5, 6, 7],
        14: [1, 2, 3, 5, 6, 7]
    }
}


def chrome_launcher(download_dir=""):
    # enable browser logging
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--enable-gpu')
    chrome_options.add_argument("--headless=new")
    #https://stackoverflow.com/questions/57599776/download-file-through-google-chrome-in-headless-mode
    chrome_options.add_experimental_option("excludeSwitches",
                                           ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    params = {'behavior': 'allow', 'downloadPath': download_dir}
    #chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument("window-size=1920,1080")
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

    return driver


def chrome_renderer(example_uri="", sleep_duration=5, driver=None, cam_pos = 0, p = 0):

    model = example_uri.split('/')[-1].split('.')[0]

    if "sd_test" in example_uri:
        driver.get(example_uri)
        time.sleep(sleep_duration)

    elif "dc_static" in example_uri:
        driver.get(example_uri)
        time.sleep(sleep_duration)
        driver.execute_script(
            'el = document.elementFromPoint(440, 120); el.click();')

        p = 1
        while p < 6:
            driver.execute_script(
                'document.querySelector("#potree_annotation_container > div:nth-child({}) > div.annotation-titlebar > span").click()'
                .format(p))
            time.sleep(sleep_duration)
            p = p + 1

    elif "soldier" in example_uri:
        driver.get(example_uri)
        time.sleep(30)
        driver.execute_script(
            'document.querySelector("#navigation > img:nth-child({})").click()'
            .format(cam_pos))
        time.sleep(10)
        driver.execute_script(
            'document.querySelector("#potree_annotation_container > div:nth-child({}) > div.annotation-titlebar > span").click()'
            .format(p))
        time.sleep(20)

    #to refresh the browser
    #driver.refresh()
    #time.sleep(SLEEP_TIME)

    #to close the browser
    driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        __doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--server_ip', '-i', default="127.0.0.1")
    parser.add_argument('--server_port', '-p', type=int, default=12345)
    parser.add_argument('--example', '-e', default="soldier_static")
    parser.add_argument('--sleep_duration', '-w', type=int, default=5)
    parser.add_argument('--download_dir', '-d', default="/tmp")
    parser.add_argument('--cam_pos', '-c', type=int, default=10)
    parser.add_argument('--target_pos', '-t', type=int, default=1)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()

    startFrame = 536
    EndFrame = 835
    frame_num = startFrame
    if "sd_test" in args.example:
        while frame_num <= EndFrame:
            example_uri = "http://{}:{}/examples/{}.html?frame_num={}".format(
                args.server_ip, str(args.server_port), args.example, frame_num)
            driver = chrome_launcher(download_dir=args.download_dir)
            chrome_renderer(example_uri, args.sleep_duration, driver)
            frame_num = frame_num + 1
    elif "soldier_static" in args.example:
        example_uri = "http://{}:{}/examples/{}.html".format(
                    args.server_ip, str(args.server_port), args.example)
        driver = chrome_launcher(download_dir=args.download_dir)
        chrome_renderer(example_uri, args.sleep_duration, driver, args.cam_pos,args.target_pos)
