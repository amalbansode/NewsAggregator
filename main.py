# MIT License
# 
# Copyright (c) 2019 Amal Bansode
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

# -*- coding: utf-8 -*-
#! python3

import webbrowser
from newspaper import Article, Source
import newspaper
import nltk
import os
from datetime import datetime, date, timedelta
import json

# CONFIGURABLE OPTIONS
NUM = 5 # Number of top articles to summarise per source
OPEN_BROWSER = True # Open news report HTML file in web browser upon end of aggregation
FILENAME = 'NewsReport.html'

ENABLE_JSON_OUTPUT = False # Output results to JSON file
JSON_OUT_FILE = 'output.json'

######################################
### DO NOT TOUCH BEYOND THIS POINT ###
######################################

F = open(FILENAME,'w')
NOW = datetime.now()
PATH = os.path.abspath(FILENAME).replace(FILENAME,'')

# Loading and checking for errors in sources.json
try:
    SOURCES = open(PATH + 'sources.json','r')
    sourcesDict = json.load(SOURCES)
except:
    print('>>> ERROR: sources.json is either missing or formatted incorrectly. Please check the file and try again!')
    exit()
else:
    SOURCES = open(PATH + 'sources.json','r')
    sourcesDict = json.load(SOURCES)

# Printing available categories in Terminal
while True:
    for key, value in sourcesDict.items():
        print(key, end='\t', flush=True)
    
    print('\n\n>>> Enter category name')
    REQUESTED = input()

    if REQUESTED in sourcesDict: 
        sourcesDict = sourcesDict[REQUESTED]
        break
    else: 
        print('>>> ERROR: CATEGORY NOT FOUND!')

print('\nBeginning the hunt for news...')

# Writing HTML file
TOP = """<html><head><title>Your News Summary</title></head><body style="max-width: 720px; margin: 2em auto; font-family: sans-serif; line-height: 1.4;"><h1>Here’s your news summary for %s</h1><p><i>Last Updated: %s</i></p>""" % (REQUESTED, str(NOW))
F.write(TOP)

if ENABLE_JSON_OUTPUT:
    JFILE = open(JSON_OUT_FILE,'w')
    JFILE.write(("""{"category": "%s","sources": [""") % (REQUESTED))

for key, value in sourcesDict.items():
    # Building source as a 'Source' object using newspaper
    source = newspaper.build(value, language='en', fetch_images=False, memoize_articles=False)
    
    newsSourceTitle = """<hr /><a href="%s" target="_blank"><h2 style="color: teal;">%s</h2></a>""" % (value,key)
    F.write(newsSourceTitle)

    if ENABLE_JSON_OUTPUT: 
        JFILE.write(("""{"name": "%s","articles": [""") % (key))
    
    articleNum = 0
    while articleNum < NUM:
        try:
            article = source.articles[articleNum]
            url = article.url
            
            article.download()
            article.parse()
            article.nlp()
        except: 
            # Skip article parsing and display if unable to download article
            articleNum += 1
            continue

        newsArticle = """<h3>%s</h3><p>%s</p><p><a href=\"%s\" target=\"_blank\">Read more</a></p>""" % (article.title, article.summary,  url)
        F.write(newsArticle)

        if ENABLE_JSON_OUTPUT: 

            # Extracting article keywords and converting to a string that can be parsed in JSON format
            keysString = '['
            for item in article.keywords:
                keysString = keysString + ('\"' + item + '\"')
                if item != article.keywords[-1]: 
                    keysString = keysString + ','
            keysString = keysString + ']'

            # Writing article details to JSON file
            JFILE.write(("""{"title": "%s","url": "%s","summary": "%s","keywords": %s}""") % (article.title, url, article.summary.replace("\"","'").replace('\n',' '), keysString))
            if not(articleNum == (NUM - 1)): 
                JFILE.write(',')

        articleNum += 1
    
    if ENABLE_JSON_OUTPUT: 
        JFILE.write("""]}""")
        if not(key == list(sourcesDict.keys())[-1]): 
            JFILE.write(""",""")

# Ending HTML file
BOTTOM = """<hr /><p style="color: green;">Powered by NewsAggregator. Designed by <a href="http://amalbansode.com" target="_blank">Amal Bansode</a>.</p></body></html>"""
F.write(BOTTOM)
F.close()

if ENABLE_JSON_OUTPUT: 
    JFILE.write("""]}""")
    JFILE.close()

# Calculating tim
DONE = datetime.now()
TIMEDELTA = (DONE - NOW).total_seconds()
print('Done, took', TIMEDELTA, 'seconds')

# Opening HTML file in device's default browser
if OPEN_BROWSER: webbrowser.open('file://' + PATH + FILENAME)