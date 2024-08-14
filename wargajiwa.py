from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

# Data desa
data_desa = [
    {"nama": "Kebonagung", "username": "kebonagungsumowono", "password": "123"},
    {"nama": "Candigaron", "username": "candigaronsumowono", "password": "123"},
    {"nama": "Ngadikerso", "username": "ngadikersosumowono", "password": "12345"},
    {"nama": "Lanjan", "username": "lanjansumowono", "password": "123"},
    {"nama": "Jubelan", "username": "jubelansumowono", "password": "123"},
    {"nama": "Sumowono", "username": "sumowonosumowono", "password": "sumowono123"},
    {"nama": "Trayu", "username": "trayusumowono", "password": "123"},
    {"nama": "Kemitir", "username": "kemitirsumowono", "password": "123"},
    {"nama": "Duren", "username": "durensumowono", "password": "123"},
    {"nama": "Pledokan", "username": "pledokansumowono", "password": "123"},
    {"nama": "Mendongan", "username": "mendongansumowono", "password": "123"},
    {"nama": "Bumen", "username": "bumensumowono", "password": "123"},
    {"nama": "Losari", "username": "losarisumowono", "password": "123"},
    {"nama": "Kemawi", "username": "kemawisumowono", "password": "123"},
    {"nama": "Piyanggang", "username": "piyanggangsumowono", "password": "123"},
    {"nama": "Keseneng", "username": "kesenengsumowono", "password": "123"}
]

# Konfigurasi opsi Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inisialisasi WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# List untuk menyimpan hasil
hasil = []

try:
    for desa in data_desa:
        # Buka URL halaman login
        driver.get("https://simpkk.kabsemarangtourism.id/index.php/login")

        # Tunggu hingga elemen input username muncul
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        # Isi username dan password
        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys(desa["username"])
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(desa["password"])

        # Klik tombol Sign In
        sign_in_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")
        sign_in_button.click()

        WebDriverWait(driver, 10)

        # Pindah ke halaman KRT
        driver.get("https://simpkk.kabsemarangtourism.id/users/registrasi")
        WebDriverWait(driver, 10)
        jml_krt = driver.find_element(By.XPATH, "//div[@class='dataTables_info']").text

        # Pindah ke halaman warga TP PPK
        driver.get("https://simpkk.kabsemarangtourism.id/users/userslistwarga")
        WebDriverWait(driver, 10)
        jml_warga = driver.find_element(By.XPATH, "//div[@class='dataTables_info']").text

        # Simpan hasil
        hasil.append({
            "Desa": desa["nama"],
            "KRT": jml_krt.replace("Showing 1 to 10 of ", "").replace(" entries", "").replace(",", ""),
            "Warga_TP_PPK": jml_warga.replace("Showing 1 to 10 of ", "").replace(" entries", "").replace(",", "")
        })

        df2 = pd.DataFrame(hasil)
        df2.index = df2.index + 1
        print(df2)
        with open('output.json', 'r') as f:
            existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {}
            existing_data.update(df2)
          # Simpan data dalam format JSON
         with open('output.json', 'w') as f:
             json.dump(existing_data.to_dict(orient='records'), f, indent=4)
finally:
    # Tutup browser
    driver.quit()

# # Buat DataFrame dari hasil
# df2 = pd.DataFrame(hasil)
# df2.index = df2.index + 1
# print(df2)
