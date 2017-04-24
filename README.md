# MSW-WordFreqCheck
WHAT IT IS:
- A simple tool for checking the frequency of words in a file.  Writers can use this as an intermediate check for word choice.
- The true virtue of this program is to catch silly word choice mistakes, such as using a noun twice in one sentence, or showing that one needs to find a thesaurus for recurring words.
- NOTE:  This program requires python-docx to be installed as well.  Without it, only *.txt files can be read, and only ASCII text can be interpreted.

HOW IT WORKS:
- After combing the entire file (specified by the user), words are scored based on three criteria: frequency in the same sentence, frequency in the same paragraph, and the frequency with which they occur in the file (ie the total number of occurences).
- After scoring the file, the user will have to perform a find/replace back in the editor being used to write the file to find the higher words on the list and choose how/whether to change occurences of the word to lower the frequency score.

ABOUT USE:
- At the moment, this is a very dumb tool (I cannot stress this enough): It lacks the ability to score the root words (ex. "grass" and "grassy" are considered two different words) and instead only scores the literal words. Human interpretation is essential to get anything out of this, and this program can never replace manually reading a document yourself. 
- THIS IS NOT INTENDED TO BE A TOOL TO "FINAL CHECK" A DOCUMENT! It is a tool to expedite intermediate editing of a document).
