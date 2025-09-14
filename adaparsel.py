import os
import re
from pdf2image import convert_from_path
import pytesseract

# PDF'lerin bulunduğu klasör
pdf_folder = r"C:\Users\kullanici\PDFler"

# OCR ve PDF işleme
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"İşleniyor: {filename}")

        try:
            # PDF'yi görsellere çevir
            pages = convert_from_path(pdf_path)

            # Tüm sayfaların metnini birleştir
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page, lang='tur') + "\n"

            # Regex ile Ada ve Parsel yakala
            ada_match = re.search(r"Ada[\s\w]*?(\d{1,4})", text, re.IGNORECASE)
            parsel_match = re.search(r"Parsel[\s\w\W]{0,15}?(\d{1,4})", text, re.IGNORECASE)

            ada_no = ada_match.group(1) if ada_match else "?"
            parsel_no = parsel_match.group(1) if parsel_match else "?"

            if ada_no != "?" and parsel_no != "?":
                new_name = f"{ada_no}-{parsel_no}.pdf"
                new_path = os.path.join(pdf_folder, new_name)
                os.rename(pdf_path, new_path)
                print(f"Yeniden adlandırıldı: {new_name}")
            else:
                print("Ada veya Parsel bulunamadı, isim değişmedi.")

        except Exception as e:
            print(f"Hata oluştu: {e}")

print("Tüm PDF'ler işlendi.")
