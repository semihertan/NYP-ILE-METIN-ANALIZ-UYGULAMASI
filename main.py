import string #string kütüphanesi metin analizi için çeşitli araçlar sağlar. Biz kodumuzda noktalama işaretlerini kaldırmak için kullandık
from collections import Counter #Python'ın collections kütüphanesinde bulunan Counter sınıfı verileri sayma işlemlerini kolaylaştırır


class Metin:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu # Dosya yolunu saklar
        self.icerik = self.dosya_okuma() # Dosya içeriğini okur
        self.kelimeler = self.metin_isleme() # Metni işler ve kelimelere ayırır

    def dosya_okuma(self): # Dosya okur
        with open(self.dosya_yolu, 'r', encoding='utf-8') as file:
            return file.read()

    def metin_isleme(self):
        temiz_icerik = self.icerik.translate(str.maketrans('', '', string.punctuation)) # Noktalama işaretlerini kaldırır
        kelimeler = temiz_icerik.lower().split() # Metni küçük harfe dönüştürür ve kelimelere ayırır
        return kelimeler

    def harf_sayisi(self):# Toplam harf sayısını hesaplar
        return sum(len(kelime) for kelime in self.kelimeler)

    def kelime_sayisi(self): #Toplam kelime sayısını hesaplar
        return len(self.kelimeler)

    def etkisiz_kelimeler(self, etkisiz_kelimeler_listesi): # Etkisiz kelimeleri listeden çıkarır ve kalan kelimeleri döndürür
        return [kelime for kelime in self.kelimeler if kelime not in etkisiz_kelimeler_listesi]

    def kelime_istatistikleri(self):
        kelime_sayaci = Counter(self.kelimeler) #self kelimeler listesindeki her bir kelimenin kaç kez geçtiğini sayar
        en_cok_gecen = kelime_sayaci.most_common(5) # En yaygın kullanılan 5 kelimeyi bulur
        en_az_gecen = kelime_sayaci.most_common()[:-6:-1] # En az kullanılan 5 kelimeyi bulur
        return en_cok_gecen, en_az_gecen
