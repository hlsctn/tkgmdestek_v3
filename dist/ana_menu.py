import sys
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
        self.kullanici_adi = None  # Kullanıcı giriş durumu

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

        # Menü butonları
        menuler = [
            ("Notlarım", self.notlarim),
            ("Yapılacaklar", self.yapilacaklar),
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

        self.setLayout(grid)
        self.adminPanelBtn = None  # Admin panel buton referansı

    # ---------------------------
    # Kullanıcı girişi
    # ---------------------------
    def kullanici_giris(self):
        from moduller.admin import AdminGirisPenceresi
        girisPencere = AdminGirisPenceresi(self)
        girisPencere.exec()  # Başarılı giriş parent üzerinden işlenecek

    def admin_giris_yapildi(self, kullanici):
        self.kullanici_adi = kullanici
        self.merhabaLabel.setText(f"Merhaba {self.kullanici_adi}")
        self.girisBtn.setVisible(False)
        # Admin panel butonunu ekle
        if not self.adminPanelBtn:
            from moduller.admin import AdminPanelPenceresi
            self.adminPanelBtn = QPushButton("Admin Paneli")
            self.adminPanelBtn.clicked.connect(self.ac_admin_panel)
            self.ustBar.addWidget(self.adminPanelBtn)

    def ac_admin_panel(self):
        from moduller.admin import AdminPanelPenceresi
        self.adminPanelPencere = AdminPanelPenceresi()
        self.adminPanelPencere.show()

    # ---------------------------
    # Kullanıcı çıkışı
    # ---------------------------
    def kullanici_cikisi(self):
        self.kullanici_adi = None
        self.girisBtn.setText("Kullanıcı Girişi")
        self.girisBtn.setEnabled(True)
        self.girisBtn.setVisible(True)
        if self.adminPanelBtn:
            self.adminPanelBtn.setParent(None)
            self.adminPanelBtn = None
        self.merhabaLabel.setText("")

    # ---------------------------
    # Menü fonksiyonları
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
        from moduller.genelgeler import GenelgelerPenceresi
        self.genelgelerPencere = GenelgelerPenceresi()
        self.genelgelerPencere.show()

    def duyurular(self):
        from moduller.duyurular import DuyurularPenceresi
        self.duyurularPencere = DuyurularPenceresi()
        self.duyurularPencere.show()

    def yararlibilgi(self):
        from moduller.yararlibilgi import YararliBilgiPenceresi
        self.yararlibilgiPencere = YararliBilgiPenceresi()
        self.yararlibilgiPencere.show()

    def takbis(self):
        from moduller.takbisklavuz import TakbisKlavuzPenceresi
        self.takbisPencere = TakbisKlavuzPenceresi()
        self.takbisPencere.show()


# ---------------------------
# Programı Çalıştır
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaMenu()
    pencere.show()
    sys.exit(app.exec())
