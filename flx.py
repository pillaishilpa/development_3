import xml.etree.ElementTree as E
import urllib2
file=urllib2.urlopen('https://teradata.slack.com/messages/G6LJ21H7S/')
data=file.read()
file.close()
print data
"""tree=E.parse(file)
root=tree.getroot()
fo=open('text',"w+")
i=0
for child in root:
	j=0
	#print "\n",child.tag,child.attrib
	fo.write("\n")
	fo.write(child.tag)
	fo.write(child.attrib)
	for subchild in child:
		fo.write(subchild.tag)
		fo.write(subchild.attrib)	
		#print subchild.tag,subchild.attrib
		#print root[i][j].text
		j+=1
	i+=1"""
	