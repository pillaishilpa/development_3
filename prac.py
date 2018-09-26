import re
str1='shilpa'
str2='abcshhilpaaxyz'
for ch in str1:
	if str2.count(ch)>=str1.count(ch):
		print 'ok'
	else:
		print 'not ok'