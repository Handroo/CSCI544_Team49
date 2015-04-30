import sys
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from random import randint

MODULE = '/users/tom/desktop/pattern'
import sys
if MODULE not in sys.path: sys.path.append(MODULE)
from pattern.en import pluralize, singularize

adjOverload = False
adjOverloadList = []
sentenceFile= open(sys.argv[1], 'r')
lastRand = -1
startList = ['', '','','', '','', 'The ', 'The ','The ', 'The ', 'The ','Students think ','Overall, ','Generally, ','Reviews say ']
posAdvList = ['','fortunately ', 'favorably ','conveniently ']
negAdvList = ['','unfortunately ', 'unluckily ']



# completeProfessorFeatues = {}
professorFeatures = {}

def main():
    global completeProfessorFeatues
    global professorFeatures
    line = sentenceFile.readline()
    while line != "":
        if line != "\n":
            #check if professor, if isn;t add to professir line, if is, copy the old dict to a new one, and empty the old dict
            line = line.replace("\n","")
            if not isProfessor(line):
                # print line
                profAdj = []
                tokens = line.split()
                for i in range(2,len(tokens)):
                    profAdj.append(tokens[i])
                professorFeatures[tokens[0]] = profAdj
            else:#it is a professor
                #run the analyzer on the professor features 
                generateSummary()
                print("")
                print(line)
                # completeProfessorFeatues = professorFeatures
                professorFeatures = {}

        line = sentenceFile.readline()
    generateSummary()

def generateSummary():
    global professorFeatures
    weedSimilarNouns()
    weedSimilarAdjectives()
    constructSentences()


    # for key in professorFeatures:
    #     print("key-----> "+key)
    #     for a in professorFeatures[key]:
    #         print(a)

    #before you print sentences, make sure you know if the adjectives sentiment are conflicting

def weedSimilarNouns():
    global professorFeatures
    newFeatures = {}
    weededFeatures = {}
    for key in sorted(professorFeatures.keys()):
        if key not in weededFeatures:

            newFeatures[key] = professorFeatures[key]# add feature to new list
            synonyms = getSynonyms(key) # get synonyms for key
            otherKeys = [] # to check similar keys
            otherKeys.append( getPluralSingular(key) )# add plural to simialr key set
            for k in synonyms:
                otherKeys.append( getPluralSingular(k) ) # add plural/singular of synonyms
            otherKeys += synonyms # add original synonyms

            for key2 in sorted(professorFeatures.keys()):
                for otherKey in otherKeys:
                    if otherKey == key2 and key != key2:#then you have a duplicate, you need to combine the list then
                        weededFeatures[otherKey] = otherKey
                        newFeatures[key] += professorFeatures[otherKey]
    professorFeatures = newFeatures

def weedSimilarAdjectives():
    global professorFeatures
    for key in professorFeatures:
        weededOpinions = {}
        newOpinions = {}
        opinionList = professorFeatures[key]
        

        for opinion in opinionList:
            opinion = opinion.split(':', 1)[0]
            if opinion == "~easy":
                opinion = "hard"
            if opinion == "~hard" or opinion == "~difficult":
                opinion = "easy"
            if opinion == "~good":
                opinion = "bad"
            if opinion == "~bad":
                opinion = "good"
            if opinion == "~boring":
                opinion = "exciting"
            if opinion not in weededOpinions: # opinion is new we need to handle negatives too!
                newOpinions[opinion] = opinion
                weededOpinions[opinion] = opinion
                if opinion[:1] == "~":
                    if len(getAntonyms(opinion[1:]).keys()) != 0:
                        opinion = getAntonyms(opinion[1:]).keys()[0]
                        weededOpinions[opinion] = opinion
                #Add to weeded opinions
                for o in getSynonyms(opinion):
                    weededOpinions[o] = o
                for o in getAntonyms(opinion):
                    weededOpinions["~"+o] = "~"+o
        professorFeatures[key] = newOpinions

def constructSentences():
    global professorFeatures
    for key in professorFeatures:
        noun = key
        adjectives = professorFeatures[key]
        adjectives = adjectives.keys()
        posAdjectives = []
        negadjectives = []
        for a in adjectives:
            # print(a)
            if sentiment(a) == 'neg':
                # print("neg")
                negadjectives.append(a)
            else:
                # print("pos")
                posAdjectives.append(a)
        if len(adjectives) == 1 :
            oneOpinionList[randint(0,len(oneOpinionList)-1)](noun,posAdjectives,negadjectives)
        if len(adjectives) == 2 :
            twoOpinionList[randint(0,len(twoOpinionList)-1)](noun,posAdjectives,negadjectives)
        if len(adjectives) == 3 :
            threeOpinionList[randint(0,len(threeOpinionList)-1)](noun,posAdjectives,negadjectives)
        if len(adjectives) == 4 :
            fourOpinionList[randint(0,len(fourOpinionList)-1)](noun,posAdjectives,negadjectives)
        if len(adjectives) > 4 :
            largeGenerator(noun,posAdjectives,negadjectives)
            # make function for above 4

    #decide if there are conflicting sentiments
        #if are, then split it into two fragments
def capitalize(word):
    return word.lower()[:1].upper() + word.lower()[1:]
def aOrAn(word):
    if word[:1].lower() == 'a' or word[:1].lower() == 'e' or word[:1].lower() == 'i' or word[:1].lower() == 'o' or word[:1].lower() == 'u':
        return "An"
    else:
        return "A"

def oneGenerator1(noun,adjective,negadjectives):
    sentence = ""
    neg = correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:
        if noun.lower() == "he" or noun.lower() == "she":
            sentence +=capitalize(noun)+" is "+negadjectives[0]+"."
        else:
            if isplural(noun):
                sentence +="The "+noun+" are "+negadjectives[0]+"."
            else:
                sentence +="The "+noun+" is "+negadjectives[0]+"."
    else:
        starters = ['The ','The ','The ','Reviewers say ', 'Sometimes the ','Often the ','Generally speaking, the ','Overall, the ']
        if not neg:
            if noun.lower() == "he" or noun.lower() == "she":
                sentence +=capitalize(noun)+" is "+adjective[0]+"."
            else:
                sentence += starters[randint(0,len(starters)-1)]+ noun+" will be "+adjective[0]+"."
        else:
            if noun.lower() == "he" or noun.lower() == "she":
                sentence +=capitalize(noun)+" is not going to be "+adjective[0].split()[1]+"."
            else:
                sentence += starters[randint(0,len(starters)-1)]+ noun+" will not be "+adjective[0].split()[1]+"."
    print (sentence),

def oneGenerator2(noun,adjective,negadjectives):
    sentence = ""
    neg = correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:#could be one or two
        if noun.lower() == "he" or noun.lower() == "she":
            sentence += capitalize(noun)+"\'s "+negadjectives[0]+"."
        elif isplural(noun):
            sentence += capitalize(noun)+" are "+negadjectives[0]+"."
        else:
            sentence += capitalize(noun)+" is "+negadjectives[0]+"."
    else:
        if not neg:
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+adjective[0]+"."
            elif isplural(noun):
                sentence +=capitalize(adjective[0])+" "+noun+"."
            else:
                sentence += aOrAn(adjective[0])+" "+adjective[0]+" "+noun+"."
        else:
            if isplural(noun):
                sentence += capitalize(noun)+" are not very "+adjective[0].split()[1]+"."
            else:
                sentence += "Not a very "+adjective[0].split()[1]+" "+noun+"."
    print (sentence),

def twoGenerator1(noun,adjective,negadjectives):
    sentence = ""
    correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:#could be one or two
        if len(negadjectives) == 1:
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += "While "+noun+"\'s "+adjective[0]+", "+noun+"\'s also "+negadjectives[0]+"!"
            elif isplural(noun):
                sentence += "Some say "+noun+" are "+negadjectives[0]+", but also "+adjective[0]+"."
            else:
                sentence += capitalize(noun)+" is "+negadjectives[0]+", but "+adjective[0]+"."
        else:#two negative 0 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+" and "+negadjectives[1]+"!"
            elif isplural(noun):
                sentence += capitalize(noun)+" are regrettably "+negadjectives[0]+" and "+negadjectives[1]+"."
            else:
                sentence += capitalize(noun)+" is both "+negadjectives[0]+" and "+negadjectives[1]+"."
    else:
        if noun.lower() == "he" or noun.lower() == "she":
                sentence +=capitalize(noun)+"\'s "+adjective[0]+" and "+adjective[1]+". "
        elif isplural(noun):
            sentence += capitalize(adjective[0])+ " and "+adjective[1]+" "+noun+"."
        else:
            sentence += aOrAn(adjective[0])+" "+adjective[0]+ " and "+adjective[1]+" "+noun+"."
    print (sentence),

def twoGenerator2(noun,adjective,negadjectives):
    sentence = ""
    correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:#could be one or two
        if len(negadjectives) == 1:
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize( noun)+"\'s "+adjective[0]+", but "+negadjectives[0]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+", but they are also "+adjective[0]+"!"
            else:
                sentence += capitalize(noun)+" is "+negadjectives[0]+",but "+adjective[0]+"."
        else:#two negative 0 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+" and also "+negadjectives[1]+". Beware!"
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+" and "+negadjectives[1]+"."
            else:
                sentence += capitalize(noun)+" is "+negadjectives[0]+" and "+negadjectives[1]+"."
    else:
        if noun.lower() == "he" or noun.lower() == "she":
                sentence +=capitalize(noun)+" seems "+adjective[0]+" and "+adjective[1]+". "
        elif isplural(noun):
            sentence += capitalize(noun) +" are "+adjective[0]+ " and "+adjective[1]+"."
        else:
            sentence += capitalize(noun) +" is "+adjective[0]+ " and "+adjective[1]+"."
    print (sentence),

def threeGenerator1(noun,adjective,negadjectives):
    sentence = ""
    correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:#could be one or two or three
        if len(negadjectives) == 1:# 1 neg 2 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize( noun)+"\'s "+negadjectives[0]+", but "+adjective[0]+" and "+adjective[1]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+". However, they also can be "+adjective[0]+" and "+adjective[1]+ "."
            else:
                sentence += capitalize(noun)+" is "+negadjectives[0]+", but is also "+adjective[0]+" and "+adjective[1]+"."
        elif len(negadjectives) == 2:#two negative 1 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += "Even though "+noun+"\'s "+adjective[0]+", "+noun+"\'s also "+negadjectives[0]+" and "+negadjectives[1]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+", "+negadjectives[1]+", but "+adjective[0]+"."
            else:
                sentence += capitalize(noun)+" is "+adjective[0]+", but "+negadjectives[0]+" and also  "+negadjectives[1]+"."
        else:#3 negative 0 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+", "+negadjectives[1]+ " and "+negadjectives[2]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are sadly "+negadjectives[0]+", "+negadjectives[1]+" and "+negadjectives[2]+ "."
            else:
                sentence += capitalize(noun)+" is "+negadjectives[0]+", "+negadjectives[1]+" and "+negadjectives[2]+"."
    else:
        if noun.lower() == "he" or noun.lower() == "she":
                sentence +=capitalize(noun)+"\'s "+adjective[0]+" and "+adjective[1]+". People say "+noun+ " is also "+adjective[2]+". "
        elif isplural(noun):
            sentence += capitalize(adjective[0])+", "+adjective[1]+","+ " and "+adjective[2]+" "+noun+"."
        else:
            sentence += capitalize(noun)+ " will be "+adjective[0]+ " and "+adjective[1]+". Sometimes "+adjective[2]+". "
    print (sentence),

def threeGenerator2(noun,adjective,negadjectives):
    sentence = ""
    correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:#could be one or two or three
        if len(negadjectives) == 1:# 1 neg 2 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(negadjectives[0])+" professor, but "+noun+"\'s also "+adjective[0]+" and "+adjective[1]+"."
            elif isplural(noun):
                sentence += capitalize(negadjectives[0])+" "+noun+". But others think they can be "+adjective[0]+" and "+adjective[1]+ "."
            else:
                sentence += capitalize(noun)+" seems "+negadjectives[0]+". But others say "+adjective[0]+" and "+adjective[1]+"."
        elif len(negadjectives) == 2:#two negative 1 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += "Even though "+noun+"\'s "+adjective[0]+", "+noun+"\'s "+negadjectives[0]+" and "+negadjectives[1]+"."
            elif isplural(noun):
                sentence += capitalize(negadjectives[0])+" and "+negadjectives[1]+ " "+noun+". But sometimes can be "+adjective[0]+"."
            else:
                sentence += capitalize(noun)+" is "+adjective[0]+", but "+negadjectives[0]+" and also  "+negadjectives[1]+"."
        else:#3 negative 0 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+", "+negadjectives[1]+ " and "+negadjectives[2]+"."
            elif isplural(noun):
                sentence += "Beware! "+noun+" are "+negadjectives[0]+", "+negadjectives[1]+" and "+negadjectives[2]+ "."
            else:
                sentence += "Warning! "+noun+" is "+negadjectives[0]+", "+negadjectives[1]+" and "+negadjectives[2]+"."
    else:
        if noun.lower() == "he" or noun.lower() == "she":
                sentence +=capitalize(noun)+"\'s "+adjective[0]+" and "+adjective[1]+". People say "+capitalize(noun)+ " is also "+adjective[2]+". "
        elif isplural(noun):
            sentence += capitalize(adjective[0])+" ,"+adjective[1]+ " and "+adjective[2]+" are three words that describe the "+noun+"."
        else:
            sentence += "The "+noun+" can be "+adjective[0]+" ,"+adjective[1]+ " and "+adjective[2]+" "+noun+"."
    print (sentence),


def fourGenerator1(noun, adjective,negadjectives):
    sentence = ""
    correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:#could be one or two or three
        if len(negadjectives) == 1:# 1 neg 3 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(negadjectives[0])+" professor, but "+noun+"\'s also "+adjective[0]+" ,"+adjective[1]+" and "+adjective[2]+"."
            elif isplural(noun):
                sentence += capitalize(negadjectives[0])+" "+noun+". But can be "+adjective[0]+" ,"+adjective[1]+" and "+adjective[2]+ "."
            else:
                sentence += capitalize(noun)+" may be "+negadjectives[0]+". Some say is "+adjective[0]+" ,"+adjective[1]+" and "+adjective[2]+ "."
        elif len(negadjectives) == 2:#two negative 2 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += "While "+noun+"\'s "+adjective[0]+" and "+adjective[1] +", "+noun+"\'s "+negadjectives[0]+" and "+negadjectives[1]+"."
            elif isplural(noun):
                sentence += capitalize(negadjectives[0])+" and "+negadjectives[1]+ " "+noun+". But can be "+adjective[0]+" and "+ adjective[1] +" ."
            else:
                sentence += capitalize(noun)+" is "+adjective[0]+" and "+ adjective[1] +" though "+negadjectives[0]+" and  "+negadjectives[1]+"."
        elif len(negadjectives) == 3:#3 negative 1 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+", "+negadjectives[1]+ " and "+negadjectives[2]+", but can be "+adjective[0]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+", "+negadjectives[1]+", "+negadjectives[2]+ ", but "+adjective[0]+"."
            else:
                sentence += capitalize(adjective[0])+" "+noun+". But also "+negadjectives[0]+", "+negadjectives[1]+" and "+negadjectives[2]+"."
        else:
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+", "+negadjectives[1]+ ", "+negadjectives[2]+" and "+negadjectives[3]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+", "+negadjectives[1]+", "+negadjectives[2]+" and "+negadjectives[3]+"."
            else:
                sentence += capitalize(noun)+" is "+negadjectives[0]+", "+negadjectives[1]+", "+negadjectives[2]+" and "+negadjectives[3]+"."
    else:
        if noun.lower() == "he" or noun.lower() == "she":
            sentence += aOrAn(adjective[0])+" "+adjective[0]+" and "+adjective[1]+" professor, "+noun.lower() +" is "+ adjective[2]+ " and "+adjective[3]+"."
        else:
            sentence += "The "+ noun+" appears to be "+adjective[0]+" and "+adjective[1]+". Others also say that it is also "+adjective[2]+" and "+adjective[3]+"." 
    print (sentence),

def fourGenerator2(noun, adjective,negadjectives):
    sentence = ""
    correctNegative(adjective)
    correctNegative(negadjectives)
    if len(negadjectives) >0:#could be one or two or three
        if len(negadjectives) == 1:# 1 neg 3 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(negadjectives[0])+" professor, but "+noun+"\'s also "+adjective[0]+" ,"+adjective[1]+" and "+adjective[2]+"."
            elif isplural(noun):
                sentence += capitalize(negadjectives[0])+" "+noun+". But can be "+adjective[0]+" ,"+adjective[1]+" and "+adjective[2]+"."
            else:
                sentence += capitalize(noun)+" may be "+negadjectives[0]+". Some say is "+adjective[0]+" ,"+adjective[1]+" and "+adjective[2]+ "."
        elif len(negadjectives) == 2:#two negative 2 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += "While "+noun+"\'s "+adjective[0]+" and "+adjective[1] +", "+noun+"\'s "+negadjectives[0]+" and "+negadjectives[1]+"."
            elif isplural(noun):
                sentence += capitalize(negadjectives[0])+" and "+negadjectives[1]+ " "+noun+". But can be "+adjective[0]+" and "+ adjective[1] +" ."
            else:
                sentence += capitalize(noun)+" is "+adjective[0]+" and "+ adjective[1] +" though "+negadjectives[0]+" and  "+negadjectives[1]+"."
        elif len(negadjectives) == 3:#3 negative 1 pos
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+", "+negadjectives[1]+ " and "+negadjectives[2]+", but can be "+adjective[0]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+", "+negadjectives[1]+", "+negadjectives[2]+ ", but "+adjective[0]+"."
            else:
                sentence += capitalize(adjective[0])+" "+noun+". But also "+negadjectives[0]+", "+negadjectives[1]+" and "+negadjectives[2]+"."
        else:
            if noun.lower() == "he" or noun.lower() == "she":
                sentence += capitalize(noun)+"\'s "+negadjectives[0]+", "+negadjectives[1]+ ", "+negadjectives[2]+" and "+negadjectives[3]+"."
            elif isplural(noun):
                sentence += capitalize(noun)+" are "+negadjectives[0]+", "+negadjectives[1]+", "+negadjectives[2]+" and "+negadjectives[3]+"."
            else:
                sentence += capitalize(noun)+" is "+negadjectives[0]+", "+negadjectives[1]+", "+negadjectives[2]+" and "+negadjectives[3]+"."
    else:
        if noun.lower() == "he" or noun.lower() == "she":
                sentence +=capitalize(noun)+" is a very good professor: "+adjective[0]+", "+adjective[1]+", "+adjective[2]+" and "+adjective[3]+". "
        else:
            sentence += "The "+ noun+" will be "+adjective[0]+", "+adjective[1]+", "+adjective[2]+" and "+adjective[3]+"."
    print (sentence),



def largeGenerator(noun, adjective,negadjectives):
    sentence = ""
    correctNegative(adjective)
    correctNegative(negadjectives)
    alladjectives = adjective+negadjectives
    if len(adjective) == 0:
        if noun.lower() == "he" or noun.lower() == "she":
            sentence+="Bad reviews for him. Students think he's: "+alladjectives[0]
        elif noun.lower() == "she":
            sentence+="Bad reviews for her. Reviews state she is "+alladjectives[0]
        else:
            sentence+="Negative reviews for "+noun+" saying: "+alladjectives[0]
        for i in range(1,len(alladjectives)-1):
            sentence+= ", "+alladjectives[i]
        sentence+= " and "+alladject    ives[len(alladjectives)-1]+"."
    elif len(negadjectives) == 0:
        if noun.lower() == "he" or noun.lower() == "she":
            sentence+="Great reviews for him. Students think he's: "+alladjectives[0]
        elif noun.lower() == "she":
            sentence+="Great reviews for her. Reviews state she is "+alladjectives[0]
        else:
            sentence+="Positive reviews for "+noun+" saying: "+alladjectives[0]
        for i in range(1,len(alladjectives)-1):
            sentence+= ", "+alladjectives[i]
        sentence+= " and "+alladjectives[len(alladjectives)-1]+"."
    else:
        if noun.lower() == "he" or noun.lower() == "she":
            sentence+="Multiple reviews for him but reviews say he is: "+alladjectives[0]
        elif noun.lower() == "she":
            sentence+="Multiple reviews for her but reviews say she is "+alladjectives[0]
        else:
            sentence+="Mixed reviews for "+noun+" but reviews say: "+alladjectives[0]
        for i in range(1,len(alladjectives)-1):
            sentence+= ", "+alladjectives[i]
        sentence+= " and "+alladjectives[len(alladjectives)-1]+"."
    print (sentence),
    
def correctNegative(adjective):
    neg = False;
    for i in range(0,len(adjective)):
        if adjective[i][:1] == "~":
            neg = True
            adjective[i] = "not "+adjective[i][1:]
    return neg

def getPluralSingular(w):
    word = w
    plural = isplural(word)
    if plural:
        word  = singularize(word)
    else:
        word  = pluralize(word)
    return word


def isplural(word):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural



def isProfessor(sentence):
    sentenceTokens = sentence.split()
    if len(sentenceTokens) == 4 and sentenceTokens[0].isdigit():
        return True
    else:
        return False


def getAntonyms(word):
    allantonyms = {}
    antonyms = []
    for w in wn.synsets(word):
        lemmas = w.lemmas()[0].antonyms()
        for antonym in lemmas:
            antonyms.append(str(antonym.key()).split('%',1)[0])
            lemma = w.lemma_names()
            for name in lemma:
                antonyms.append(name)
        for a in antonyms:
            if a not in allantonyms:
                allantonyms[a] = a
    return allantonyms

def getSynonyms(word):
    allsynonyms = {}
    synonyms = []
    for s in  wn.synsets(word):
        synonyms.append(s.name().split(".")[0])
        lemma =  s.lemma_names()
        for name in  lemma:
            synonyms.append(name)
        for s in synonyms:
            if s not in allsynonyms:
                allsynonyms[s] = s
    return allsynonyms

def sentiment(word):
    # print word
    posScore = 0
    negScore = 0
    if word[:1] == "~" and len(getAntonyms(word[1:])) != 0:
        word = getAntonyms(word[1:]).keys()[0]
    opinions = swn.senti_synsets(word)
    for o in list(opinions):
        negScore += o.neg_score()
        posScore += o.pos_score()
    # print "POS " + str(posScore)
    # print "NEG " + str(negScore)
    negWords = ['rude','arrogant','boring','difficult','terrible','hard','dull','long','tricky','impossible','long','intimidating','ridiculous','tough','challenging']
    posWords = ['exciting', 'cool','smart','incredible','super','great','good','excellent','engaging','clear','entertaining','interesting','easy','straightforward','helpful','amazing','awesome','related','funny','doable']
    if word.lower() in negWords:
        return 'neg' 
    elif word.lower() in posWords:
        return 'pos'
    if word[:1] == "~":
        if word[1:].lower() in negWords:
            return 'pos'
        elif word[1:].lower() in posWords:
            return 'neg'

    if posScore > negScore:
        return 'pos'
    elif posScore < negScore:
        return 'neg'
    else:
        return 'neut'
    
oneOpinionList = [oneGenerator1,oneGenerator2]
twoOpinionList = [twoGenerator1,twoGenerator2]
threeOpinionList = [threeGenerator1,threeGenerator2]
fourOpinionList = [fourGenerator1, fourGenerator2]

if __name__ == "__main__":
    main()
    # weedNouns()
    # synonyms = getAntonyms('bad')
    # for s in synonyms:
    #     print s
    # w = "~bad"
    # print w+" -> "+sentiment(w)



    