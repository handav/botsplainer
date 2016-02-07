#only english?
#take out punctuation


import requests
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#NLTK VARIABLES
commonwords = stopwords.words('english')
lemma = nltk.wordnet.WordNetLemmatizer()
punctuation = ['.','?','!',',']

#SAMPLE TEXT
sampleT1 = '...oh, right, I should write a lambda function, duh.'
sampleT2 = 'the quick brown fox jumps over the lazy dog'
sampleT3 = 'why is growth so important, when you have the most influential people on the planet accessible here? Tell that story.'

textToAnalyze = sampleT3

tokenizedText = word_tokenize(textToAnalyze)
tokens_pos = pos_tag(tokenizedText)
translation = ''

textStrings = []



def cleanConnection(rel):
    switcher = {
        "HasA": "has a",
        "RelatedTo": "is related to",
        "IsA": "is a",
        "HasProperty": "is",
        "DerivedFrom": "is derived from",
        "adverbPertainsTo": "pertains to",
        "SimilarTo": "similar to",
        "AtLocation": "at location",
        "Antonym": "is an antonym of",
        "Synonym": "is a synonym of"
    }

    return switcher.get(rel, rel)


def makeRequest(word):
    requestString = 'http://conceptnet5.media.mit.edu/data/5.4/c/en/' + word + '?limit=3'
    resp = requests.get(requestString)
    if resp.status_code != 200:
        # something went wrong
        print "ERROR", resp.status_code
        #raise ApiError('GET error'.format(resp.status_code))
    else:
        information = resp.json()
        edges=information['edges']
        numFound = information['numFound']

        edgeString = ""
        if (numFound > 0):
            edgeString = word.upper()+": "

        for edge in edges:
            relation = edge['start'], edge['rel'], edge['end']
            relevantWords = ''
            for rel in relation:
                relSplit = rel.split('/')
                if relSplit[1] == 'c':
                    language = relSplit[2]
                    #THIS ISN'T ALWAYS RIGHT
                    lastWord = relSplit[len(relSplit)-1]
                    if len(lastWord)>1:
                        relevantWords = relevantWords + ' ' + relSplit[len(relSplit)-1]
                    else:
                        relevantWords = relevantWords + ' ' + relSplit[len(relSplit)-2]
                elif relSplit[1] == 'r':
                    if len(relSplit) > 3:
                        relevantWords = relevantWords + ' ' +cleanConnection(relSplit[3])
                    else:
                        relevantWords = relevantWords + ' ' +cleanConnection(relSplit[2])

            relevantWords = ' '.join(relevantWords.split('_')) + ","
            edgeString = edgeString + relevantWords
        textStrings.append(edgeString)


for i, word in enumerate(tokens_pos):
    word = tokens_pos[i][0]
    wordPos = tokens_pos[i][1]
    if ('V' in wordPos or 'MD' in wordPos):
        word = lemma.lemmatize(word, 'v')
    elif ('NN' in wordPos or 'PRP' in wordPos or 'WP' in wordPos or 'CD' in wordPos):
        word = lemma.lemmatize(word, 'n')
    else:
        word = lemma.lemmatize(word)
    if (word not in commonwords and word not in punctuation):
        makeRequest(word)

textStrings = ' '.join(textStrings)
print textStrings


