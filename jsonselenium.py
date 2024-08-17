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
    driver.get("https://simpkk.kabsemarangtourism.id/index.php/login")  # Sesuaikan dengan URL halaman login Anda

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

    # # Tunggu beberapa saat untuk memastikan halaman berikutnya dimuat
    # WebDriverWait(driver, 10).until(
    #     EC.title_contains("Dashboard")  # Sesuaikan dengan judul halaman setelah login
    # )
    WebDriverWait(driver, 10)
    # Cetak judul halaman setelah login
    # nama_admin = driver.find_element(By.XPATH, "//ul[@class='navbar-nav ml-auto']//a[@class='nav-link']")
  #  ok
    # nama_admin = driver.find_element(By.XPATH, "//div[@class='card dashboard text-white bg-primary o-hidden h-100']//h5")
    # print("Alamat url halaman setelah login:", driver.current_url)
    # print("Nama Admin: ", nama_admin.text)

    driver.get("https://simpkk.kabsemarangtourism.id/admin/dawis")  # Sesuaikan dengan URL halaman baru
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table[@id='dataTable']")))
    # Temukan elemen select untuk menampilkan jumlah entri
    select_elem = driver.find_element(By.NAME, "dataTable_length")
    select = Select(select_elem)
    # Tambahkan opsi baru secara manual
    driver.execute_script("arguments[0].innerHTML += '<option value=\"20000\">20000</option>';", select_elem)

    # Pilih opsi 20000 dengan cara mengirimkan keyboard keys pada elemen select
    select_elem.send_keys(Keys.DOWN)  # Memastikan kursor di bawah
    select_elem.send_keys(Keys.RETURN)  # Memilih opsi 20000
    select.select_by_value('20000')

        # Tunggu beberapa saat untuk memastikan tabel baru dimuat
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='dataTable']/tbody/tr")))

    jml_warga = driver.find_element(By.XPATH, "//table[@id='dataTable']").text
    # Pisahkan baris menjadi list
    rows = jml_warga.split('\n')

    # Filter data berdasarkan Nama_Kecamatan = Sumowono dan Nama_Desa/Kelurahan = Lanjan
    filtered_rows = []
    for row in rows:
        cols = row.split()
        if len(cols) >= 3 and cols[0] == 'Sumowono' and (cols[1] == 'Candigaron' or cols[1] == 'Lanjan' or cols[1] == 'Kebonagung' or cols[1] == 'Ngadikerso' or cols[1] == 'Jubelan' or cols[1] == 'Sumowono' or cols[1] == 'Trayu' or cols[1] == 'Kemitir' or cols[1] == 'Duren' or cols[1] == 'Pledokan' or cols[1] == 'Mendongan' or cols[1] == 'Bumen' or cols[1] == 'Losari' or cols[1] == 'Kemawi' or cols[1] == 'Piyanggang' or cols[1] == 'Keseneng'):
            filtered_rows.append(row)

    # Cetak hasil filter
    # if filtered_rows:
    #     print("Hasil Filter:")
    #     for row in filtered_rows:
    #         print(row)
    # else:
    #     print("Tidak ada hasil yang cocok dengan filter.")
    

    # Inisialisasi dictionary untuk menyimpan jumlah setiap desa
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

    # Hitung jumlah baris untuk setiap desa (Anda perlu menambahkan logika ini)
    # Contoh:
    for row in filtered_rows:
        cols = row.split()
        if len(cols) >= 3:
            desa = cols[1]
            if desa in desa_counts:
                desa_counts[desa] += 1

    # Jumlahkan total baris untuk setiap desa
    total_kebonagung = desa_counts["Kebonagung"]
    total_candigaron = desa_counts["Candigaron"]
    total_ngadikerso = desa_counts["Ngadikerso"]
    total_lanjan = desa_counts["Lanjan"]
    total_jubelan = desa_counts["Jubelan"]
    total_sumowono = desa_counts["Sumowono"]
    total_trayu = desa_counts["Trayu"]
    total_kemitir = desa_counts["Kemitir"]
    total_duren = desa_counts["Duren"]
    total_pledokan = desa_counts["Pledokan"]
    total_mendongan = desa_counts["Mendongan"]
    total_bumen = desa_counts["Bumen"]
    total_losari = desa_counts["Losari"]
    total_kemawi = desa_counts["Kemawi"]
    total_piyanggang = desa_counts["Piyanggang"]
    total_keseneng = desa_counts["Keseneng"]

    # Buat DataFrame
    data = {
        "Desa": ["Kebonagung", "Candigaron", "Ngadikerso", "Lanjan", "Jubelan", "Sumowono", "Trayu", "Kemitir", "Duren", "Pledokan", "Mendongan", "Bumen", "Losari", "Kemawi", "Piyanggang", "Keseneng"],
        "Dawis": [total_kebonagung, total_candigaron, total_ngadikerso, total_lanjan, total_jubelan, total_sumowono, total_trayu, total_kemitir, total_duren, total_pledokan, total_mendongan, total_bumen, total_losari, total_kemawi, total_piyanggang, total_keseneng]
    }
    df1 = pd.DataFrame(data)

    # Tampilkan DataFrame
    df1.index = df1.index + 1

    # Simpan data dalam format JSON
    with open('output.json', 'w') as f:
        json.dump(df1.to_dict(orient='records'), f, indent=4)

finally:
    driver.quit()
