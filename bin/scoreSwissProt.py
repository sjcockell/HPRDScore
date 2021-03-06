#!/usr/bin/env python

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import re
import sys

class proteinInfo:
	protein = {}
	def __init__(self, array):
		protein = {}
		headers = ['HPRD_ID', 'UNIPROT_ID', 'GO_IDS']
		for i in range(0,3):
			try:
				protein[headers[i]] = array[i]
			except IndexError:
				protein[headers[i]] = None
		self.protein = protein
	
	def getProtein(self):
		return self.protein

def main():
	proteinDictionary = {}
	proteinFile = sys.argv[1]
	interactionFile = sys.argv[2]
	pf = open(proteinFile, 'r')
	plines = pf.readlines()
	for line in plines:
		tokens = line.rstrip().split('\t')
		p = proteinInfo(tokens)
		proteinDictionary[tokens[0]] = p.getProtein()
	intf = open(interactionFile, 'r')
	ilines = intf.readlines()
	for line in ilines:
		ids = line.rstrip().split('\t')
		try:
			SP1 = proteinDictionary[ids[0]]['UNIPROT_ID']
			SP2 = proteinDictionary[ids[1]]['UNIPROT_ID']
		except KeyError:
			SP1 = None
			SP2 = None
		if SP1 == '':
			SP1 = None
		if SP2 == '':
			SP2 = None
		if SP1 != None and SP2 != None:
			try:
				go_list1 = proteinDictionary[ids[0]]['GO_IDS']
				go_list2 = proteinDictionary[ids[1]]['GO_IDS']
			except KeyError:
				go_list1 = None
				go_list2 = None
			if go_list1 != None and go_list2 != None:
				go1 = open("GO1", 'w')
				go2 = open("GO2", 'w')
				go_list1 = formatGOList(go_list1)
				go_list2 = formatGOList(go_list2)
				for go in go_list1:
					go1.write(go+'\n')
				for go in go_list2:
					go2.write(go+'\n')
				go1.close()
				go2.close()
				print SP1+'\t'+SP2+'\t'+parseHtml(gSesameCall())
			else:
				print SP1+'\t'+SP2+'\t'+'None'


def formatGOList(list):
	go_list = []
	p = re.compile('GO:(\d{7}),')
	matches = p.findall(list)
	for m in matches:
		go_list.append(m)
	return go_list

def gSesameCall():
	register_openers()
	datagen, headers = multipart_encode({"uploadedfile1": open("GO1"),
										"uploadedfile2": open("GO2"),
										"isA": "0.8",
										"partOf": "0.6",
										})
	request = urllib2.Request("http://bioinformatics.clemson.edu/G-SESAME/Program/GOCompareMultiple2.php", datagen, headers)
	return urllib2.urlopen(request).read()

def parseHtml(content):
	p = re.compile('Semantic similarity of two GO term sets is: <div class="emphasis2">(\d.\d+)')
	score = p.findall(content)
	try:
		s = score[0]
	except IndexError:
		return 0
	else:
		return s

if __name__ == '__main__':
	main()


