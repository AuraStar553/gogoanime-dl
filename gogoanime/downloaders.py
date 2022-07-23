"""
@author: AuraMoon55
@contact: garganshul553@gmail.com
@license: MIT License, see LICENSE file
Copyright (C) 2022
"""


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests, time, zipfile, io, os


def get_readable_time(seconds) -> str:
  seconds = int(seconds)
  count = 0
  ping_time = ""
  time_list = []
  time_suffix_list = ["s", "m", "h", "days"]
  while count < 4:
    count += 1
    if count < 3:
      remainder, result = divmod(seconds, 60)
    else:
      remainder, result = divmod(seconds, 24)
    if seconds == 0 and remainder == 0:
      break
    time_list.append(int(result))
    seconds = int(remainder)

  for i, _ in enumerate(time_list):
    time_list[i] = str(time_list[i]) + time_suffix_list[i]

  if len(time_list) == 4:
    ping_time += time_list.pop() + ", "

  time_list.reverse()
  ping_time += ":".join(time_list)
  return ping_time



def get_chromedriver():
  curr_dir = "./"

  def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  if is_exe (curr_dir + "\chromedriver.exe"):
    return curr_dir + "\chromedriver.exe"
  for path in os.environ["PATH"].split(os.pathsep):
    exe_file = os.path.join(path, "chromedriver.exe")
    if is_exe(exe_file):
      print("chromedriver exist and is executable", exe_file)
      return exe_file
  url = "https://chromedriver.storage.googleapis.com/72.0.3626.69/chromedriver_win32.zip"
  r = requests.get(url)
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall()
  chromedriver = os.path.join(curr_dir, "chromedriver.exe")
  return chromedriver



def dlfiles(File, url):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  browser = webdriver.Chrome('chromedriver',options=chrome_options)
  try:
    t1 = time.time()
    timeout = 100
    browser.get(url)
    element = browser.find_element(By.ID, "download")
    element.click()
    what_is_this = WebDriverWait(browser, timeout).until(
      EC.presence_of_element_located(
        (By.CLASS_NAME, "clickdownload")
      )
    )
    t2 = time.time() - t1
    for x in browser.find_elements(By.CLASS_NAME, "clickdownload"):
      option = input(f"Do You Want To Download This Anime in {x.get_property('text')}p Quality?\nType y/n")
      if option.lower()[0] == "y":
        b = requests.get(x.get_property("href"))
        open(f'{File}-{x.get_property("text")}p.mp4',"wb").write(b.content)
        print(f"Time Taken To Download: {get_readable_time(time.time()-t2)}")
        return browser.quit()
      else:
        t2 = time.time()
        pass
    browser.quit()
    
  except TimeoutException as x:
    browser.quit()
    return print(x)
