#AUTHOR:    Tom Harden
#DATE:      20 April 2017

#This is a Python3 script to for checking the word frequency of documents of text.
#Every word in the file (*.doc or *.txt) is then scored, and the score is recorded in a dict:
#     for every word a sentence contains more than once, it receives a score of +10
#     for every word a paragraph contains more than once, it recieves a score of +4
#     for every word that is used in a file, it receive a score of its total word count (ie +1).
#The user is then presented these words in order of frequency score.
#The user may update the scoring by pressing enter.
#The user must exit the program and relaunch it to score a new file.

############################################################
####################    IMPORTS         ####################
############################################################
from docx import Document#necessary to read MS docx files!  WIthout it, limited to only reading text files ans ASCII characters!
from file_manipulation import * #imports all functions pertaining to file_manipulation. NOT ALL FUNCTIONS FROM THE CLASS ARE USED (unsafe?)

############################################################
####################    FUNCTIONS       ####################
############################################################
#updates the scoring dictionary based on the specified list (sentence, paragraph, or file).
#   The first occurrence of a word is given a score of 1.  The penalty for the first occurrence is
#   "1". Additional occurences recieve the specified penalty.
#@param list l is a list of all words in a body of text (either sentence, paragraph, or file)
#@param dictionary d is a dict which scores the frequencies of the words in all bodies of text
#@param int penalty is the size of the penalty to be added to the word's frequency score.
def updateScores(l, d, penalty):
    alreadyUsedElts = list()#used to track the elts as they occur for scoring purposes
    for elt in l:
        if elt in d:
            if alreadyUsedElts.count(elt) > 0:
                d[elt] += penalty
            else:
                alreadyUsedElts.append(elt)
                d[elt] += 1
        else:
            alreadyUsedElts.append(elt)
            d[elt] = 1

#converts a string to a list using specified characters as delimiters
#@param string s is the string to be converted into a list.
#@return list l is the list made from s
def delimitStringToList(s):
    l = list()
    tmpStr = ""
    for char in s:
        if isRunonPunctuation(char) or isMiscPunctuation(char) or char == " ":
            if tmpStr != "":
                l.append(tmpStr)
            tmpStr = ""
        elif char == "\n":
            if tmpStr != "":
                l.append(tmpStr)
            l.append(char)
            tmpStr = ""
        else:
            tmpStr += char
    if tmpStr != "":
        l.append(tmpStr)
    return l

#returns true if the specified character is punctuation for ending sentences
def isEndingPunctuation(c):
    return c == '.' or c == '!' or c == '?' or c == ';'
#returns true if the specified character is punctuation for sentence breaks
def isRunonPunctuation(c):
    return c == "," or c == "\t" or c == ':'
#returns true if the specified character is punctuation for that has various purposes
def isMiscPunctuation(c):
    return c == "\"" or c == "(" or c == ")"
#returns true if the specified character is punctuation
def isPunctuation(c):
    return isEndingPunctuation(c) or isRunonPunctuation(c) or isMiscPunctuation(c)

#converts a dictionary's keys and their values to a sorted list, sorted by the values stored at the dictionary's keys
#@param dictionary d is a dict of words as keys, and the value stored at the key corresponds with the word's frequency score
#@return list l the sorted list of dictionary keys and values based on the value of the keys.
def convertToSortedList(d):
    l = list()
    for k,v in d.items():
        l.append((v, k))
    return sorted(l, key=lambda x: x[0])

#returns the number of elts in a list
def getLength(l):
    totalWords = 0
    for elt in l:
        totalWords += 1
    return totalWords

############################################################
####################    PROGRAM MAIN    ####################
############################################################
SAME_SENTENCE_PENALTY = 10;#returns true if the specified character is punctuation for ending sentences
SAME_PARAGRAPH_PENALTY = 4;#returns true if the specified character is punctuation for ending sentences
SAME_FILE_PENALTY = 1;#returns true if the specified character is punctuation for ending sentences

f = getFileAttributes()#get a tuple consisting of (the parent directory, filename, and file extension)

while(True):
    s = fileToString(f[0], f[1], f[2]).upper()#converts the text of the file to all upper case (this takes care of dealing with comparing words of differing cases)
    allWords = delimitStringToList(s)#takes out all spaces, only leaves returns
    fileWordCount, paragraphWordCount, sentenceWordCount = list(), list(), list()

    allWordScores = dict()
    for word in allWords:
        #remove punctuation from the end of words
        if isEndingPunctuation(word[-1]) == False:
            sentenceWordCount.append(word)
        else:#move onto new sentence
            word = word[:-1]
            sentenceWordCount.append(word)#add the last word minus the punctuation
            updateScores(sentenceWordCount, allWordScores, SAME_SENTENCE_PENALTY)
            sentenceWordCount.clear()

        #separate into paragraphs (the returns have already been removed and are treated as individual words!)
        if word != "\n" and word != "\r\n":
            paragraphWordCount.append(word)
        else:#move onto new paragraph
            updateScores(paragraphWordCount, allWordScores, SAME_PARAGRAPH_PENALTY)
            paragraphWordCount.clear()

        #update file Count
        fileWordCount.append(word)

    updateScores(fileWordCount, allWordScores, SAME_FILE_PENALTY)
    updateScores(paragraphWordCount, allWordScores, SAME_PARAGRAPH_PENALTY)
    updateScores(sentenceWordCount, allWordScores, SAME_SENTENCE_PENALTY)

    allWords = dict()#reassign list allWords into a dict()
    updateScores(fileWordCount, allWords, 1)#This is to get the total number of times the word was used in the file!

    print("\n+____________________________________________\n")
    print (" _Freq_\t_Total_\t_Word_")
    totalWords = getLength(convertToSortedList(allWordScores))
    count = 0
    for elt in convertToSortedList(allWordScores):
        if elt[1] != "\n":
            print (" " + str(elt[0]) + "\t" + str(allWords[elt[1]]) + "\t" + elt[1])
        else:
            print (" " + str(elt[0]) + "\t" + str(allWords[elt[1]]) + "\t" + "<CARRIAGE RETURN>")
        count += 1
        if ((totalWords - count) % 25 == 0) and (totalWords - count >= 5):
            print(" ----------- Top " + str(totalWords - count) + " -----------")

    print("Scoring complete.\nTotal Vocab used: " + str(totalWords) + " different words.\n")
    input("Hit \'enter\' to refresh the scores\n\n")
print("Goodbye.")
exit(0)
