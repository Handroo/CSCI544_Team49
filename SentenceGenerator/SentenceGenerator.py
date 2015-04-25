import sys
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from random import randint

adjOverload = False
adjOverloadList = []
sentenceFile= open(sys.argv[1], 'r')
lastRand = -1
startList = ['', '','','', '','', 'The ', 'The ','The ', 'The ', 'The ','Students think ','Overall, ','Generally, ','Reviews say ']
posAdvList = ['','fortunately ', 'favorably ','conveniently ']
negAdvList = ['','unfortunately ', 'unluckily ']


def main():
    line = sentenceFile.readline()
    while line != "":
        if line != "\n":
            # print("S:"+line)
            line = line.replace("\n","")
            boolean = isProfessor(line)
            if(not boolean):
                print(makeSentence(line),end=" ")
            else:
                print("\n"+line)
        line = sentenceFile.readline()
    print("")

def sentimentAnalyzer(word):
    #Potential to fill later if we want to use sentiment analyzer
    result = 'neutral'
    # print("word: "+word)
    # opinions = swn.senti_synsets(word)
    # opinion = list(opinions)[0]
    # posScore = opinion.pos_score()
    # negScore =opinion.neg_score()
    # if(abs(posScore - negScore) > .4):
    #     if(posScore>negScore):
    #         result = 'positive'
    #     else:
    #         result = 'negative'
    # print(result)
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

def randStart(word):
    global lastRand
    if word.lower() == "he" or word.lower() == "she" or word.lower() == "it":
        return word[:1].upper() + word[1:]
    else:
        index = randint(0,len(startList)-1)
        while index == lastRand:
            index = randint(0,len(startList)-1)
        lastRand = index
        if index > 5:
            return (startList[index] + word)
        else:
            return (startList[index] + word[:1].upper() + word[1:])

def isplural(word):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural

def filterAdj(adjList):

    #lets remove synonyms first
    blacklistAdj = {}
    newAdjList = []
    for i in range(0,len(adjList)):
        word = adjList[i].split(':', 1)[0]
        count = adjList[i].split(':', 1)[1]
        # print("Analyzing "+word)
        if word[0] != "~":#is synonym
            # print("word: "+word)
            synList = getSynonyms(word)#list of synonyms
            valid = True
            for syn in synList:#for all the synonyms
                if syn in blacklistAdj:# ifsynonym is in blacklist
                    valid = False
            if word not in blacklistAdj and valid:
                newAdjList.append(adjList[i])
                for syn in synList:
                    # print("Adding to bl: "+syn)
                    blacklistAdj[syn] = count
        else:#if negative, get the antonyms and see if any are in blacklist or in the adjlist
            antList = getAntonyms(word[1:])
            blacklisted = False
            for ant in antList:
                if ant in blacklistAdj:
                    blacklisted = True
                else:
                    blacklistAdj[ant] = count


            if not blacklisted:
                newAdjList.append(adjList[i])

    #if we still ahev too much, then cut it down 
    if(len(newAdjList)>3):
        slimAdjList = []
        for adj in newAdjList:
            count = adj.split(':', 1)[1]
            if(count != '1'):
                slimAdjList.append(adj)
        if len(slimAdjList) == 0:
            newAdjList = newAdjList[:4]
        else:
            newAdjList = slimAdjList


    return newAdjList
def adjOverload(overloadList):
    global adjOverload, adjOverloadList
    adjOverload = True
    adjOverloadList = overloadList


def makeSentence(sentence):

    adjList = []
    noun = ""
    sentenceToken  = sentence.split()
    noun = sentenceToken[0]
    for i in range(2,len(sentenceToken)):
        adjList.append(sentenceToken[i])
    adjList = filterAdj(adjList)

    plural = isplural(noun)#check if noun is plural
    
    if(not plural):
        sentenceBuilder = randStart(noun) + " is " + checkNeg(adjList[0])
    else:
        sentenceBuilder = randStart(noun) + " are " + checkNeg(adjList[0])

    if(len(adjList)>1):
        for i in range(1,len(adjList)-1):
            sentenceBuilder += ", " +checkNeg(adjList[i])
        sentenceBuilder += " and "+ checkNeg(adjList[len(adjList)-1])
    sentenceBuilder+=". "
    # if adjOverload:
    #     sentenceBuilder+=" Others "
    return sentenceBuilder

def isProfessor(sentence):
    sentenceTokens = sentence.split()
    if len(sentenceTokens) == 4 and sentenceTokens[0].isdigit():
        return True
    else:
        return False

def checkNeg(word):
    # print(word)
    emphasis = ""
    count = word.split(':', 1)[1]
    if count == '2':
        emphasis = "very"
    elif count != '1':
        emphasis = "super"
    word = word.split(':', 1)[0]
    if word[0] == "~":
        return ("not "+word[1:])
    else:
        phrase = adverbPhrase(word)
        return emphasis+" " + phrase

def getAntonyms(word):
    allantonyms = {}
    antonyms = []
    for w in wn.synsets(word):
        lemmas = w.lemmas()[0].antonyms()
        for antonym in lemmas:
            antonyms.append(str(antonym.key()).split('%',1)[0])
        for a in antonyms:
            if a not in allantonyms:
                allantonyms[a] = a
    return allantonyms

def getSynonyms(word):
    allsynonyms = {}
    for s in  wn.synsets(word):
        s = s.name().split(".")[0]
        if s not in allsynonyms:
            allsynonyms[s] = s
    return allsynonyms

def isSimilar(word1):
    total = 0
    tot = []
    list1 = getAntonyms(word1)
    for l1 in list1:
    #     tot+=getSynonyms(l1)
    # for t in tot:
        print(l1)


    



if __name__ == "__main__":
    main()
    