class rever_itr:
	def __init__(self,n):
		self.i=n
		
	def __iter__(self):
		return self
	def next(self):
		print 'aa'
		while (1):
			print 'nn'
			if self.i>0:
				i=self.i
				print i,'dd'
				self.i-=1
				print self.i
				yield i
			else:
				print "ERROR"
f=rever_itr([1,2,3])
f.__iter__()
f.next()
f.next()
		