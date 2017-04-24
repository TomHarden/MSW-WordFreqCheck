############################################################
####################    IMPORTS         ####################
############################################################
import os#necessary to get the directory of the file in question (and the directory of this program).

############################################################
####################    FUNCTIONS       ####################
############################################################
#prompts the user for a file name and extension.  It recursively calls itself until a valid iinput is recieved, so at the risk of readability, there is a slight performance loss.
#   Once a valid file is input, the parent directory, name, and extension are returned as a tuplefrom docx import Document # necessary
#@return (String, String, String) returns a tuple of three strings, the parent directory, the file name, and the file extension.
def getFileAttributes():
    filePath = os.path.dirname(os.path.realpath(__file__))
    fullFileName = input("Enter the name and extension of the file (ex. \"Some File.docx\").\nIMPORTANT:  It must be in the same directory as this program!:\n\n    >>>" + filePath + "\\")
    fileName, fileExtension = "", ""
    beforeExtension = True
    if (fullFileName.count(".") != 1):
        print("ERROR, PROBLEM WITH FILE EXTENSION (check period (\".\") !).\n\n\n")
        return getFileAttributes()#"loop" through recursion

    #get the file name and extention from the user input chracter by character
    for char in fullFileName:
        if char != "." and beforeExtension:
            fileName += char
        else:#build the file extension
            beforeExtension = False
            fileExtension += char

    #check that user input is valid
    if fileExists(filePath, fileName, fileExtension) == False:
        print("ERROR, \"" + fullFileName + "\" COULD NOT BE FOUND IN DIRECTORY" + filePath + "\n\n\n")
        return getFileAttributes()#"loop" through recursion
    return (filePath, fileName, fileExtension)

#checks if a specified file exists.  Returns true if the file is found, and false if the file is not
#@param String filePath is the parent directory of the file
#@param String fileName is the name of the file (does not include the parent directory or extension!
#@param String fileExtension is the extension of the file (ex. ".txt")
#@return bool return true if the file if found (ie exists), and false otherwise.
def fileExists(filePath, fileName, fileExtension, action = 'r'):
    try:
        f = open(filePath + "\\" + fileName + fileExtension, action)
        f.close()
        return True;
    except:
        try:
            doc = Document(open(filePath + "\\" + fileName + fileExtension, action + 'b'))
            doc.close()
            return True
        except FileNotFoundError:
            return False
        return False
    return True

#Appends a line to a specified file (assumed in working directory), and also adds additional functionality for the addiion.  It is assumed, however, that the appending is standard
#@String s is the string representing the text to be added to the file
#@String fileName is the name of the dile to which the text will be appended.  It is assumed to be in the working directory.
#@bool allowDuplicates is a boolean value which is true by default.  If specified to false, the string being added must be an original line in the file or else it will not be added
#@bool alphabetizeFile is a boolean value which is false by default.  If specified to be true, the entire file will be alphabetized by line.  the current file will then be overwritten with the newly alphabetized version.
#@return void
def addNewLine(s, fileName, allowDuplicates = True, alphabetizeFile = False):#return none;  appends string s to a new line in file fileName and then rewrites the file so it is in alpabetical order.  CURRENTLY NOT EFFIECIENT FOR LARGE FILE SIZES.  Assumes that s is a verified string.
    if isKnown(s, fileName):#checks if the element to be added is already in the file.  Also checks that there is a file to add to!  (if not, creates the file!)
        if allowDuplicates == False:#from encasing (previous) if statement, know that there is a dupliate in there! So no need to add, just return!
            return#no need to add anthing
        f = open(fileName, 'a')#append this file
        f.write(s + "\n")#add the element to the file before sorting it.
        f.close()
    else: #file (or string in that file) does not exist!  no need to D2!
        f = open(fileName, 'a')#append this file
        f.write(s + "\n")#add the element to the file before sorting it.
        print("Appended " + s + " to " + fileName)
        f.close()
    if alphabetizeFile == True:
        #need to enter the name so it is in alphabetical order!
        f = open(fileName, 'rb')
        tmpList = []
        for line in sorted(f):
            tmpList.append(line)
            print("#####" + line)
        f.close()
        f = open(fileName, 'w')
        for element in tmpList:
            f.write(element)
        f.close()

#safely creates a file of the specified name (assumed to be in the working directory!)
#@String fileName is the name of the file to be created.  It will be created by in the current working directory
#@return void
def createFile(fileName):
    f = open(fileName, 'a')
    f.close

#returns all the text of a file as a single string.
#@String directory is the parent directory of the file specified in fileName
#@return void
def fileToString(directory, fileName, extension):
    #######################
    ### LOCAL FUNCTIONS ###
    #######################
    def isAscii(s):
        try:
            s.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    ###########################
    ###        MAIN         ###
    ###########################
    eraseTmpFile = False
    TMP_FILENAME = directory + "tmpFile" + '.txt'
    if (extension == ".txt"):
        f = open(directory + "\\" + fileName + extension, 'r')
    elif (extension == ".docx"):
        print ("\n Looking for the following doc: (" + directory + "\\) " + fileName + extension + "\n")
        doc = Document(open(directory + "\\" + fileName + extension, 'rb'))
        createFile(TMP_FILENAME)
        eraseTmpFile = True
        tmpf = open(TMP_FILENAME, 'a')
        for para in doc.paragraphs:
            try:
                tmpf.write(para.text)
            except UnicodeEncodeError:
                tmpf.write(" ")
            tmpf.write("\n")#turn string to txt file
        tmpf.close()
        f = open(TMP_FILENAME, 'r')
    s = "";
    for line in f:
        for char in line:
            if (isAscii(str(char))):
                s += str(char)
            else:
                s+= " "
    f.close()
    if (eraseTmpFile):
        os.remove(TMP_FILENAME)
    return s

############################################################
####################    PROGRAM MAIN    ####################
############################################################
