import sys
import re
import os

def executePdf2Txt():
    print("pdf2txt "+file+" -o temp.xml")
    os.system("pdf2txt "+file+" -o temp.xml")

def getName():
    try:
        name_file = sys.argv[1]
        global file
        file = name_file
    except :
        print("Veuillez preciser le PDF")

def parseTitle():
    executePdf2Txt()
    file1 = open('temp.xml', 'r')
    Lines = file1.readlines()
    
    index_max = 0
    title = ""
    espace_b = 1
    full_size = 0.0
    # Strips the newline character
    for line in Lines:
        index_max += 1
        if(index_max == 400):
            break
        m_size = re.search('size="(.)+\.([0-9])+',line)
        try:
            mot = m_size.group(0).replace('size="',"")
            m_text = re.search('">(.)+</text',line)
            m_text = m_text.group(0).replace('">',"").replace('</text',"")
            if(float(full_size)<float(mot)):
                title = m_text
                full_size = float(mot)
            elif(full_size==float(mot)):
                title = title + m_text
            espace_b = 0
        except:
            if espace_b == 0:
                espace_b = 1
                title = title + " "
    print(title)

def getAbstract():
	os.system("pdf2txt"+file+"-o temp.txt -A -V")
	fi =open('temp.txt','r')
	lignes=fi.readlines()
	fi.close()
	debut=0
	abstract =""
	for ligne in lignes:
		if ("Abstract" in ligne or "ABSTRACT" in ligne ):
			debut=1
		if ("I." in ligne or "Introduction" in ligne or "INTRODUCTION" in ligne ):
			debut=0
			break
		if (debut==1):
			abstract=abstract+ligne
	print(abstract)


file = ""
getName()

try:
    parseTitle()
except:
    print("err")
