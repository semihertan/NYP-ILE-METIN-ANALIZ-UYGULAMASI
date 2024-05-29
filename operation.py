import re
from difflib import SequenceMatcher

# Metni Tokenlarına Ayırma 
class Token():

    def __init__(self, data):
        self.text = data

    def removePunct(self):
        text = self.text

        turkish_punctuation = [
            '.', ',', ';', ':', '!', '?', '(', ')',
            '[', ']', '{', '}', '-', '—', '…', '‘',
            '’', '“', '”', '«', '»', '/', '\\', '|',
            '§', '$', '%', '@', '&', '*', '•', '_',
            '~', '`', '"', "'"
        ]

        for isaret in turkish_punctuation:
            text = text.replace(isaret, "")  

        return text.lower()

    def sentenceSplit(self):
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', self.text)
        return sentences

    def wordSplit(self):
        words = self.removePunct().split()
        return words

# Tokenların İçeriğini Sayma
class Counter():

    def __init__(self, words):
        self.words = words

    def letterCount(self):
        words = self.words
        concat = "".join(words)
        
        return len(concat)
    
    def wordCount(self):
        words = self.words
        return len(words)

# Token İçeriğini Analiz Etme
class Analyzer():
    def __init__(self, words):
        self.words = words

    def frequencyMatch(self):
        words = self.words

        frequency = {}
        for word in words:
            if word in frequency:
                continue          

            count = words.count(word)
            frequency[word] = count                 

        return frequency

    def wordRarity(self):
        frequency = self.frequencyMatch()
        maxFrequency = max(frequency.values())
        minFrequency = min(frequency.values())
        maxWords = [word for word in frequency if frequency[word] == maxFrequency]
        minWords = [word for word in frequency if frequency[word] == minFrequency]
        
        if len(maxWords) > 5:
            maxWords = [maxWords[i] for i in range(5)]
        if len(minWords) > 5:
            minWords = [minWords[i] for i in range(5)]

        if maxWords == minWords:
            return maxWords, ["---"]
        
        return maxWords, minWords
        
    def uselessWord(self):
        words = self.words

        etkisiz_kelimeler = [
            "acaba", "ama", "ancak", "aslında", "az", "bana", "bazı", "belki", "bile", 
            "bir", "biraz", "birçok", "biri", "birisi", "birkaç", "birşey", "biz", 
            "bu", "bunu", "bunun", "da", "daha", "de", "defa", "diğer", "diye", 
            "dışında", "eğer", "en", "gibi", "hem", "hep", "hepsi", "her", "herhangi", 
            "herkes", "hiç", "hiçbir", "için", "ise", "işte", "kaç", "kadar", 
            "karşın", "kendi", "kez", "ki", "kim", "kimse", "kise", "mı", "mi", 
            "mu", "mü", "nasıl", "ne", "neden", "nedenle", "nerde", "nerede", 
            "nereye", "niçin", "niye", "o", "sadece", "sanki", "şey", "siz", "şu", 
            "şuna", "şunlar", "şunu", "tarafından", "ve", "veya", "ya", "yani", 
            "yine", "yoksa", "zaten"
        ]

        count = 0
        for useless in etkisiz_kelimeler:
            if useless in words:
                times = words.count(useless)
                count += times

        return count

# Dosya Kontrolü
class FileHandler():
    def __init__(self, path):
        self.path = path
        self.data = self.dataCollect()
        

    def dataCollect(self):
        path = self.path
        try:
            with open(path, mode="r", encoding="utf-8") as readFile:
                data = readFile.read()
                return data
            
        except FileNotFoundError:
            with open(path, mode="a", encoding="utf-8") as createFile:
                data = "Merhaba! Bugün nasılsın? Ben iyiyim. Yarın ne yapacaksın?\n"
                createFile.write(data)
                return data

    def upload(self):
        pass

# Metin Özelliklerini Sınıflandırma
class TextData:
    def __init__(self,data):
        self.text = data
        self.token = Token(self.text) 
        self.count = Counter(self.token.wordSplit())
        self.analyst = Analyzer(self.token.wordSplit())

        self.wordCount = self.count.wordCount()
        self.letterCount = self.count.letterCount()

        self.uselessWordCount = self.analyst.uselessWord()
        self.maxWord, self.minWord = self.analyst.wordRarity()

    def get_text(self):
        return self.text

    def get_wordCount(self):
        return self.wordCount

    def get_letterCount(self):
        return self.letterCount

    def get_uselessWordCount(self):
        return self.uselessWordCount

    def get_maxWord(self):
        return ", ".join(self.maxWord)

    def get_minWord(self):
        return ", ".join(self.minWord)

# Benzerlik Ölçümü
class Similarity:
    def __init__(self):
        pass

    def percentage(self, text1, text2):
        similar = SequenceMatcher(None, text1, text2).ratio()
        yuzdelik = round(similar * 100, 2)
        return yuzdelik

    def test(self):
        text1 = TextData(FileHandler("text1.txt").data).text
        text2 = TextData(FileHandler("text2.txt").data).text
        print(text1)
        print()
        print(text2)
        print(Similarity().percentage(text1,text2))


# Similarity().test()

