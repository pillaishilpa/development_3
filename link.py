import re
import requests
fo=open('file',"w+")
info={'inUserName':"shilpapillai920815@gmail.com",'inUserPass':"@paru123"}
"""with requests.Session() as s:
	p=s.post('https://www.linkedin.com/uas/login',data=info)
	fo.write(p.text.encode('utf-8'))"""
fo=open('jira_file',"w+")
info={'inUserName':"sp186090",'inUserPass':"mssrrP15@"}
with requests.Session() as s:
	p=s.post('https://jira.td.teradata.com/jira/login.jsp',data=info)
	fo.write(p.text.encode('utf-8'))
	