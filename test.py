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
	indexlst=[]
	if re.search(r"create.*table",lst[index],re.I) or re.search(r"ct",lst[index]):
		while(';' not in lst[index]):
			indexlst.append(index)
			qrylst=lst[index].split()
			for val in qrylst:
				qrylst2.append(val)
			index+=1
		qrylst=lst[index].split()
		for val in qrylst:
			qrylst2.append(val)
		while(subindex<len(qrylst2)):
			if re.search(r"[,]?.*map.*[=]?",qrylst2[subindex]):
				flg=1
				break
			subindex+=1
		if flg==1:
			if ',' in qrylst2[subindex] and '=' in qrylst2[subindex]:
				if re.search("^,",qrylst2[subindex]) and re.search("=$",qrylst2[subindex]):
					del qrylst2[subindex]
					if '(' not in qrylst2[subindex]:
						del qrylst2[subindex]
					else:
						a,b=qrylst2[subindex].split('(',1)
						qrylst2[subindex]='('+b	
				elif re.search(r"^,",qrylst2[subindex]):
					if '(' not in qrylst2[subindex]:
						del qrylst2[subindex]
					else:
						a,b=qrylst2[subindex].split('(',1)
						qrylst2[subindex]='('+b
				elif re.search(r"=$",qrylst2[subindex]):
					a,b=qrylst2[subindex].split(",map=")
					qrylst2[subindex]=a
					if '(' not in qrylst2[subindex+1]:
						del qrylst2[subindex+1]
					else:
						a,b=qrylst2[subindex+1].split('(',1)
						qrylst2[subindex+1]='('+b	
				else:
					a,b=qrylst2[subindex].split(',map=',1)
					if '(' not in b:
						qrylst2[subindex]=a
					else:
						c,d=b.split('(',1)
						qrylst2[subindex]=a+'('+d
			elif ',' in qrylst2[subindex]:
				if re.search(r"^,",qrylst2[subindex]):
					del qrylst2[subindex]
					if qrylst2[subindex]== "=":
						del qrylst2[subindex]
						if '(' not in qrylst2[subindex]:
							del qrylst2[subindex]
						else:
							a,b=qrylst2[subindex].split('(',1)
							qrylst2[subindex]='('+b
					else:
						if '(' not in qrylst2[subindex]:
							del qrylst2[subindex]
						else:
							a,b=qrylst2[subindex].split('(',1)
							qrylst2[subindex]='('+b
				else:
					a,b=qrylst2[subindex].split(",map")
					qrylst2[subindex]=a
				if qrylst2[subindex+1]== "=":
					del qrylst2[subindex+1]
					if '(' not in qrylst2[subindex+1]:
						del qrylst2[subindex+1]
					else:
						a,b=qrylst2[subindex+1].split('(',1)
						qrylst2[subindex+1]='('+b
				else:
					if '(' not in qrylst2[subindex+1]:
						del qrylst2[subindex+1]
					else:
						a,b=qrylst2[subindex+1].split('(',1)
						qrylst2[subindex+1]='('+b
			elif '=' in qrylst2[subindex]:
				if re.search("=$",qrylst2[subindex]):
					del qrylst2[subindex]
					if '(' not in qrylst2[subindex]:
						del qrylst2[subindex]
					else:
						a,b=qrylst2[subindex].split('(',1)
						qrylst2[subindex]='('+b
				else:
					if '(' not in qrylst2[subindex]:
						del qrylst2[subindex]
					else:
						a,b=qrylst2[subindex].split('(',1)
						qrylst2[subindex]='('+b
				if re.search(r",$",qrylst2[subindex-1]):
					str=qrylst2[subindex-1].rstrip(',')
					qrylst2[subindex-1]=str
			else:
				del qrylst2[subindex]
				if qrylst2[subindex]=='=':
					del qrylst2[subindex]
					if '(' not in qrylst2[subindex]:
						del qrylst2[subindex]
					else:
						a,b=qrylst2[subindex].split('(',1)
						qrylst2[subindex]='('+b
				elif '(' not in qrylst2[subindex]:
					del qrylst2[subindex]
				else:
					a,b=qrylst2[subindex].split('(',1)
					qrylst2[subindex]='('+b
				if re.search(r",$",qrylst2[subindex-1]):
					str=qrylst2[subindex-1].rstrip(',')
					qrylst2[subindex-1]=str
		qry=' '.join(qrylst2)
		qry=qry+"\n"
		fnl_lst.append(qry)
		#index+=1
	else:
		fnl_lst.append(lst[index])
	index+=1
fo=open("test_2.bteq","w+")
for val in fnl_lst:
	fo.write(val)
fo.close()