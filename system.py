
import os
import re
import paramiko
import spur
"""ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('153.64.30.101',username='root',password='Beagl342')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sshpass -p "Beagl342" scp -r root@10.25.36.111:/sh.txt /sh.txt')
print ssh_stderr"""
spur.ssh.MissingHostKey.accept
shell=spur.SshShell(hostname="153.64.30.101", username="root", password="Beagl342")
spur.ssh.MissingHostKey.accept
result=shell.run("pdestate -a")
print result.oputput
