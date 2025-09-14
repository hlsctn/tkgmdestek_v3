import sys
import tkinter as tk
from functools import partial
import subprocess

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

# -------------------------------
# Menüler ve linkler
# -------------------------------
MENULER = {
    "Tapu Müdürlüğü GYS": "https://www.tkgmdestek.com.tr/?cat=34",
    "Tapu Sicil Müdür Yardımcısı GYS": "https://www.tkgmdestek.com.tr/?cat=35",
    "Ünvan Değişikliği Sınavı": "https://www.tkgmdestek.com.tr/?cat=40",
    "GYS Sınavları": "https://www.tkgmdestek.com.tr/?cat=46",
    "GYS SAYAÇ": "https://tkgmdestek.com.tr/sayac"
}

# -------------------------------
# PyQt Tarayıcı Penceresi
# -------------------------------
class Browser(QMainWindow):
    def __init__(self, url, baslik):
        super().__init__()
        self.setWindowTitle(baslik)
        self.resize(1100, 700)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)

def pyqt_pencere_ac(url, baslik):
    """PyQt tarayıcı penceresini ayrı işlem olarak açar"""
    exe_path = sys.argv[0]  # exe veya python dosyasının kendisi
    subprocess.Popen([exe_path, url, baslik])

# -------------------------------
# Tkinter GYS Penceresi
# -------------------------------
def gys_pencere():
    root = tk.Toplevel()
    root.title("Görevde Yükselme (GYS)")
    root.geometry("420x320")

    info = tk.Label(root, text="Aşağıdaki menülerden birini seçin.")
    info.pack(pady=8)

    buton_kapsul = tk.Frame(root)
    buton_kapsul.pack(fill="both", expand=True, padx=12, pady=8)

    for ad, url in MENULER.items():
        btn = tk.Button(
            buton_kapsul,
            text=ad,
            width=38,
            height=2,
            command=partial(pyqt_pencere_ac, url, ad)
        )
        btn.pack(pady=5)

# -------------------------------
# PyQt tarafı bağımsız çalıştırma
# -------------------------------
def pyqt_main():
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        baslik = sys.argv[2]

        app = QApplication(sys.argv)
        window = Browser(url, baslik)
        window.show()
        sys.exit(app.exec())

# -------------------------------
# Ana kontrol
# -------------------------------
if __name__ == "__main__":
    # Eğer argüman var ise PyQt penceresini aç
    if len(sys.argv) >= 3:
        pyqt_main()
    else:
        # Tkinter penceresini aç
        root = tk.Tk()
        root.withdraw()  # Tkinter ana penceresini gizle
        gys_pencere()
        root.mainloop()
