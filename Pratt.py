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
def removeCommonWordsStemming(main,generic):
    finaler=[]
    for i in main:
        query=i
        stopwordss=generic
        querywords=query.split()
        resultwords=[word for word in querywords if word.lower() not in stopwordss]
        result=' '.join(resultwords)
        finaler.append(stemSentence(result))
    return finaler
stop_words=set(stopwords.words('english'))
document1=removeCommonWordsStemming(final1,stop_words)
document2=removeCommonWordsStemming(final2,stop_words)

d=256
def search(pat,txt,q):
    M=len(pat)
    N=len(txt)
    i=0
    j=0
    p=0
    t=0
    h=1
    count=0

    for i in range(M-1):
        h=(h*d)%q

    if (N>M):
        for i in range (M-1):
            p=(d*p+ord(pat[i]))%q
            t=(d*t + ord(txt[i]))%q
    else:
        exit

    for i in range(N-M + 1):
        if p==t:
            for j in range(M):
                if txt[i+j]!=pat[j]:
                    break
            j+=1

            if j==N:
                count =count+1
                print("patterb found at"+ str(i))

        if i< N-M:
            t=(d*(t-ord(txt[i])*h)+ ord(txt[i+M]))%q

            if t<0:
                t=t+q
    return count

q=101
match_no=0

for i in document2:
    for j in document1:
        print(str('\n doc 1 string ->')+j + ' doc 1 string->' +i+ str('<------pattern\n'))
        test=search(j,i,q)
        if test>0:
            match_no=match_no+1

rate_plagiarism = (2 * match_no) / (len(document1) + len(document2))
print("the matches are " + str(match_no))
print("\n The rate  of plagiarism is " + str(rate_plagiarism))


