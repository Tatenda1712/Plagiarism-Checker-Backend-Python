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
import glob

import numpy as np
import os

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])
myAssignments= glob.glob('C:/xampp/htdocs/Laravel/Laravel/storage/app/Assignments/*.txt')
print('\n assignments avilable are\n')
for assignment in myAssignments:
    print(assignment)

#with open('C:/xampp/htdocs/Laravel/Laravel/storage/app/Assignments/musodza.txt','r') as file:
 #   data = file.read().replace('\n', '')
  #  str2=data.replace(' ', '')
#with open('C:/xampp/htdocs/Laravel/Laravel/storage/app/Assignments/tatenda.txt','r') as file:
 #   data = file.read().replace('\n', '')
 #   str2=data.replace(' ', '')

print("\n plagalised files are:")
for i in range(0,len(myAssignments)):
    with open(myAssignments[i],'r') as file:
        data = file.read().replace('\n', '')
        str1 = data.replace(' ', '')
        str1file=myAssignments[i]
    for i in range(0,len(myAssignments)):
        with open(myAssignments[i],'r') as file:
            data = file.read().replace('\n', '')
            str2 = data.replace(' ', '')
            str2file = myAssignments[i]
            if(len(str1)>len(str2)):
                length=len(str1)
                plagiarised = 100 - round((levenshtein(str1, str2) / length) * 100, 2)
                print(str1file, "and",str2file, plagiarised, "% plagarised")
            else:
                length = len(str2)
                if str1file!=str2file:
                    plagiarised = 100 - round((levenshtein(str1, str2) / length) * 100, 2)
                    print(str1file, "and", str2file, plagiarised, "% plagarised")


#plagiarised= 100-round((levenshtein(str1,str2)/length)*100,2)
#print(myAssignments[i],plagiarised,"% plagarised")
#print(100-round((levenshtein(str1,str2)/length)*100,2),'% Similarity')