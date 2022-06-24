import glob
import re
from flask import jsonify
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from db import mysql
from flaskext.mysql import MySQL
from flask import Flask, request,session,jsonify
from flask_cors import CORS, cross_origin
from datetime import timedelta
import pymysql
import os
from werkzeug.utils import secure_filename
import studentSimilarity
import tatenda

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

def removeStopWords(main,generic):
    finaler=[]
    for i in main:
        query=i
        stopwordss=generic
        querywords=query.split()
        resultwords=[word for word in querywords if word.lower() not in stopwordss]
        result=' '.join(resultwords)
        finaler.append(stemSentence(result))
    return finaler

def checkPlagiarism(course):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT coursecode coursecode, regnumber regnumber, url url FROM assignments WHERE coursecode=%s", course)
        row = cursor.fetchall()
        myAssignments=[]
        regnumber=[]
        print("results")
        for rw in row:
            regnumber.append(rw['regnumber'])
            myAssignments.append("C:/xampp/htdocs/Laravel/Laravel/storage/app/"+rw['url'] )
        results = []
        for i in range(0, len(myAssignments) ):
            with open(myAssignments[i], 'r') as file:
                assignment = file.readlines()
                stop_words = set(stopwords.words('english'))
                document1 = removeStopWords(assignment, stop_words)
                assignmentwords = []
                for word in document1:
                    assignmentwords.append(word)
                str1 = " ".join(assignmentwords)
                for j in range(0, len(regnumber)):
                    str1file =regnumber[j]
                print(str1file)
            for i in range(0, len(myAssignments)):
                with open(myAssignments[i], 'r') as file:
                    # data = file.read().replace('\n', '')
                    assignment = file.readlines()
                    stop_words = set(stopwords.words('english'))
                    document2 = removeStopWords(assignment, stop_words)
                    assignmentwords2 = []
                    for word in document2:
                        assignmentwords2.append(word)
                    # data = re.sub(r"[A-Za-z]+\d+|\d+[A-Za-z]+", '', data).strip()
                    # str2 = data.replace(' ', '')
                    str2 = " ".join(assignmentwords2)
                    for j in range(0, len(regnumber)):
                        str2file = regnumber[j]
                    print(str1file)
                    # if(len(str1)>len(str2)):
                    length = len(str1)
                    #plagiarised = 100 - round((levenshtein(str1, str2) / length) * 100, 2)
                    # print(str1file, "and", str2file, plagiarised, "% plagarised")
                    if str1file != str2file:
                        plagiarised = 100 - round((levenshtein(str1, str2) / length) * 100, 2)

                        print(str1file, "and", str2file, plagiarised, "% plagarised")
        conn.commit()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


checkPlagiarism("Cs207")