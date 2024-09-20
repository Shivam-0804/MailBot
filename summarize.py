"""frequency-based extraction summarization"""
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
import nltk

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
        print(word_freq)
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
        num_sentences = min(num_sentences, len(sorted_sentences)) 
        summary = sorted_sentences[:num_sentences]
        return ' '.join(summary)

text = """
Dear Students,

Smart India Hackathon (SIH) is one of the national level reputed Hackathons for the last many years. Details about SIH 2024 are available at https://www.sih.gov.in/.

Internal Hackathon is the primary step for participation in SIH. Internal Hackathon is conducted at Institute Level where selected teams at Institute Level move to the next step of SIH. The guidelines about formation of teams are as follows:

1. Each team needs to have exactly 6 students / members. 
2. Each team must have at least 1 female member.
3. Each team must have One Team Leader
4. All the students in a team must be from JIIT-62 or 128.

The Internal Hackathon for SIH 2024 at JIIT Noida will be conducted soon. Detailed instructions in this regard will be communicated soon. The Internal Hackathon will act as the qualifier round for entry in SIH - 2024. 

As the first step for the Internal Hackathon, all teams need to register. All students are encouraged to make the teams (as per following guidelines) and complete the registration process by 14th September 2024 by filling the Google Form:

Link of Google Form: https://forms.gle/a7NWRiCfxMzxrACg7

After registration, all important communication will be through email with the provided mail ID of the Team Leader. All are encouraged to register for the JIIT Noida's Internal Hackathon for SIH 2024

With Good Wishes

Prof. Manish Kumar Thakur (WhatsApp Number: 9667189911)
Professor and Associate Head, Dept. of CSE & IT / JIIT SPOC for SIH 2024 

Mr. Prantik Biswas (WhatsApp Number: 9836438182)
Assistant Professor, Dept. of CSE & IT
"""

summarizer = TextSummarizer(text)
summary = summarizer.generate_summary(2)
print(summary)
