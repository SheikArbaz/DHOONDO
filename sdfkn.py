from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words("english"))  # load stopwords

example_sent = "This is a sample sentence, showing off the stop words filtration."

example_words = word_tokenize(example_sent)

print(example_words)

example_words = filter(lambda x: x not in string.punctuation, example_words)

print(example_words)

# removing stopwords 
cleaned_text = filter(lambda x: x not in stop_words, example_words)

print(cleaned_text)
