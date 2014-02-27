#!/usr/bin/python
import pexpect

def run_cmd (method,host,user,password,args):
    return_info="success"
    ssh_newkey = 'Are you sure you want to continue connecting'
    if method == "ssh":
        process  = pexpect.spawn('ssh %s -l %s -t  "%s" ' % (host,user,args[0]))
    else:
        print 'scp -r %s %s@%s:%s  ' % (args[0],user,host,args[1])
        process  = pexpect.spawn('scp -r %s %s@%s:%s' % (args[0],user,host,args[1]))
    return_value = process.expect([pexpect.TIMEOUT, ssh_newkey, 'password: ',pexpect.EOF],timeout=2)
    print "first",return_value
    if return_value == 0:
        return_info='ERROR,SSH could not login'
        return return_info
    elif return_value == 1:
        process.sendline ('yes')
        return_value = process.expect([pexpect.TIMEOUT, 'password: ',pexpect.EOF],timeout=20)
        print "second",return_value
        if return_value == 0:
            return_info='ERROR,SSH could not login'
            return return_info
        elif return_value == 2:
            process.sendline(password)
    elif return_value == 2:
        process.sendline(password)
    else:
        return "success"
    return_value = process.expect([pexpect.TIMEOUT, 'Permission denied, please try again.',pexpect.EOF],timeout=30)
    print "last",return_value
    if return_value==2:
        return "success"
    else:
        return "Permission denied,or Connect timeout"
