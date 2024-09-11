from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import nltk

# Ensure required resources are available
# nltk.download('stopwords')
# nltk.download('punkt_tab')

class TextSummarizer:
    def __init__(self, text):
        self.text = text
        self.sentences = self.split_into_sentences()
        self.word_freq = self.calculate_word_frequency()
        self.sentence_scores = self.calculate_sentence_scores()

    def split_into_sentences(self):
        """
        Split the text into sentences.
        """
        sentences = sent_tokenize(self.text)
        return [s.strip() for s in sentences if s.strip()]

    def calculate_word_frequency(self):
        """
        Calculate word frequencies, excluding stop words and applying stemming.
        """
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        words = word_tokenize(self.text.lower())
        words = [stemmer.stem(word) for word in words if word.isalnum() and word not in stop_words]
        word_freq = Counter(words)
        return word_freq

    def calculate_sentence_scores(self):
        """
        Calculate sentence scores based on word frequencies.
        """
        sentence_scores = {}
        for sentence in self.sentences:
            words = word_tokenize(sentence.lower())
            words = [word for word in words if word.isalnum()]
            stemmed_words = [PorterStemmer().stem(word) for word in words]
            score = sum(self.word_freq.get(word, 0) for word in stemmed_words)
            sentence_scores[sentence] = score
        return sentence_scores

    def generate_summary(self, num_sentences):
        """
        Generate a summary by selecting the top scoring sentences.
        """
        sorted_sentences = sorted(self.sentence_scores, key=self.sentence_scores.get, reverse=True)
        num_sentences = min(num_sentences, len(sorted_sentences))  # Ensure not to exceed available sentences
        summary = sorted_sentences[:num_sentences]
        return ' '.join(summary)

# Example usage
text = """
Subject: Leave Application

Dear Ms. Johnson,

I hope this message finds you well. I am writing to request a leave of absence from August 28, 2024, to August 30, 2024, due to a personal matter that requires my attention.

I have arranged for my colleague, Tom Brown, to manage any urgent tasks and ensure that my ongoing projects are on track. I will be available via email or phone for any critical issues.

Please let me know if there is any further information you require or if there are specific tasks I should address before my leave.

Thank you for your understanding and support.

Best regards,

Emily Clarke
Project Manager
Marketing Department
"""

summarizer = TextSummarizer(text)
summary = summarizer.generate_summary(2)
print(summary)
