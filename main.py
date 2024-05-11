import string
from collections import Counter

class MetinAnaliz:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu
        self.metin = self._dosyadan_metin_oku()

    def _dosyadan_metin_oku(self):
        try:
            with open(self.dosya_yolu, 'r', encoding='utf-8') as dosya:
                return dosya.read()
        except FileNotFoundError:
            print("Hata: Belirtilen dosya bulunamadı.")
            return ''

    def noktalama_isaretlerini_kaldir(self):
        self.metin = self.metin.translate(str.maketrans('', '', string.punctuation))

    def kelimelere_ayir(self):
        kelimeler = self.metin.lower().split()
        return kelimeler

    def istatistikleri_al(self):
        self.noktalama_isaretlerini_kaldir()
        kelimeler = self.kelimelere_ayir()

        # Harf sayısı
        harf_sayisi = sum(c.isalpha() for c in self.metin)

        # Kelime sayısı
        kelime_sayisi = len(kelimeler)

        # Etkisiz kelime (dur-stop words) sayısı
        etkisiz_kelimeler = {'ve', 'veya', 'ile', 'gibi', 'da', 'için', 'ise', 'ki', 'kadar'}
        etkisiz_kelime_sayisi = sum(1 for kelime in kelimeler if kelime in etkisiz_kelimeler)

        # Kelime frekanslarını bulma (etkisiz kelimeleri çıkartarak)
        kelime_siklikleri = Counter(word for word in kelimeler if word not in etkisiz_kelimeler)

        return harf_sayisi, kelime_sayisi, etkisiz_kelime_sayisi, kelime_siklikleri

# Kullanım örneği
dosya_yolu = 'metin_belgesi.txt'
metin_analizci = MetinAnaliz(dosya_yolu)
harf_sayisi, kelime_sayisi, etkisiz_kelime_sayisi, kelime_siklikleri = metin_analizci.istatistikleri_al()

print(f"Harf Sayısı: {harf_sayisi}")
print(f"Kelime Sayısı: {kelime_sayisi}")
print(f"Etkisiz Kelime Sayısı: {etkisiz_kelime_sayisi}")
print("En Çok Geçen Kelimeler ve Frekansları:")
for kelime, frekans in kelime_siklikleri.most_common(5):
    print(f"- {kelime}: {frekans}")
print("En Az Geçen Kelimeler ve Frekansları:")
for kelime, frekans in kelime_siklikleri.most_common()[:-6:-1]:
    print(f"- {kelime}: {frekans}")
