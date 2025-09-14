import os
import shutil
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog,
    QComboBox, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt

# ---------------------------
# Dosya ve Klasör Yolları
# ---------------------------
DUYURULAR_DOSYA = "moduller/duyurular.txt"
GENELGELER_KLASOR = "moduller/genelgeler"

# ---------------------------
# Admin Giriş Penceresi
# ---------------------------
class AdminGirisPenceresi(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Admin Girişi")
        self.resize(300, 150)

        layout = QVBoxLayout()

        self.kullaniciInput = QLineEdit()
        self.kullaniciInput.setPlaceholderText("Kullanıcı Adı")
        layout.addWidget(self.kullaniciInput)

        self.sifreInput = QLineEdit()
        self.sifreInput.setPlaceholderText("Şifre")
        self.sifreInput.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.sifreInput)

        self.girisBtn = QPushButton("Giriş Yap")
        self.girisBtn.clicked.connect(self.giris_yap)  # clicked sinyali
        layout.addWidget(self.girisBtn)

        self.setLayout(layout)

    def giris_yap(self, checked=False):  # QPushButton sinyali için parametre eklendi
        kullanici = self.kullaniciInput.text().strip()
        sifre = self.sifreInput.text().strip()
        if kullanici == "admin" and sifre == "1234567+pl":
            if self.parent:
                self.parent.admin_giris_yapildi(kullanici)
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

# ---------------------------
# Admin Panel Penceresi
# ---------------------------
class AdminPanelPenceresi(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Admin Paneli")
        self.setGeometry(500, 250, 400, 400)
        layout = QVBoxLayout()

        self.kullaniciYonetimBtn = QPushButton("Üye Yönetimi")
        self.kullaniciYonetimBtn.clicked.connect(self.uyeleri_yonet)
        layout.addWidget(self.kullaniciYonetimBtn)

        self.duyuruGonderBtn = QPushButton("Duyuru Gönder")
        self.duyuruGonderBtn.clicked.connect(self.duyuru_gonder)
        layout.addWidget(self.duyuruGonderBtn)

        self.genelgeEkleBtn = QPushButton("Genelge Ekle / Düzenle")
        self.genelgeEkleBtn.clicked.connect(self.genelge_ekle)
        layout.addWidget(self.genelgeEkleBtn)

        self.sifreDegistirBtn = QPushButton("Şifre Değiştir")
        self.sifreDegistirBtn.clicked.connect(self.sifre_degistir)
        layout.addWidget(self.sifreDegistirBtn)

        self.cikisBtn = QPushButton("Çıkış Yap")
        self.cikisBtn.clicked.connect(self.cikis_yap)
        layout.addWidget(self.cikisBtn)

        self.setLayout(layout)

    def uyeleri_yonet(self):
        QMessageBox.information(self, "Üye Yönetimi", "Üye yönetimi paneli açıldı.")

    def duyuru_gonder(self):
        pencere = DuyuruEklePenceresi()
        pencere.exec()

    def genelge_ekle(self):
        pencere = GenelgeEklePenceresi()
        pencere.exec()

    def sifre_degistir(self):
        pencere = SifreDegistirPenceresi({"admin": "1234567+pl"}, "admin")
        pencere.exec()

    def cikis_yap(self):
        if self.parent:
            self.parent.kullanici_cikisi()
        self.close()

# ---------------------------
# Genelge Ekle / Düzenle Penceresi
# ---------------------------
class GenelgeEklePenceresi(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genelge Ekle / Düzenle")
        self.resize(500, 300)
        self.pdfDosya = None

        layout = QVBoxLayout()

        self.baslikInput = QLineEdit()
        self.baslikInput.setPlaceholderText("Genelge başlığını girin")
        layout.addWidget(QLabel("Genelge Başlığı:"))
        layout.addWidget(self.baslikInput)

        self.dosyaSecBtn = QPushButton("PDF Dosyası Seç")
        self.dosyaSecBtn.clicked.connect(self.pdf_sec)
        layout.addWidget(self.dosyaSecBtn)

        self.surukleLabel = QLabel("PDF dosyasını buraya sürükleyip bırakabilirsiniz")
        self.surukleLabel.setStyleSheet("border: 2px dashed gray; padding: 20px;")
        self.surukleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.surukleLabel.setAcceptDrops(True)
        layout.addWidget(self.surukleLabel)

        self.anaKategoriBox = QComboBox()
        self.anaKategoriBox.addItems(["2025", "2020-2024", "2015-2019", "2010-2014",
                                      "2005-2009", "2000-2004", "1995-1999"])
        self.anaKategoriBox.currentTextChanged.connect(self.alt_yil_guncelle)
        layout.addWidget(QLabel("Ana Kategori Seç:"))
        layout.addWidget(self.anaKategoriBox)

        self.altYilBox = QComboBox()
        layout.addWidget(QLabel("Alt Yıl Seç:"))
        layout.addWidget(self.altYilBox)
        self.alt_yil_guncelle(self.anaKategoriBox.currentText())

        self.kaydetBtn = QPushButton("Kaydet")
        self.kaydetBtn.clicked.connect(self.genelge_kaydet)
        layout.addWidget(self.kaydetBtn)

        self.setLayout(layout)

    def pdf_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "PDF Seç", "", "PDF Files (*.pdf)")
        if dosya:
            self.pdfDosya = dosya
            self.surukleLabel.setText(os.path.basename(dosya))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.pdfDosya = urls[0].toLocalFile()
            self.surukleLabel.setText(os.path.basename(self.pdfDosya))

    def alt_yil_guncelle(self, anaKategori):
        self.altYilBox.clear()
        if "-" in anaKategori:
            bas, son = map(int, anaKategori.split("-"))
            alt_yillar = [str(y) for y in range(bas, son + 1)]
        else:
            alt_yillar = [anaKategori]
        self.altYilBox.addItems(alt_yillar)

    def genelge_kaydet(self):
        baslik = self.baslikInput.text().strip()
        if not baslik:
            QMessageBox.warning(self, "Hata", "Başlık boş olamaz!")
            return
        if not self.pdfDosya:
            QMessageBox.warning(self, "Hata", "PDF dosyası seçilmedi!")
            return

        anaKategori = self.anaKategoriBox.currentText()
        altYil = self.altYilBox.currentText()
        hedefKlasor = os.path.join(GENELGELER_KLASOR, anaKategori, altYil)
        os.makedirs(hedefKlasor, exist_ok=True)

        hedefDosya = os.path.join(hedefKlasor, f"{baslik}.pdf")
        try:
            shutil.copy(self.pdfDosya, hedefDosya)
            QMessageBox.information(self, "Başarılı", f"{baslik}.pdf başarıyla kaydedildi!")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Dosya kaydedilemedi:\n{str(e)}")

# ---------------------------
# Duyuru Ekle Penceresi
# ---------------------------
class DuyuruEklePenceresi(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Duyuru Ekle")
        self.resize(400, 300)
        layout = QVBoxLayout()

        self.baslikInput = QLineEdit()
        self.baslikInput.setPlaceholderText("Duyuru Başlığı")
        layout.addWidget(QLabel("Duyuru Başlığı:"))
        layout.addWidget(self.baslikInput)

        self.icerikInput = QTextEdit()
        self.icerikInput.setPlaceholderText("Duyuru İçeriği")
        layout.addWidget(QLabel("Duyuru İçeriği:"))
        layout.addWidget(self.icerikInput)

        self.kaydetBtn = QPushButton("Kaydet")
        self.kaydetBtn.clicked.connect(self.duyuru_kaydet)
        layout.addWidget(self.kaydetBtn)

        self.setLayout(layout)

    def duyuru_kaydet(self):
        baslik = self.baslikInput.text().strip()
        icerik = self.icerikInput.toPlainText().strip()
        if not baslik or not icerik:
            QMessageBox.warning(self, "Hata", "Başlık ve içerik boş olamaz!")
            return

        os.makedirs(os.path.dirname(DUYURULAR_DOSYA), exist_ok=True)
        with open(DUYURULAR_DOSYA, "a", encoding="utf-8") as f:
            f.write(f"{baslik}|{icerik}\n")
        QMessageBox.information(self, "Başarılı", "Duyuru kaydedildi!")
        self.close()

# ---------------------------
# Şifre Değiştir Penceresi
# ---------------------------
class SifreDegistirPenceresi(QDialog):
    def __init__(self, kullanici_sifre_dict, kullanici):
        super().__init__()
        self.kullanici_sifre_dict = kullanici_sifre_dict
        self.kullanici = kullanici

        self.setWindowTitle("Şifre Değiştir")
        self.resize(300, 150)
        layout = QVBoxLayout()

        self.yeniSifre = QLineEdit()
        self.yeniSifre.setPlaceholderText("Yeni Şifre")
        self.yeniSifre.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.yeniSifre)

        self.kaydetBtn = QPushButton("Kaydet")
        self.kaydetBtn.clicked.connect(self.sifre_degistir)
        layout.addWidget(self.kaydetBtn)

        self.setLayout(layout)

    def sifre_degistir(self):
        yeni = self.yeniSifre.text().strip()
        if not yeni:
            QMessageBox.warning(self, "Hata", "Şifre boş olamaz!")
            return
        self.kullanici_sifre_dict[self.kullanici] = yeni
        QMessageBox.information(self, "Başarılı", "Şifre değiştirildi!")
        self.close()
