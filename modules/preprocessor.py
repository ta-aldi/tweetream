import re, string, nltk, os
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import ngrams

class Preprocessor():

    def __init__(self):
        # download & apply indonesian stopword database
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('indonesian'))

        # add additional words to be replaced
        self.replacement_word_list_path = os.path.abspath('utils/replacement_word_list.txt')
        self.replacement_word_list = [line.rstrip('\n').rstrip('\r') for line in open(self.replacement_word_list_path)]

    def run(self, tweet):
        # remove "RT"
        regex = re.compile('RT\s')
        tweet = regex.sub(' ', tweet)

        # lowercase
        tweet = tweet.lower()

        # remove http(s), hashtags, username, RT
        tweet = re.sub(r'http\S+', ' ', tweet)
        tweet = re.sub(r'#\S+', ' ', tweet)
        tweet = re.sub(r'@[a-zA-Z0-9_]+', ' ', tweet)
        tweet = re.sub(r'RT\s', ' ', tweet)
        tweet = re.sub(r'[^a-zA-Z0-9]', ' ', tweet)

        # replace abbreviations
        replacement_words = {}
        for replacement_word in self.replacement_word_list:
            replacement_words[replacement_word.split(',')[0]] = replacement_word.split(',')[1]

        # change abbreviations
        new_string = []
        for word in tweet.split():
            if replacement_words.get(word, None) is not None:
                word = replacement_words[word]
            new_string.append(word)

        # remove stopwords
        new_string = [new_str for new_str in new_string if new_str not in self.stop_words]

        # join strings
        tweet = ' '.join(new_string)

        return tweet
