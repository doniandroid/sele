# import json
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import pandas as pd
# chrome_driver_path = "/usr/local/bin/chromedriver"
# # Konfigurasi opsi Chrome
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Menjalankan Chrome dalam mode headless

# # Setup selenium webdriver
# driver_service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=driver_service, options=chrome_options)
# # driver = webdriver.Chrome()
# driver.get('http://example.com')

# # Contoh data yang ingin diekstrak
# data = {
#     'title': driver.title,
#     'url': driver.current_url
# }
# with open('output.json', 'w') as f:
#     json.dump(data, f)

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

chrome_driver_path = "/usr/local/bin/chromedriver"
# Konfigurasi opsi Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan Chrome dalam mode headless

# Inisialisasi driver Chrome
driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

try:
    # Buka URL halaman login
    driver.get("https://simpkk.kabsemarangtourism.id/index.php/login")

    # Tunggu hingga elemen input username muncul
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Temukan elemen input untuk username
    username_input = driver.find_element(By.NAME, "username")
    # Isi input username
    username_input.send_keys("sumowono")

    # Temukan elemen input untuk password
    password_input = driver.find_element(By.NAME, "password")
    # Isi input password
    password_input.send_keys("123")

    # Temukan tombol Sign In dengan tag <button>
    sign_in_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")

    # Klik tombol Sign In
    sign_in_button.click()

    # Navigasi ke halaman yang diperlukan
    driver.get("https://simpkk.kabsemarangtourism.id/admin/dawis")

    # Tunggu hingga tabel muncul
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table[@id='dataTable']")))

    # Temukan elemen select dan pilih jumlah entri
    select_elem = driver.find_element(By.NAME, "dataTable_length")
    select = Select(select_elem)
    driver.execute_script("arguments[0].innerHTML += '<option value=\"20000\">20000</option>';", select_elem)
    select.select_by_value('20000')

    # Tunggu beberapa saat untuk memastikan tabel baru dimuat
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='dataTable']/tbody/tr")))

    # Ambil data dari tabel
    rows = driver.find_elements(By.XPATH, "//table[@id='dataTable']/tbody/tr")
    
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append({
            "Nama_Kecamatan": cols[0].text,
            "Nama_Desa/Kelurahan": cols[1].text
        })

    # Convert data ke DataFrame
    df = pd.DataFrame(data)

    # Hitung jumlah entri per desa
    desa_counts = df['Nama_Desa/Kelurahan'].value_counts()

    # Buat DataFrame untuk hasil akhir
    data_summary = {
        "Desa": desa_counts.index,
        "Jumlah": desa_counts.values
    }
    df_summary = pd.DataFrame(data_summary)

    # Tampilkan DataFrame
    df_summary.index = df_summary.index + 1

    # Desain ulang data_counts
    desa_counts = {
        "Kebonagung": 0,
        "Candigaron": 0,
        "Ngadikerso": 0,
        "Lanjan": 0,
        "Jubelan": 0,
        "Sumowono": 0,
        "Trayu": 0,
        "Kemitir": 0,
        "Duren": 0,
        "Pledokan": 0,
        "Mendongan": 0,
        "Bumen": 0,
        "Losari": 0,
        "Kemawi": 0,
        "Piyanggang": 0,
        "Keseneng": 0
    }

    # Hitung jumlah baris untuk setiap desa
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 2:
            desa = cols[1].text
            if desa in desa_counts:
                desa_counts[desa] += 1

    # Buat DataFrame dari desa_counts
    data = {
        "Desa": list(desa_counts.keys()),
        "Dawis": list(desa_counts.values())
    }
    df1 = pd.DataFrame(data)

    # Tampilkan DataFrame
    df1.index = df1.index + 1

    with open('output.json', 'r') as f:
        existing_data = json.load(f)
    except FileNotFoundError:
    existing_data = {}
    existing_data.update(df1)
        
    # Simpan data dalam format JSON
    with open('output.json', 'w') as f:
        json.dump(existing_data.to_dict(orient='records'), f, indent=4)

finally:
    driver.quit()

