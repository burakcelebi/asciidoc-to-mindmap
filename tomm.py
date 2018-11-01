#!/usr/bin/env python

import re
import sys, getopt


class Node:
	def __init__(self, title, link):
		self.title = title
		self.link = link

def build_link(str):
	base_doc_link = "https://docs.hazelcast.org/docs/3.11/manual/html-single/index.html#"
	return base_doc_link + str.replace('\n', '').replace("[", "").replace("]", "").strip()

def to_nodes(file):
	array = []
	pattern = re.compile('=+ ')
	with open(file, "r") as ins:
		content = ins.readlines()
		i = 0
		for line in content:
			if pattern.match(line):
				array.append(Node(line, build_link(content[i-1])))
			i += 1
	return array

def level_diff(node1, node2):
	return node2.title.count('=') - node1.title.count('=')

def trim_title(node):
	return node.title.replace('=', '').replace("\'", "").replace("\"", "").strip()

def generate_position_str(arr, i):
	if (arr[i].title.count('=')==2):
		pos = 'left' 
		if i>len(arr)/2:
			pos = 'right'
		return "POSITION='" + pos + "' "
	else:
		return ""

def generate_style_str(arr, i):
	return " LOCALIZED_STYLE_REF=\"styles.topic\""

def generate_link_str(arr, i):
	return " LINK=\"" + arr[i].link + "\""

def to_nodes_xml(arr):
	nodes = [] 
	for i in range(len(arr)):
		if (i != len(arr)-1):
			level_change = level_diff(arr[i], arr[i+1])
			
			position = generate_position_str(arr, i)
			style = generate_style_str(arr, i)
			link = generate_link_str(arr, i)

			trimmed_title = trim_title(arr[i])

			if (level_change == 0):
				nodes.append("<node " + position + style + link + " FOLDED=\"true\" TEXT='" + trimmed_title + "'/>")
			elif (level_change > 0):
				nodes.append("<node " + position + style + link + " FOLDED=\"true\" TEXT='" + trimmed_title + "'>")
			else:
				nodes.append("<node " + position + style + link + " FOLDED=\"true\" TEXT='" + trimmed_title + "'/>")
				nodes.append("</node>" * (level_change*-1) ) 

	return nodes


def create_mm(outputfile, array):
	with open(outputfile, 'w') as f:
		f.write("<map version=\"freeplane 1.6.0]\">")
		f.write("<node TEXT=\"Hazelcast\" LOCALIZED_STYLE_REF=\"AutomaticLayout.level.root\">")
		for item in array:
			f.write("%s\n" % item)
		f.write("</node>")
		f.write("</map>")


def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'tomm.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'tomm.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

   	nodes = to_nodes(inputfile)
	nodes_XML = to_nodes_xml(nodes)
	create_mm(outputfile, nodes_XML)

if __name__ == "__main__":
   main(sys.argv[1:])
