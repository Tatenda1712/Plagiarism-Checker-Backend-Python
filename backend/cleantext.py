import nltk
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics

text="College social network project is designed only for students of the college. This project is similar to many popular social networking platforms where the students will be provided with the opportunity to share information. It will also help them to tackle the problems they are facing in the college by highlighting the issue on this platform. One should have to make an account on this platform to get access to all of its features. Students will also be able to get updates related to the college. The creation of an account of anyone other than the college students is restricted.Students can connect by sending friend requests. After this, they can share the information which consists of educational materials and many more. Students are also able to upload their profile pictures on which they can receive likes and comments from the students to whom they connected with. There are also features of forming groups, sharing videos, etc. Students are also able to send messages to each other which is the major feature of any social networking platform."
tokenised=sent_tokenize(text)
print(tokenised)
word=word_tokenize(text)
print(word)
fdist=FreqDist(word)
print(fdist)
print(fdist.most_common(5))
stop_words=set(stopwords.words("english"))
print(stop_words)
cleaned=[]
for w in word:
    if w not in stop_words:
        cleaned.append(w)

print(cleaned)

ps=PorterStemmer()
stemmed_words=[]
for w in cleaned:
    stemmed_words.append(ps.stem(w))
print(stemmed_words)

print(nltk.pos_tag(stemmed_words))
