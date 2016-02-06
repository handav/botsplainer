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



def cleanConnection(rel):
    switcher = {
        "HasA": "has a",
        "RelatedTo": "related to",
        "IsA": "is a",
        "HasProperty": "has property",
        "DerivedFrom": "derived from",
        "adverbPertainsTo": "adverb pertains to",
        "SimilarTo": "similar to",
        "AtLocation": "at location",
        "SimilarTo": "similar to"
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
        for edge in edges:
            relation = edge['start'], edge['rel'], edge['end']
            print '\n'
            print word
            print relation
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
                        print relSplit[3]
                    else:
                        relevantWords = relevantWords + ' ' +cleanConnection(relSplit[2])
                        print relSplit[2]

                #relevantWords = relevantWords.split('_')
            textString = relevantWords

            global translation 
            if len(translation) > 0:
                translation = translation + ', ' + textString
            else:
                translation = textString
            print relevantWords


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

print translation