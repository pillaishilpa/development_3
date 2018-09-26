import re
"""acclst=[]
accnt={}
i=1
while(i):
	y=raw_input('do u want to add a new account: Y or N')
	if y.lower()=='y':
		accno=int(raw_input('provide your acc number'))
		blnc=float(raw_input('provide your current balance'))
		accnt={'account_number':accno,'balance':blnc}
		acclst.append(accnt)
	elif y.lower()=='n':
		print 'EXITTING...\n'
		i=0
if len(acclst)!=0:
	for val in acclst:
		print val"""
class bank:
	bank_lst=[]
	acc_dict={}
	def __init__(self,acno=None,name=None,balance=0):
		self.acno=acno
		self.name=name
		self.balance=balance
		print '****new account added*****',"\n",'accno:',acno,'name:',name,'balance:',balance,"\n"
	def add_acc(self):
		bank.acc_dict={'account_number':self.acno,'name':self.name,'balance':self.balance}
		bank.bank_lst.append(bank.acc_dict)
	def deposite(self,amnt):
		bank.acc_dict={'balance':amnt}
		bank.bank_lst.append(bank.acc_dict)
	
def main():
	i=1
	while(i):
		opt=raw_input('do u want to add  a new accnt: y or n ')
		if opt.lower()=='y':
			print '*****provide below details*****\n'
			acn=int(raw_input('account_number:'))
			name=raw_input('name:')
			bal=0
			x=bank(acn,name,bal)
			x.add_acc()
			continue
		elif opt.lower()=='n':
			print 'EXITING....'
			i=0
	val=raw_input('do u want to deposite money: y or n')
	if val.lower()=='y':
		amnt=float(raw_input('enter the amount to depost: '))
		x.deposite(amnt)
	elif val.lower()=='n':
		pass
	print bank.bank_lst
main()
	
