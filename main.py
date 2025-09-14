import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QLabel,
    QVBoxLayout, QLineEdit, QListWidget, QHBoxLayout, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


# ---------------------------
# Veritabanı Yardımcı Fonksiyonlar
# ---------------------------
def veritabani_olustur():
    conn = sqlite3.connect("notlar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metin TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def notlari_getir():
    conn = sqlite3.connect("notlar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, metin FROM notlar")
    veriler = cursor.fetchall()
    conn.close()
    return veriler


def not_ekle(metin):
    conn = sqlite3.connect("notlar.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notlar (metin) VALUES (?)", (metin,))
    conn.commit()
    conn.close()


def not_sil(not_id):
    conn = sqlite3.connect("notlar.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notlar WHERE id = ?", (not_id,))
    conn.commit()
    conn.close()


# ---------------------------
# Notlarım Penceresi
# ---------------------------
class NotlarimPenceresi(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notlarım")
        self.setGeometry(500, 250, 400, 400)

        layout = QVBoxLayout()

        # Başlık
        baslik = QLabel("Notlarım")
        baslik.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(baslik)

        # Not giriş alanı
        self.notInput = QLineEdit()
        self.notInput.setPlaceholderText("Yeni not yazın ve Enter’a basın...")
        self.notInput.returnPressed.connect(self.not_ekle)
        layout.addWidget(self.notInput)

        # Not listesi
        self.notList = QListWidget()
        layout.addWidget(self.notList)

        # Silme butonu
        silLayout = QHBoxLayout()
        btnSil = QPushButton("Seçili Notu Sil")
        btnSil.clicked.connect(self.not_sil)
        silLayout.addWidget(btnSil)
        layout.addLayout(silLayout)

        self.setLayout(layout)

        # Veritabanındaki notları yükle
        self.notlari_yukle()

    def notlari_yukle(self):
        self.notList.clear()
        veriler = notlari_getir()
        for veri in veriler:
            not_id, metin = veri
            self.notList.addItem(f"{not_id} - {metin}")

    def not_ekle(self):
        metin = self.notInput.text().strip()
        if metin:
            not_ekle(metin)
            self.notInput.clear()
            self.notlari_yukle()

    def not_sil(self):
        secili = self.notList.currentItem()
        if secili:
            text = secili.text()
            not_id = int(text.split(" - ")[0])  # ID'yi al
            not_sil(not_id)
            self.notlari_yukle()


# ---------------------------
# Ana Menü
# ---------------------------
class AnaMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tapu ve Kadastro - Masaüstü Uygulaması")
        self.setGeometry(400, 200, 600, 400)
        self.setStyleSheet("background-color: orange;")

        # Başlık
        self.label = QLabel("Tapu ve Kadastro Genel Müdürlüğü", self)
        self.label.setFont(QFont("Arial", 16, weight=QFont.Weight.Bold))
        self.label.setStyleSheet("color: white; margin-bottom: 20px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Grid düzeni
        grid = QGridLayout()
        grid.addWidget(self.label, 0, 0, 1, 3)

        # Menü butonları
        menuler = [
            ("Notlarım", self.notlarim),
            ("Yapılacaklar", self.yapilacaklar),
            ("Görevde Yükümlülükler", self.gorevler),
            ("Yararlı Bilgiler", self.yararliBilgi),
            ("Genelgeler", self.genelgeler),
            ("TAKBİS Kılavuzları", self.takbis),
            ("Sözlük", self.sozluk),
            ("Kadastro Modülü", self.kadastro),
            ("Chat Grupları", self.chatGruplari)
        ]

        # Butonları ekleme
        row, col = 1, 0
        for isim, fonksiyon in menuler:
            btn = QPushButton(isim)
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet(
                "background-color: white; color: black; "
                "padding: 10px; border-radius: 10px;"
            )
            btn.clicked.connect(fonksiyon)
            grid.addWidget(btn, row, col)

            col += 1
            if col > 2:  # her satırda 3 buton olsun
                col = 0
                row += 1

        self.setLayout(grid)

    # Menü fonksiyonları
    def notlarim(self):
        pencere = NotlarimPenceresi()
        pencere.exec()

    def yapilacaklar(self):
        QMessageBox.information(self, "Yapılacaklar", "Yapılacaklar menüsü açıldı.")

    def gorevler(self):
        QMessageBox.information(self, "Görevde Yükümlülükler", "Görevler menüsü açıldı.")

    def yararliBilgi(self):
        QMessageBox.information(self, "Yararlı Bilgiler", "Yararlı Bilgiler menüsü açıldı.")

    def genelgeler(self):
        QMessageBox.information(self, "Genelgeler", "Genelgeler menüsü açıldı.")

    def takbis(self):
        QMessageBox.information(self, "TAKBİS Kılavuzları", "TAKBİS Kılavuzları menüsü açıldı.")

    def sozluk(self):
        QMessageBox.information(self, "Sözlük", "Sözlük menüsü açıldı.")

    def kadastro(self):
        QMessageBox.information(self, "Kadastro Modülü", "Kadastro Modülü açıldı.")

    def chatGruplari(self):
        QMessageBox.information(self, "Chat Grupları", "Chat Grupları menüsü açıldı.")


# ---------------------------
# Programı Çalıştır
# ---------------------------
if __name__ == "__main__":
    veritabani_olustur()  # program açıldığında tabloyu oluştur
    app = QApplication(sys.argv)
    pencere = AnaMenu()
    pencere.show()
    sys.exit(app.exec())
