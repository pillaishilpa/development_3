import thread
lock=thread.allocate_lock()
def  fun_1(a):
	while(a>0):
		print 'a=',a
		
		a-=1
		
	
def fun_2(b):
	while (b>0):
		print 'b=',b
		b-=1
def main():
	thread.start_new_thread(fun_1,(20,))
	thread.start_new_thread(fun_1,(10,))
	thread.start_new_thread(fun_2,(10,))
	thread.start_new_thread(fun_2,(10,))
	c=raw_input('enter a key to exit the program:')
main()