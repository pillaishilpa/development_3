import io
import datetime
import paramiko
import os
from jira import JIRA
import csv
import re
import getpass



def getMeLastRunTime():
    with open('lastRunTime.txt','r') as f:
        lastRunTime = f.read()
        return lastRunTime

def setLastRunTime(scriptStartTime):
    with open('lastRunTime.txt','w') as f:
        f.write(str(scriptStartTime))

def getSerialNumber(description):
    serialNumber = re.findall(r'(ttc.td.teradata.com/PTE/cases.cfm\?Serial_Number=|/PTE/DWA/\?SerialNumber=|ttc.td.teradata.com/pte/dwa/index.cfm\?ShowContentsOnly=true\&SerialNumber=|ttc.td.teradata.com/PTE/DWA/index.cfm\?SerialNumber=)([0-9]*).*',description,re.IGNORECASE)
    serialNumberList = list(set([x[1] for x in serialNumber]))
    if len(serialNumberList)>0:
        return serialNumberList
    else:
        return 0

def getJiraAttributes(jiraContent):    
    testCaseName = (str(jiraContent.fields.customfield_10517)+'').strip()
    testCaseNames = re.split('\r\n|,|\r|\n',testCaseName);
    allTestCaseNames =''
    for name in testCaseNames:
        testCase = name.split('.')
        allTestCaseNames = allTestCaseNames+(str(testCase[0])+'').strip()+','
    #have to deal with case where we have multiple testcases
    #have to deal with case where the file names are having extension or plain '.' at end
    testSuiteName = (str(jiraContent.fields.customfield_10510)+'').strip()
    testSuiteNames = re.split('\r\n|,|\r|\n',testSuiteName);
    allTestSuiteNames =''
    for suiteName in testSuiteNames:
        testSuiteName =name.split('.')
        allTestSuiteNames = allTestSuiteNames+(str(testSuiteName[0])+'').strip()+','
    jiraStatus = (str(jiraContent.fields.status)).strip()
    if unicode((jiraContent.fields.resolution)).endswith("Deliver/Implement/Fix"):
        jiraResolution = "Wont Deliver Implement Fix:"
    else:
        jiraResolution = str(jiraContent.fields.resolution)
    jiraFoundInBuild = (str(jiraContent.fields.customfield_10513)).strip()
    return [allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild]

def buildDictJira(fileName):
    fullNameList = list(csv.reader(open(fileName,'rb'),delimiter = '$'));
    jiraDict = {jiraNumber.strip():testSuite.strip() for jiraNumber, testSuite,testCase,status,resolution,foundin in fullNameList}
    testSuiteDict = {testSuite.strip():testCase.strip() for jiraNumber,testSuite,testCase,status,resolution,foundin in fullNameList}
    jiraStatusDict = {jiraNumber.strip():status.strip() for jiraNumber, testSuite,testCase,status,resolution,foundin in fullNameList}
    return jiraDict,testSuiteDict,jiraStatusDict

def copyDiffFiles(serialNumberList,allTestCaseNames,issueNumber,sftp,ssh):
    foundFolder=0
    for serialNumber in serialNumberList:
        issueNumber = str(issueNumber)
        sftp.chdir('/ptehome/pte_save/')
        print sftp.getcwd()
        #allFolders = sftp.listdir(path='.')
        command = "find /ptehome/pte_save -maxdepth 1 -name \""+"*"+str(serialNumber)+"*\" -type d"
        (stdin,stdout,stderr) = ssh.exec_command(command)
        allFolders = stdout
        testCaseNamesList = re.split(',',str(allTestCaseNames))
        programPath = os.getcwd()
        for folderName in allFolders:
            if str(serialNumber) in str(folderName):
                foundFolder = foundFolder+1
                print ("The folder with Seraial Number: "+ str(serialNumber)+ " exists")
                fullPath =str(folderName).strip()+'/tmpout'
                print ("Going to copy .dif file and .err file from "+ fullPath)
                sftp.chdir(fullPath)
                allPteFiles= sftp.listdir(path='.')
                print sftp.getcwd()
                targetPath = 'Jiras\\'+str(issueNumber)
                if os.path.isdir(targetPath):
                    pass
                else:
                    os.mkdir(targetPath)
                print targetPath
                for pteFileName in allPteFiles:
                    for testCaseName in testCaseNamesList:
                        if pteFileName.endswith('.dif') or pteFileName.endswith('.err'):
                            if (re.split('\.',pteFileName,)[0]).strip() == testCaseName.strip():
                                sftp.get(pteFileName,targetPath+'\\'+pteFileName)
                                print ("copied "+pteFileName+ " to "+ targetPath)
    if foundFolder ==0:
        print ("one of the  test suite having Serial Number in list : "+str(serialNumberList)+ " could not be found")
        print ("The folder could have been archived")
        print ("we are going to store this information in Jira//jiratcfiledb.txt Moving on to next Jira")
        return 0
    else:
        return 1
         

def updateFile(fileDicti,filepath,issue,testSuiteName,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild):
    if str(issue) not in fileDicti:
        with open(filepath,'a+') as f:
            f.write(unicode(str(issue)+'$'+str(testSuiteName)+'$'+str(allTestCaseNames)+'$'+str(jiraStatus)+'$'+str(jiraResolution)+'$'+str(jiraFoundInBuild)+'\n'))
    elif str(issue) in fileDicti:
        with open(filepath,'r') as f:
            allContent = f.readlines()
        for idx,contentline in enumerate(allContent):
            #print re.split('/$',contentline)[0]
            #print str(issue)
            #print re.split('\$',contentline)[0]
            if re.split('\$',contentline)[0] == str(issue):
                #print (str(issue) + " is existing ")
                allContent[idx] = unicode(str(issue)+'$'+str(testSuiteName)+'$'+str(allTestCaseNames)+'$'+str(jiraStatus)+'$'+str(jiraResolution)+'$'+str(jiraFoundInBuild)+'\n')

        
        with open(filepath,'w') as f:
            #print (allContent)
            f.writelines(allContent)
                
def getUpdatedJiras(lastRunTime,userName,passWord):
    jiraDict,testSuiteDict,jiraStatusDict = buildDictJira("Jiras\\jiratcfiledb.txt")
    njiraDict,ntestSuiteDict,njiraStatusDict = buildDictJira("Jiras\\jirawithoutdifffiles.txt")
    print "establishing Connection with Jira"
    try:
        jira = JIRA(server = 'https://jira.td.teradata.com/jira/',basic_auth=(userName,passWord))
    except Exception as e:
        print str(e)+"Error occured while connecting to JIRA , Check the username password and other details"
        sys.exit(0);
        
    issues = jira.search_issues('project = TDEEFIX AND component = "E-Fix triage" AND updated >='+str(lastRunTime),0,1000)
	#we can give our own JQL while testing the code.
    print "Jira Connection Establdished"
    print ("The following Jiras are updated after LastRuntime :"+ lastRunTime)
    for iss in issues: print iss
    
    print "connecting with ptesd"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('ptesd',username=userName,password=passWord)
    sftp = ssh.open_sftp()
    sftp.chdir('/ptehome/pte_save')
    #allfolders = sftp.listdir(path ='.')
    
    print "ptesd connected"
    for issue in issues:
		
        print ("\n Processing Jira : "+str(issue))
        jiraContent = jira.issue(issue)
        [allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild] = getJiraAttributes(jiraContent)
        if str(issue) not in jiraDict:
            print ("This "+str(issue)+" was not noted earlier")
            if(jiraContent.fields.description):                             
                serialNumberList = getSerialNumber(jiraContent.fields.description)
                if serialNumberList ==0:
                    print ("CAUTION: The program could not retrieve the Serial Number from the description")
                    print ("Still we are storing this information in jiratcfiledb.txt")
                    updateFile(jiraDict,"Jiras\\jiratcfiledb.txt",issue,allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild);
                    print ("Moving on to next Jira")
                    continue

                print ("the serail number acquired from this jira is "+str(serialNumberList))
                issueNumber= str(issue)
                rDiffCopied =copyDiffFiles(serialNumberList,allTestCaseNames,issueNumber,sftp,ssh)
                if rDiffCopied ==0:
                    updateFile(jiraDict,"Jiras\\jiratcfiledb.txt",issue,allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild);
                elif rDiffCopied ==1:
                    updateFile(jiraDict,"Jiras\\jiratcfiledb.txt",issue,allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild);
                    #updateFile(jiraDict,"Jiras\\jiratcfiledb.txt",issue,allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild);
            else:print "There is no description available for this Jira"
                        
        elif str(issue) in jiraDict:
            print ("We found this Jira in existing files and updating the same")
            print ("Checking for any new serail Number")
            if(jiraContent.fields.description):
                serialNumberList = getSerialNumber(jiraContent.fields.description)
                if serialNumberList ==0:
                    print ("CAUTION: The program could not retrieve the Serial Number from the description")
                    print ("Still we are storing this information in jiratcfiledb.txt")
                    updateFile(jiraDict,"Jiras\\jiratcfiledb.txt",issue,allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild);
                    print ("Moving on to next Jira")
                    continue
            serialNumberList = getSerialNumber(jiraContent.fields.description)
            issueNumber= str(issue)
            copyDiffFiles(serialNumberList,allTestCaseNames,issueNumber,sftp,ssh)
            print (issue,allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild);
            updateFile(jiraDict,"Jiras\\jiratcfiledb.txt",issue,allTestSuiteNames,allTestCaseNames,jiraStatus,jiraResolution,jiraFoundInBuild);
            
        
    print ("Closing Jira Session")
    jira.kill_session()
    print ("Closing SFTP connection")
    ssh.close()

    
def main():
	userName = raw_input ("Enter your quick lookid  :")
	print "Enter password"
	passWord = getpass.getpass()        
	scriptStartTime = datetime.datetime.now()
	lastRunTime = getMeLastRunTime()
	lastRunTime = (re.split(' ',lastRunTime)[0]).strip()
	print lastRunTime
	getUpdatedJiras(lastRunTime,userName,passWord)
	#setLastRunTime(scriptStartTime)
    
main()


