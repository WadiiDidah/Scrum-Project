import sys
import re
import os

def outputFile():
	global type_file
	global file
	global title
	global abstract
	if(type_file == "-t"):
		fi_out=open('output.txt','r+')
		fi_out.truncate()
		fi_out.write("Name File: "+file+"\n")
		fi_out.write("Title: "+title+"\n")
		fi_out.write("Auteur: "+auteurs+"\n")
		fi_out.write("Abstract: "+abstract+"\n")
	else:
		fi_out=open('output.xml','r+')
		fi_out.truncate()
		fi_out.write("<article>\n\t<preamble>"+file+"</preamble>\n")
		fi_out.write("\t<title>"+title+"</title>\n")
		fi_out.write("\t<auteur>"+auteur+"</auteur>\n")
		fi_out.write("\t<abstract>"+abstract+"</abstract>\n")
		fi_out.write("</article>")
		return 0

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
	global	title_end_line

	executePdf2Txt()
	file1 = open('temp.xml', 'r')
	Lines = file1.readlines()

	index_max = 0
	global title    
	espace_b = 1
	full_size = 0.0
	for line in Lines:
		index_max = 1 + index_max
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
				title_end_line = index_max
			espace_b = 0
		except:
			if espace_b == 0:
				espace_b = 1
				title = title + " "

def getAbstract():
	global abstract
	global file
	os.system("pdf2txt "+file+" -o temp.txt -A -V")
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
	abstract = abstract.replace("Abstract","")
	abstract = abstract.replace("ABSTRACT","")
	abstract = abstract.replace("\n","")

def getAuteurs():
	global	title_end_line
	global	auteurs
	file1 = open('temp.xml', 'r')
	Lines = file1.readlines()
	i = 0
	font_typed = False
	font_style = ""
	auteurs_t = []
	auteur_t = ""
	next_aut = False
	# pour chaque lignes du fichier dans un interval 
	for line in Lines:
		i += 1
		# si on est dans l'interval
		if(i > title_end_line):
			# on recup le style des auteurs 
			if(font_typed == False):
				try:
					font_style = re.search('^<text font="(.)+">',line).group(0)
					font_style = re.sub('bbox=(.)+colours', '', font_style)
					font_typed = True
				except:
					print("searching auteur")
			else:
				# si on l'a deja, prendre tous le text avec exactement le meme style d'ecriture
				try:
					inline = re.search('^<text font="(.)+">',line).group(0)
					inline = re.sub('bbox=(.)+colours', '', inline)
					if(font_style == inline):
						m_auteur = re.search('">(.)+</text',line)
						m_auteur = m_auteur.group(0).replace('">',"").replace('</text',"")
						auteur_t = auteur_t + m_auteur
						next_aut = False
					elif next_aut == True:
						auteurs_t.append(auteur_t)
						auteur_t = ""
						next_aut = False
				except:
					print("searching font")
		if(i > (title_end_line+300)):
			auteurs_t.append(auteur_t)
			break
	for aut in auteurs_t:
		auteurs += aut+", "

file = ""
abstract = ""
title = ""
type_file = ""
title_end_line = 0
auteurs = ""

getName()   

try:
	type_file = sys.argv[2]
	if((type_file != "-t") and (type_file != "-x")):
		raise
	parseTitle()
	getAbstract()
	getAuteurs()
	outputFile()

except:
	print("err")
