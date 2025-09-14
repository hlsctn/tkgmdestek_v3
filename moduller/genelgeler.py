# moduller/genelgeler.py
import os
import subprocess
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

GENELGELER_KLASOR = "moduller/genelgeler"

class GenelgelerPenceresi(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genelgeler")
        self.setGeometry(500, 220, 800, 400)

        mainLayout = QHBoxLayout()

        # Sol panel: Ana kategori
        self.anaKategoriLayout = QVBoxLayout()
        mainLayout.addLayout(self.anaKategoriLayout)

        # Orta panel: Alt yıllar
        self.altYilLayout = QVBoxLayout()
        mainLayout.addLayout(self.altYilLayout)

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
            "2025",
            "2020-2024",
            "2015-2019",
            "2010-2014",
            "2005-2009",
            "2000-2004",
            "1995-1999",
        ]
        self.anaKategori_butonlarini_olustur()

        # Seçilen ana kategori ve alt yılı saklamak için
        self.secili_anaKategori = None
        self.secili_altYil = None

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
            btn.clicked.connect(lambda _, k=kategori: self.altYillar_goster(k))
            self.anaKategoriLayout.addWidget(btn)

    def altYillar_goster(self, anaKategori):
        # Önceki alt yıl butonlarını temizle
        for i in reversed(range(self.altYilLayout.count())):
            widget = self.altYilLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.altYilLayout.addWidget(QLabel(f"{anaKategori} Alt Yıllar:"))

        if "-" in anaKategori:
            bas, son = map(int, anaKategori.split("-"))
            alt_yillar = [str(y) for y in range(bas, son + 1)]
        else:
            alt_yillar = [anaKategori]

        for yil in alt_yillar:
            btn = QPushButton(yil)
            btn.setMinimumHeight(36)
            btn.setFont(QFont("Arial", 11))
            btn.setStyleSheet(
                "QPushButton {"
                "  background-color: #e0e0e0;"
                "  border-radius: 8px;"
                "}QPushButton:hover {"
                "  background-color: #d0d0d0;"
                "}"
            )
            btn.clicked.connect(lambda _, y=yil, a=anaKategori: self.pdf_listele(a, y))
            self.altYilLayout.addWidget(btn)

    def pdf_listele(self, anaKategori, yil):
        self.pdfList.clear()
        self.secili_anaKategori = anaKategori
        self.secili_altYil = yil

        path = os.path.join(GENELGELER_KLASOR, anaKategori, yil)
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.lower().endswith(".pdf"):
                    self.pdfList.addItem(f)

    def pdf_ac(self, item):
        if self.secili_anaKategori and self.secili_altYil:
            dosya = os.path.join(GENELGELER_KLASOR, self.secili_anaKategori, self.secili_altYil, item.text())
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
