#!/usr/bin/env python


##
## This runs over the XML dump files of HPRD
##

import sys
import os
import xml.etree.cElementTree as ET

def main():

	directory = sys.argv[1]

	filelist = os.listdir(directory)
	count = 0
	protein_list = []

	for file in filelist:
		protein = HPRDProtein()
		protein_list.append(protein)
				
		if file.split(".")[1] == "xml":

			if count > 10:
				break
				   
			count += 1
			print(file)
			for events in ET.iterparse(directory + "/" + file):

				## get element
				element = events[1]

				## look for protein events, so we can capture the ID
				## we only need the name, not the namespace.
				if name_only(element) == "protein":
					id = element.get("id")
					if id != None:
						protein.set_hprd_id(id.split("_")[1])


				if name_only(element) == "SwissProt":
					protein.set_swissprot_id(element.text)

				if name_only(element) == "cellular_component":
					for c_elem in element.getchildren():
						for c_c_element in c_elem.getchildren():
							if name_only(c_c_element) == "go_id":
								protein.add_go_id(c_c_element.text)
								

				if name_only(element) == "interactorRef":
					protein.add_interactor(element.text)

				#if name_only(element) == 'interactorList':
				#	children = element.getchildren()
				#	for child in children:
				#		if name_only(child) == 'interactor':
				#			print child.attrib.get('id')
				if name_only(element) == 'interactionList':
					interactions = element.getiterator('{net:sf:psidev:mi}interaction')
					for interaction in interactions:
						participants = interaction.find('{net:sf:psidev:mi}participantList').getiterator('{net:sf:psidev:mi}participant')
						participant_ids = []
						for participant in participants:
							ref = participant.find('{net:sf:psidev:mi}interactorRef').text
							participant_ids.append(ref)
						x = 0
						for pid in participant_ids:
							if pid == protein.get_hprd_id():
								x += 1
						print hprd_id()
						if x > 1:
							print 'Self Interactor'
	
	
	out1 = open('out/hprd_interactions', 'w')
	out2 = open('out/hprd_proteins', 'w')
	for i in protein_list:
		if i.get_hprd_id() != None:
			#print i.get_hprd_id() + '\t',
			out2.write(i.get_hprd_id() + '\t')
		else:
			out2.write('\t')
		if i.get_swissprot_id() != None:
			#print i.get_swissprot_id() + '\t',
			out2.write(i.get_swissprot_id() + '\t')
		else:
			out2.write('\t')
		for go_id in i.get_go_id():
			#print go_id + ',',
			out2.write(go_id + ',')
		#print
		out2.write('\n')
		for interactor in i.get_interactors():
			#print i.get_hprd_id() + '\t' + interactor
			out1.write(i.get_hprd_id() + '\t' + interactor + '\n')
		#print( i.get_hprd_id() )
		#print( i.get_swissprot_id() )
		#print( i.get_interactors() )
		#print( i.get_go_id() )
	out1.close()
	out2.close()


def name_only(element):
	return element.tag.split("}")[1]


class HPRDProtein:
	def __init__(self):
		self.interactors_id = []
		self.go_ids = []
		self.swissprotid = None
		self.hprd = None
				

	def get_hprd_id(self):
		return self.hprd

	## not including the underscore!
	def set_hprd_id(self, id):
		self.hprd = id

	def get_swissprot_id(self):
		return self.swissprotid

	def set_swissprot_id(self, id):
		self.swissprotid = id
				
	def get_go_id(self):
		return self.go_ids

	def add_go_id(self, id):
		self.go_ids.append(id)

	def get_interactors(self):
		#if self.get_hprd_id() in self.interactors_id:
		#	self.interactors_id.remove(self.get_hprd_id())
		return self.interactors_id

	def add_interactor(self, id):
		if id not in self.interactors_id:
			self.interactors_id.append(id)
		
		





		
if __name__ == '__main__':
	main()




