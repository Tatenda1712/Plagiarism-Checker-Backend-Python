import nltk
from joblib.numpy_pickle_utils import xrange
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def TokenizeText():
    f = open("text.txt", "rt")
    stop_words=set(stopwords.words('english'))
    words = str(f.readlines())
   # print(word_tokenize(words))
    tokenized=word_tokenize(words)
    filtered=[]
    wordfrequency=[]
    #print(tokenized)
    for w in tokenized:
        if w not in stop_words:
            filtered.append(w)
    #print(filtered)
    for w in filtered:
        wordfrequency.append(filtered.count(w))
    #print(str(wordfrequency)+ "\n")
   # print("Paris"+ str(list(zip(tokenized,wordfrequency))))

    #return a dictitionary of word frequency pairs
    def wordsToFreqDist(tokenized):
        wordfreq=[tokenized.count(p) for p in tokenized]
        return dict(list(zip(tokenized,wordfreq)))

    # sort a dictitionary of word-frequency pairs in order of descending frequency
    def sortFreqDict(freqdict):
        aux=[(freqdict[key],key) for key in freqdict]
        aux.sort()
        aux.reverse()
        return aux
    def removeStopwords(tokenised,stop_words):
        return [w for w in tokenized if w not in stop_words]

    # Python program for KMP Algorithm
    def KMPSearch(pat, txt):
        M = len(pat)
        N = len(txt)
        # create lps[] that will hold the longest prefix suffix
        # values for pattern
        lps = [0] * M
        j = 0  # index for pat[]
        # Preprocess the pattern (calculate lps[] array)
        computeLPSArray(pat, M, lps)
        i = 0  # index for txt[]
        while i < N:
            if pat[j] == txt[i]:
                i += 1
                j += 1
            if j == M:
                print("Found pattern at index " + str(i - j))
                j = lps[j - 1]
            # mismatch after j matches
            elif i < N and pat[j] != txt[i]:
                # Do not match lps[0..lps[j-1]] characters,
                # they will match anyway
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

    def computeLPSArray(pat, M, lps):
        len = 0  # length of the previous longest prefix suffix
        lps[0]  # lps[0] is always 0
        i = 1
        # the loop calculates lps[i] for i = 1 to M-1
        while i < M:
            if pat[i] == pat[len]:
                len += 1
                lps[i] = len
                i += 1
            else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
                if len != 0:
                    len = lps[len - 1]
                    # Also, note that we do not increment i here
                else:
                    lps[i] = 0
                    i += 1

    # d is the number of characters in the input alphabet
    d = 256

    # pat -> pattern
    # txt -> text
    # q -> A prime number
    def search(pat, txt, q):
        M = len(pat)
        N = len(txt)
        i = 0
        j = 0
        p = 0  # hash value for pattern
        t = 0  # hash value for txt
        h = 1
        # The value of h would be "pow(d, M-1)% q"
        for i in xrange(M - 1):
            h = (h * d) % q
            # Calculate the hash value of pattern and first window
            # of text
        for i in xrange(M):
            p = (d * p + ord(pat[i])) % q
            t = (d * t + ord(txt[i])) % q
            # Slide the pattern over text one by one
            # for i in xrange(N - M + 1):
            # Check the hash values of current window of text and
            # pattern if the hash values match then only check
            # for characters on by one
            if p == t:
                # Check for characters one by one
               for j in xrange(M):
                    if txt[i + j] != pat[j]:
                        break
              j += 1
              # if p == t and pat[0...M-1] = txt[i, i + 1, ...i
              if j == M:
                print("Pattern found at index " + str(i))
                # Calculate hash value for next window of text: Remove
                # leading digit, add trailing digit
            if i < N - M:
               t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q
               # We might get negative values of t, converting it
               # positive
               if t < 0:
                   t = t + q
    # Driver program to test the above function
    txt = "GEEKS FOR GEEKS"
    pat = "GEEK"
    q = 101  # A prime number
    search(pat, txt, q)

    wordsto= wordsToFreqDist(tokenized)
    sorted=sortFreqDict(wordsto)
    removed=removeStopwords(sorted,stop_words)
    pat = "ABABCABAB"
    KMPSearch(pat, removed)

TokenizeText()