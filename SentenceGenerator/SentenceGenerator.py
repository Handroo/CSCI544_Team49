import sys
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
from random import randint

sentenceFile= open(sys.argv[1], 'r')

startList = ['The ','Students say ','Most of the time, ','You will notice that ']
posAdvList = ['','fortunately ', 'favorably ','conveniently ']
negAdvList = ['','unfortunately ', 'unluckily ']

def main():
    line = sentenceFile.readline()
    while line != "":
        line = line.replace("\n","")
        boolean = isProfessor(line)
        if(not boolean):
            print(makeSentence(line),end=" ")
        line = sentenceFile.readline()
    print("")

def sentimentAnalyzer(word):
    result = 'neutral'
    list(swn.senti_synsets('slow'))
    opinion = swn.senti_synsets(word)
    opinion0 = list(opinion)[0]
    posScore = opinion0.pos_score()
    negScore =opinion0.neg_score()
    if(abs(posScore - negScore) > .4):
        if(posScore>negScore):
            result = 'positive'
        else:
            result = 'negative'

    return result

def adverbPhrase(adjective):

    opinion = sentimentAnalyzer(adjective)
    adverb = randAdverb(opinion)
    if(adverb is None):
        return adjective
    else:
        return adverb+adjective


def randAdverb(opinion):
    if opinion == 'positive':
        index = randint(0,len(posAdvList)-1)
        return posAdvList[index]
    elif opinion == 'negative':
        index = randint(0,len(negAdvList)-1)
        return negAdvList[index]

def randStart():
    index = randint(0,len(startList)-1)
    return startList[index]

def isplural(word):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural

def makeSentence(sentence):
    sentenceToken  = sentence.split()
    plural = isplural(sentenceToken[0])
    if(not plural):
        sentenceBuilder = randStart() + sentenceToken[0] + " is " + checkNeg(sentenceToken[1])
    else:
        sentenceBuilder = randStart() + sentenceToken[0] + " are " + checkNeg(sentenceToken[1])

    if(len(sentenceToken)>2):
        for i in range(2,len(sentenceToken)-1):
            sentenceBuilder += ", " +checkNeg(sentenceToken[i])
        sentenceBuilder += " and "+ checkNeg(sentenceToken[len(sentenceToken)-1])
    sentenceBuilder+="."
    return sentenceBuilder

def isProfessor(sentence):
    if sentence == "__Professor__":
        return True
    else:
        return False

def checkNeg(word):
    if word[0] == "~":
        return ("not "+word[1:])
    else:
        phrase = adverbPhrase(word)
        return phrase

if __name__ == "__main__":
    main()
    # result = sentimentAnalyzer('difficult')
    # print(result)
    sentenceFile.close()