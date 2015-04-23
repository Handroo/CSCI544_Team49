import sys
import nltk.data


topNNFile= open(sys.argv[1], 'r')
commentsFile= open(sys.argv[2], 'r')
NNMap = {}

def populateNNMap():
    NNLine = topNNFile.readline()
    while NNLine != "":
        noun = NNLine.replace("\n","")
        NNMap[noun]= noun
        NNLine = topNNFile.readline()

def read():
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    commentLine = commentsFile.readline()
    while commentLine != "":
        commentLine = commentLine.replace("\n","")
        commentTokens = commentLine.split()
        if isProfessor(commentTokens):
            print(commentLine)
            s = 1
        else:
            commentLine = unicode(commentLine, errors='ignore') 
            sentenceList =  tokenizer.tokenize(commentLine)
            for i in range(0,len(sentenceList)):
                if hasFeature(sentenceList[i]):
                    print sentenceList[i]
            
        commentLine = commentsFile.readline()

def isProfessor(commentArray):
    if len(commentArray) == 4:
            if commentArray[0].isdigit() and commentArray[3].isdigit() :
                return True

    return False

def hasFeature(sentence):
    hasfeature = False;
    sentenceTokens = sentence.split()
    for i in range(0,len(sentenceTokens)):
        if len(sentenceTokens[i]) == 1:
            if sentenceTokens[i] in NNMap:
                hasfeature = True
        else:
            newstr = sentenceTokens[i].replace(".", "").replace(",", "").replace("_", " ")
            if newstr.lower() in NNMap:
                hasfeature = True
    return hasfeature


def main():
    populateNNMap()
    read()


if __name__ == "__main__":
    # //store allthe nouns into a hashmap
    main()
    commentsFile.close()



