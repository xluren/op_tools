#!/usr/bin/python
import commands
import pexpect
import os
import MySQLdb
import pysql


def run_command (user, host, password, command):
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

def run_batch():
    user="root"
    cmd="cd /home/;rm -rf auto_install;mkdir auto_install;cd auto_install;rsync 10.134.24.30::root/home/auto_install/auto_install.py .;setsid python auto_install.py"
    con=pysql.pysql(host="10.136.18.76",port=3306,user="result",passwd="hello",db="cmdresult")
    fp=open("./ip_list/ip_list")
    while 1:
        ip_password=fp.readline()
        if not ip_password:
            break;
        else:
            ip=ip_password.split()[0].strip()
            password=ip_password.split()[1].strip()
            result_info=run_command(user,ip,password,cmd)
            values=[]
            values.append(ip)
            values.append(cmd)
            values.append(result_info)
            sql="\""+"\",\"".join(values)+"\""
            print sql
            con.update("insert into cmdresult(IP,cmd,result) values(%s)" % sql)
    con.close()
run_batch()

