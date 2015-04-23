import sys
from sys import stdout
from time import sleep
from stanford_parser.parser import Parser        

parser = Parser()

topNNFile= open(sys.argv[1], 'r', errors='ignore')
topJJFile= open(sys.argv[2], 'r', errors='ignore')
sentenceFile= open(sys.argv[3], 'r', errors='ignore')

NNMap = {}
JJMap = {}


def createPrunedSentenceFile():
    count = 0
    outputFile = open("PrunedSentences.txt",'w')
    sentenceLine = sentenceFile.readline()
    while sentenceLine != "":
        count +=1
        print("Analyzing Line "+str(count), end="\r")
        hasWord = False
        sentenceTokens = sentenceLine.split()
        for i in range(0,len(sentenceTokens)):
            currToken = sentenceTokens[i]
            if currToken in NNMap:
                hasWord = True
        if hasWord:
            outputFile.write(sentenceLine)
        sentenceLine = sentenceFile.readline()
            
    outputFile.close()

def populateNNMap():
    NNLine = topNNFile.readline()
    while NNLine != "":
        NNMap[NNLine]= NNLine
        NNLine = topNNFile.readline()

def populateJJMap():
    JJLine = topJJFile.readline()
    while JJLine != "":
        JJMap[JJLine]= JJLine
        JJLine = topJJFile.readline()

def p():
        
        dependencies = parser.parseToStanfordDependencies("Pick up the tire pallet.")

        tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]
        print(tupleResult)

def main():
    # populateNNMap()
    # createPrunedSentenceFile()
    p()


if __name__ == "__main__":
    # //store allthe nouns into a hashmap
    main()
    topJJFile.close()
    topNNFile.close()
    sentenceFile.close()



