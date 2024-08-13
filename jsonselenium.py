import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
# driver_service = ChromeService(executable_path='/usr/local/bin/chromedriver')
chrome_driver_path = "/usr/local/bin/chromedriver"
# Konfigurasi opsi Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan Chrome dalam mode headless

# Setup selenium webdriver
driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=chrome_options)
# driver = webdriver.Chrome()
driver.get('http://example.com')

# Contoh data yang ingin diekstrak
data = {
    'title': driver.title,
    'url': driver.current_url
}

# Simpan data dalam format JSON
with open('output.json', 'w') as f:
    json.dump(data, f)

driver.quit()
