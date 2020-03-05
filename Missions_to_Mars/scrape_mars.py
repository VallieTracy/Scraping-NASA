# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
   executable_path = {"executable_path":r"C:/bin/chromedriver"}
   return Browser('chrome', **executable_path, headless=False) 