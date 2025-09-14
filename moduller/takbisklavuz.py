# moduller/takbisklavuz.py
import os
import subprocess
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox
)
from PyQt6.QtGui import QFont

TAKBIS_KLAVUZ_KLASOR = "moduller/takbisklavuz_dosyalar"

class TakbisKlavuzPenceresi(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAKBİS Kılavuzları")
        self.setGeometry(500, 220, 800, 400)

        mainLayout = QHBoxLayout()

        # Sol panel: Ana kategori
        self.anaKategoriLayout = QVBoxLayout()
        mainLayout.addLayout(self.anaKategoriLayout)

        # Sağ panel: PDF listesi
        self.pdfLayout = QVBoxLayout()
        mainLayout.addLayout(self.pdfLayout)
        self.pdfList = QListWidget()
        self.pdfLayout.addWidget(QLabel("PDF Dosyaları:"))
        self.pdfLayout.addWidget(self.pdfList)
        self.pdfList.itemDoubleClicked.connect(self.pdf_ac)

        self.setLayout(mainLayout)

        # Ana kategoriler
        self.ana_kategoriler = [
            "Mülkiyet İşlemleri",
            "Şerh İşlemleri",
            "Beyan İşlemleri",
            "Rehin İşlemleri",
            "Vekalet ve Yetki İşlemleri",
            "Taşınmaz ile İlgili İşlemler",
            "İrtifak Hakları İşlemleri",
        ]

        # Klasörleri oluştur
        self.klasorleri_olustur()

        # Ana kategori butonları
        self.anaKategori_butonlarini_olustur()

        # Seçilen ana kategori
        self.secili_anaKategori = None

    def klasorleri_olustur(self):
        """Ana kategoriler için klasörleri otomatik oluşturur."""
        if not os.path.exists(TAKBIS_KLAVUZ_KLASOR):
            os.makedirs(TAKBIS_KLAVUZ_KLASOR)

        for kategori in self.ana_kategoriler:
            kategori_path = os.path.join(TAKBIS_KLAVUZ_KLASOR, kategori)
            if not os.path.exists(kategori_path):
                os.makedirs(kategori_path)

    def anaKategori_butonlarini_olustur(self):
        self.anaKategoriLayout.addWidget(QLabel("Ana Kategoriler:"))
        for kategori in self.ana_kategoriler:
            btn = QPushButton(kategori)
            btn.setMinimumHeight(44)
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet(
                "QPushButton {"
                "  background-color: #ffffff;"
                "  color: #222;"
                "  border-radius: 10px;"
                "  padding: 8px 12px;"
                "}QPushButton:hover {"
                "  background-color: #f3f3f3;"
                "}"
            )
            btn.clicked.connect(lambda _, k=kategori: self.pdf_listele(k))
            self.anaKategoriLayout.addWidget(btn)

    def pdf_listele(self, anaKategori):
        self.pdfList.clear()
        self.secili_anaKategori = anaKategori

        path = os.path.join(TAKBIS_KLAVUZ_KLASOR, anaKategori)
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.lower().endswith(".pdf"):
                    self.pdfList.addItem(f)

    def pdf_ac(self, item):
        if self.secili_anaKategori:
            dosya = os.path.join(TAKBIS_KLAVUZ_KLASOR, self.secili_anaKategori, item.text())
            if os.path.exists(dosya):
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(dosya)
                    elif os.name == 'posix':  # Mac/Linux
                        subprocess.call(('open', dosya))
                except Exception as e:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setText(f"PDF açılamadı:\n{str(e)}")
                    msg.setWindowTitle("Hata")
                    msg.exec()
