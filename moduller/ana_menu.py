import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QLabel, QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class AnaMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TKGMDESTEK v3 - Masaüstü Uygulaması")
        self.setGeometry(400, 200, 700, 400)
        self.setStyleSheet("background-color: orange;")
        self.kullanici_adi = None

        # Üst bar
        self.ustBar = QHBoxLayout()
        self.merhabaLabel = QLabel("")
        self.merhabaLabel.setFont(QFont("Arial", 10))
        self.girisBtn = QPushButton("Kullanıcı Girişi")
        self.girisBtn.clicked.connect(self.kullanici_giris)
        self.ustBar.addStretch()
        self.ustBar.addWidget(self.merhabaLabel)
        self.ustBar.addWidget(self.girisBtn)

        # Başlık
        self.label = QLabel("TKGMDESTEK v3", self)
        self.label.setFont(QFont("Arial", 16, weight=QFont.Weight.Bold))
        self.label.setStyleSheet("color: white; margin-bottom: 20px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Grid düzeni
        grid = QGridLayout()
        grid.addLayout(self.ustBar, 0, 0, 1, 3)
        grid.addWidget(self.label, 1, 0, 1, 3)

        # ✅ Önce sabit modül butonlarını ekleyelim
        menuler = [
            ("Notlarım (Modül)", self.notlarim),
            ("Yapılacaklar (Modül)", self.yapilacaklar),
            ("Genelgeler", self.genelgeler),
            ("Duyurular", self.duyurular),
            ("Yararlı Bilgiler", self.yararlibilgi),
            ("TAKBİS Kılavuzları", self.takbis),
        ]

        row, col = 2, 0
        for isim, fonksiyon in menuler:
            btn = QPushButton(isim)
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet(
                "background-color: white; color: black; padding: 10px; border-radius: 10px;"
            )
            btn.clicked.connect(fonksiyon)
            grid.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # ✅ Şimdi moduller klasöründeki tüm exe dosyalarını bulup otomatik ekleyelim
        exe_klasoru = os.path.join(os.getcwd(), "moduller")
        if os.path.exists(exe_klasoru):
            for dosya in os.listdir(exe_klasoru):
                if dosya.endswith(".exe"):
                    isim = os.path.splitext(dosya)[0]
                    btn = QPushButton(f"{isim} (EXE)")
                    btn.setFont(QFont("Arial", 12))
                    btn.setStyleSheet(
                        "background-color: #e6e6e6; color: black; padding: 10px; border-radius: 10px;"
                    )
                    btn.clicked.connect(lambda _, d=dosya: self.exe_ac(d))
                    grid.addWidget(btn, row, col)
                    col += 1
                    if col > 2:
                        col = 0
                        row += 1

        self.setLayout(grid)
        self.adminPanelBtn = None

    # ---------------------------
    # Kullanıcı girişi
    # ---------------------------
    def kullanici_giris(self):
        from moduller import admin
        girisPencere = admin.AdminGirisPenceresi(self)
        girisPencere.exec()

    def admin_giris_yapildi(self, kullanici):
        self.kullanici_adi = kullanici
        self.merhabaLabel.setText(f"Merhaba {self.kullanici_adi}")
        self.girisBtn.setVisible(False)
        if not self.adminPanelBtn:
            from moduller import admin
            self.adminPanelBtn = QPushButton("Admin Paneli")
            self.adminPanelBtn.clicked.connect(self.ac_admin_panel)
            self.ustBar.addWidget(self.adminPanelBtn)

    def ac_admin_panel(self):
        from moduller import admin
        self.adminPanelPencere = admin.AdminPanelPenceresi(self)
        self.adminPanelPencere.show()

    # ---------------------------
    # Modül fonksiyonları
    # ---------------------------
    def notlarim(self):
        from moduller.notdefteri import NotlarimPenceresi
        self.notlarPencere = NotlarimPenceresi()
        self.notlarPencere.show()

    def yapilacaklar(self):
        from moduller.yapilacaklar import YapilacaklarPenceresi
        self.yapilacakPencere = YapilacaklarPenceresi()
        self.yapilacakPencere.show()

    def genelgeler(self):
        from moduller import genelgeler
        self.genelgelerPencere = genelgeler.GenelgelerPenceresi()
        self.genelgelerPencere.show()

    def duyurular(self):
        from moduller import duyurular
        self.duyurularPencere = duyurular.DuyurularPenceresi()
        self.duyurularPencere.show()

    def yararlibilgi(self):
        from moduller import yararlibilgi
        self.yararlibilgiPencere = yararlibilgi.YararliBilgiPenceresi()
        self.yararlibilgiPencere.show()

    def takbis(self):
        from moduller import takbisklavuz
        self.takbisPencere = takbisklavuz.TakbisKlavuzPenceresi()
        self.takbisPencere.show()

    # ---------------------------
    # EXE açma fonksiyonu
    # ---------------------------
    def exe_ac(self, dosya):
        exe_yolu = os.path.join(os.getcwd(), "moduller", dosya)
        if os.path.exists(exe_yolu):
            try:
                subprocess.Popen([exe_yolu])
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"{dosya} açılamadı!\n{e}")
        else:
            QMessageBox.warning(self, "Eksik Dosya", f"{dosya} bulunamadı!")


# ---------------------------
# Programı Çalıştır
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaMenu()
    pencere.show()
    sys.exit(app.exec())
