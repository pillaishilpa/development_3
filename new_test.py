import re
import itertools
fo=open("test_1.txt","r+")
lst=fo.readlines()
index=0

subindex=0
fnl_lst=[]
while(index<len(lst)):
	subindex=0
	qrylst=[]
	qrylst2=[]
	flg=0
	flag=0
	if re.search(r"create.*table",lst[index],re.I) or re.search(r"ct",lst[index]):
		flg=1
		while(';' not in lst[index]):
			qrylst.append(lst[index])
			index+=1
		qrylst.append(lst[index])
	if flg==1:
		str='\n'.join(qrylst)
		mo=re.search(r"(,.*map.*=)",str)
		if mo:
			a,b=str.split(mo.group(0))
			print 'aaa',a
			print 'bbbb',b
			m1=re.search("(^.*)",b)
			if '(' in m1.group(0):
				flag=1
			c,d=b.split(m1.group(0))
			print 'cccc',c
			print 'dddd',d
			if flag==1:
				str=a+'('+d
			else:
				str=a+d
			fnl_lst.append(str)
				
	else:
		fnl_lst.append(lst[index])
	index+=1
fo=open('test_2.txt',"w+")
for lines in fnl_lst:
	fo.write(lines)
fo.close()