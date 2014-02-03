#!/usr/bin/python
import os
import commands
import re
import time

def run_command (user, host, password, command):
    import pexpect
    return_info="success"
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s -t  %s ' % (user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '],timeout=2)
    if i == 0:
        return_info='ERROR,SSH could not login'
        return return_info
    if i == 1:
        child.sendline ('yes')
        i = child.expect([pexpect.TIMEOUT, 'password: '],timeout=20)
        if i == 0:
            return_info='ERROR,SSH could not login'
            return return_info
    child.sendline(password)
    i = child.expect([pexpect.TIMEOUT, 'Permission denied, please try again.',pexpect.EOF],timeout=30)
    if i==2:
        return "success"
    else:
        return "Permission denied,or Connect timeout"

def install_package():
    sshd = """yum -y install  pexpect*"""
    os.system(sshd)
    
def add_user(user_name):
    status,output=commands.getstatusoutput("useradd -d /search/"+user_name+" -s /bin/bash "+user_name)
    if status != 0:
        return "failed"+output
    else:
        status,out_put=commands.getstatusoutput("echo push_file|passwd "+user_name+" --stdin")
        if status != 0:
            print "faild"+out_put
        return "success"

def backup_ssh(user):
    fp=open("/etc/passwd")
    condition=re.compile(r'%s' % user)
    while 1:
        line=fp.readline()
        if not line:
            break
        match=condition.match(line)
        if match:
            user_home=line.split(":")[-2]
            print user_home
    fp.close()
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    print "cp -r "+user_home+"/.ssh "+user_home+"/.ssh."+date
    status,output=commands.getstatusoutput("ls -l "+user_home+"/.ssh ")
    if status == 0:
        status,output=commands.getstatusoutput("cp -r "+user_home+"/.ssh "+user_home+"/.ssh."+date)
        if status!=0:
            return "failed"+output
        else:
            status,output=commands.getstatusoutput("rm -fr "+user_home+"/.ssh/*")
            if status != 0:
                print "faild"+output
                return "faild"
    gen_rsa(user)
    ip=get_ip()
    push_rsa(ip,user,user_home)
    
def gen_rsa(user_name):
    import pexpect
    print 'su - '+user_name+' -c ssh-keygen -t rsa'
    child = pexpect.spawn ('su - '+user_name+' -c "ssh-keygen -t rsa"')
    child.expect ('Generating.*:')
    child.sendline ()
    child.expect ('Enter.*:')
    child.sendline ()
    child.expect ('Enter.*:')
    child.sendline ()

def get_ip():
    import socket
    host_name = socket.getfqdn(socket.gethostname())  
    host_addr = socket.gethostbyname(host_name)
    return host_addr
def get_hostname():
    import socket 
    return  socket.gethostname()

def push_rsa(ip,user_name,user_home):
    status,output=commands.getstatusoutput("cp %s/.ssh/id_rsa.pub /search/auto_install/id_rsa.pub.%s.%s" % (user_home,ip,user_name))
    if status != 0:
        commands.getstatusoutput("echo 'push rsa error' >>/search/error")
if __name__ == '__main__':
    install_package()
    add_user("push_file")
    backup_ssh("push_file")
    status,output=commands.getstatusoutput("touch /search/auto_install/done")
    if status !=0:
        commands.getstatusoutput("echo %s >>/search/log" % output)
    else:
        ip=get_ip()
        status,output=commands.getstatusoutput("touch /search/auto_install/hello")
        if status !=0:
            commands.getstatusoutput("echo %s >>/search/log" % output)
