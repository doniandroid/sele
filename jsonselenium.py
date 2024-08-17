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

    # Temukan elemen input untuk username dan password
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    
    # Isi input username dan password
    username_input.send_keys("sumowono")
    password_input.send_keys("123")

    # Temukan tombol Sign In dengan tag <button> dan klik
    sign_in_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")
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
    
    # Daftar nama desa yang diinginkan
    desa_target = [
        "Candigaron", "Lanjan", "Kebonagung", "Ngadikerso", "Jubelan", "Sumowono",
        "Trayu", "Kemitir", "Duren", "Pledokan", "Mendongan", "Bumen", "Losari",
        "Kemawi", "Piyanggang", "Keseneng"
    ]

    # Filter data berdasarkan nama desa
    filtered_rows = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 3 and cols[0].text == 'Sumowono' and cols[1].text in desa_target:
            filtered_rows.append({
                "Nama_Kecamatan": cols[0].text,
                "Nama_Desa/Kelurahan": cols[1].text
            })

    # Convert data yang difilter ke DataFrame
    df_filtered = pd.DataFrame(filtered_rows)

    # Tampilkan DataFrame
    print(df_filtered)

    # Simpan data yang difilter dalam format JSON
    with open('filtered_output.json', 'w') as f:
        json.dump(df_filtered.to_dict(orient='records'), f, indent=4)

finally:
    driver.quit()
