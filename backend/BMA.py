from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def stemSentence(sentence):
    porter=PorterStemmer()
    porter.stem(sentence)
    token_words=word_tokenize(sentence)
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
        return "".join(stem_sentence)

document1=open('D:/PlagiarismChecker/musodza.txt','r').readlines()
document2=open('D:/PlagiarismChecker/tatenda.txt','r').readlines()

listee=(document1)
final1=[]

for i in listee:
    t=i.split('_')
    for i in t:
        final1.append(i)

for i in range(0,final1.count(' \n')):
    final1.remove(' \n')
for i in range(0, final1.count('\n')):
    final1.remove('\n')
print("final 1")
print(final1)
listee=(document2)
final2=[]
for i in listee:
    t=i.split('_')
    for i in t:
        final2.append(i)

for i in range(0,final2.count(' \n')):
    final2.remove(' \n')
for i in range(0, final2.count('\n')):
    final2.remove('\n')
print("final 2")
print(final2)
def removeCommonWordsStemming(main,generic):
    finaler=[]
    for i in main:
        query=i
        stopwordss=generic
        querywords=query.split()
        resultwords=[word for word in querywords if word.lower() not in stopwordss]
        result=' '.join(resultwords)
        finaler.append(stemSentence(result))
        print(finaler)
        return finaler
stop_words=set(stopwords.words('english'))
document1=removeCommonWordsStemming(final1,stop_words)
document2=removeCommonWordsStemming(final2,stop_words)

def BoyerMoore(pattern,text):
    m=len(pattern)
    n=len(text)
    if m>n: return -1
    skip=[]
    for k in range(256):skip.append(m)
    for k in range(m-1): skip[ord(pattern[k])]=m-k-1
    skip=tuple(skip)
    k=m-1
    while k<n:
        j=m-1;i=k
        while j>=0 and text[i]==pattern[j]:
            j-=1;i-=1
            if j==1: return  i+1
            k+=skip[ord(text[k])]
    return -1
count=0
document2_joined=".".join(document2)
print(document2_joined)

for i in document1:
    checkvar=0
    checkvar=(BoyerMoore(i,document2_joined))
    if checkvar>-1:
        count=count+1

print("the matches are "+ str(count))
rate_plagiarism=(2*count)/(len(document1)+len(document2))
print("\n The rate  of plagiarism is "+ str(rate_plagiarism))