import re
c=0
index=0
fo = open("test_1.txt","r+")
lst=fo.readlines()
fo.close()
while(index<len(lst)):
	if re.search(r"^create",lst[index].strip(),re.I) and re.search(r" table",lst[index].strip(),re.I) or re.search(r"(hash index|join index)",lst[index].strip()) :
		if "table" in lst[index].lower():
			a,b=lst[index].lower().split("table",1)
			if ',' in a:
				print '@@@@',lst[index]
				pass
			else:
				c+=1
				print '%%%%',lst[index]
				print 'aaaa',lst[index]
				print 'aaa',c
		else:
			c+=1
			print 'aaaa',lst[index]
	elif re.search(r"^create",lst[index].strip(),re.I) and re.search(r";$",lst[index].strip(),re.I):
		index+=1
		continue
	elif re.search(r"^create",lst[index].strip(),re.I):
		index+=1
		while((index<len(lst)) and ';' not in lst[index].strip()):
			if re.search(r"table",lst[index].strip(),re.I) or re.search(r"(hash index|join index)",lst[index].strip()):
				if "table" in lst[index].lower():
					a,b=lst[index].lower().split("table",1)
					if ',' in a or ',' in lst[index-1]:
						pass
					else:
						c+=1
						print 'bbbb',lst[index]
						print c
						index+=1
						break
				else:
					c+=1
					print 'bbb',lst[index]
					index+=1
					break
			index+=1
		if re.search(r"table",lst[index].strip(),re.I) or re.search(r"(hash index|join index)",lst[index].strip()):
			if "table" in lst[index].lower():
				a,b=lst[index].lower().split("table",1)
				if ',' in a or ',' in lst[index-1]:
					pass
				else:
					c+=1
					print  'cccc',lst[index]
					print 'cccc',c
			else:
				c+=1
				print 'cccc',lst[index]
	else :
		if re.search(r"/bct/b",lst[index].strip(),re.I):
			c+=1
			print 'dddd',lst[index]
			print 'dddd',c
	index+=1
print c
			
			
				