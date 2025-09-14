import os
import sys
import requests
from PyQt6.QtWidgets import QMessageBox

# -------------------------------
# GitHub raw base ve exe dosyalar
# -------------------------------
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/hlsctn/tkgmdestek_v3/main/moduller/"
DOSYALAR = [
    "NotDefteri.exe",
    "YapilacaklarListesi.exe",
    "GYS.exe"
]

def dosya_guncelle(dosya):
    url = GITHUB_RAW_BASE + dosya
    try:
        r = requests.get(url)
        r.raise_for_status()

        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.getcwd()
        yol = os.path.join(base_path, "moduller", dosya)
        os.makedirs(os.path.dirname(yol), exist_ok=True)

        with open(yol, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"{dosya} güncellenemedi: {e}")
        return False

def kontrol_ve_guncelle(parent=None):
    guncellenecek = []

    for dosya in DOSYALAR:
        url = GITHUB_RAW_BASE + dosya
        try:
            r = requests.head(url)
            remote_size = int(r.headers.get("Content-Length", 0))
        except:
            continue

        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.getcwd()
        dosya_yolu = os.path.join(base_path, "moduller", dosya)

        if not os.path.exists(dosya_yolu):
            guncellenecek.append(dosya)
        else:
            local_size = os.path.getsize(dosya_yolu)
            if local_size != remote_size:
                guncellenecek.append(dosya)

    if guncellenecek:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Güncelleme Mevcut")
        msg.setText(f"{len(guncellenecek)} dosya güncellenebilir. Güncellemek ister misiniz?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        cevap = msg.exec()

        if cevap == QMessageBox.StandardButton.Yes:
            for dosya in guncellenecek:
                dosya_guncelle(dosya)
            QMessageBox.information(parent, "Güncelleme Tamam", "Dosyalar güncellendi!")
