import os
import math
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
import sys
data_4 = {}
flag = 0
#accessing the directory 4/5/6 and getting all the xml documents in the folder. Parse all the documents in the  folder and get
# the abstracts/background from it.
#split each abstract and remove any stop words from the words in each file.
for filename in os.listdir("4"):
	flag = flag+1
	file = str(filename)
	varibale = '4/'+file
	f =open(varibale,'r',encoding="utf8")
	content = f.read()
	tree = ET.parse(varibale)
	root = tree.getroot()
	if root.findall('Doc_abstract'):
		data_4[os.path.splitext(filename)[0]] =(root.find('Doc_abstract').text).lower()
	elif root.findall('Background'):
		data_4[os.path.splitext(filename)[0]] =(root.find('Background').text).lower()
data_4_split = {}
for i in data_4:
	data_4_split[i] = [word for word in data_4[i].split() if word not in (stopwords.words('english'))]
dictionary_words = {}
#create a dictionary of all unique words and their count in all the documents in the folder.
for i in data_4_split:
	for j in data_4_split[i]:
		if j in dictionary_words:
			v = dictionary_words[j]
			v = v+1
			dictionary_words[j] = v
		else:
			dictionary_words[j] = 1
###query preperation###########################################
##query preparation is accessing the query file 4.xml/5/xml/... and then getting all the data in the tags and removing the stopwords
# from it and then getting a list of query terms from it.
query_input = ET.parse('4.xml')
query_root = query_input.getroot()
query_terms = []
qt = [word for word in ((query_root.find('disease').text).lower()).split() if word not in (stopwords.words('english'))]
for j in qt:
	query_terms.append(j)
qt = [word for word in ((query_root.find('other').text).lower()).split() if word not in (stopwords.words('english'))]
for j in qt:
	query_terms.append(j)
qt = [word for word in ((query_root.find('demographic').text).lower()).split() if word not in (stopwords.words('english'))]
for j in qt:
	query_terms.append(j)
qt = [word for word in ((query_root.find('gene').text).lower()).split() if word not in (stopwords.words('english'))]
for j in qt:
	query_terms.append(j)
print("\nThe query terms are...\n")
print(query_terms)
#########################################################
##tf
# here we calculate the term frequency of each query word by counting the number of occurences in the file to the total number of words in the file
# by this we get the importance of a word in the document.
tf_dictionary_words ={}
for i in dictionary_words:
	tf_dictionary_words[i] = math.log10(flag/dictionary_words[i])
##idf
#########################################################
#building idf
#number of docs with term in it.	
#here we calcluate the inversse docment frequency by normalizing the documents with the terms 
#to get the idf we count the total number of documents in the folder and then count the number of documents with the 
#query terms this makes the important documents with a good score.
doc_with_terms_count = {}
for i in query_terms:
	count = 0
	for j in data_4_split:
		if i in data_4_split[j]:
			count = count + 1
	doc_with_terms_count[i] = count
idf_query_terms = {}
for i in query_terms:
	if doc_with_terms_count[i] > 0:
		idf_query_terms[i] = math.log10(flag/doc_with_terms_count[i])
	else:
		idf_query_terms[i] = 0
#print(doc_with_terms_count)
#print(idf_query_terms)


######calculating the tf and also the score for each word
#calculating the score for each document for each of the query terms and adding them gives us a final score for each document.
#we multiply the idf and tf for each term and get the score for the term in that document.
#now we have a dictionary of the scores and the document names. we arrange them accoriding to the 
#score values and we take the documents only over a particular threshold value let say 0.01 or 0.5 etc.
#this threshold value is used to get the relevant documents for the given query terms.

#improvemnts
#can try with more bigrams and trigrams to get more accuracy and normalize the query terms occurence with 1 to speed up the process.
#
count = {}

score = {}
tf = {}
for i in data_4_split:
	score[i] = 0
	for j in query_terms:
		count[j] = 0
		for k in data_4_split[i]:
			if k == j:
				count[j] = count[j] + 1
		tf[j] = count[j]/len(data_4_split[i])
		score[i] =  score[i] + (tf[j]*idf_query_terms[j])
	#print(count)
#print(score)
#print(len(score))
score_sorted = sorted(score, key=score.get, reverse=True)
rank = 0
print('\nPrinting all the relevant documents list into file titled as 4out.txt')
f=open("4out.txt", 'w')
sys.stdout = f
print("\nPrinting Top 50 relevant documents.....\n")
print("**************************************************************************")
print("[question ID]     Q0    [rank]  [Document ID] \t [score] \t     [group ID]")
print("**************************************************************************")
for r in score_sorted:
	if score[r] > 0.00912:
		rank = rank + 1
		print("1\t ","\t  Q0\t ", rank,'\t{:>10}\t{:5}\t{:5}\t'.format(r,score[r],"Group-2"))
print("\nPrinting all relevant documents.....\n")
print("**************************************************************************")
print("[question ID]     Q0    [rank]  [Document ID] \t [score] \t     [group ID]")
print("**************************************************************************")
rank = 0
for r in score_sorted:
	if score[r] > 0:
		rank = rank + 1
		print("1\t ","\t  Q0\t ", rank,'\t{:>10}\t{:5}\t{:5}\t'.format(r,score[r],"Group-2"))
f.close()
		