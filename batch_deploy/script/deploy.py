#!/usr/bin/python
import pcmd
import threading
import ConfigParser
import sys

class pcmd_thread(threading.Thread):
    def __init__(self,method,ip,user,password,args):
        threading.Thread.__init__(self)
        self.method=method
        self.ip=ip
        self.user=user
        self.password=password
        self.args=args
    def run(self):
        print self.method,self.ip,self.user,self.password,self.args
        result=pcmd.run_cmd(self.method,self.ip,self.user,self.password,self.args)
        print result


def deal_host(host_name):
    user_ip=host_name.split("@")
    if len(user_ip) == 1:
        return "root",user_ip[0]
    elif len(user_ip)==2:
        return user_ip[0],user_ip[1]
    else:
        return None

def deal_other(host_name):
    password=host_name.split()[1].strip()
    user,ip=deal_host(host_name.split()[0])
    return  user,ip,password
    
if __name__=="__main__":
    conf=ConfigParser.ConfigParser()
    conf.read("../conf/batch.cfg")
    print conf.sections()
    if "cmd" in  conf.sections():
        ip_list=conf.get("cmd","ip_list")
        password=conf.get("cmd","password")
        cmd_list=conf.get("cmd","cmd_list")
        args=[]
        args.append(cmd_list)
        print ip_list,password,cmd_list
        for user_ip in ip_list.split(","):
            user,ip=deal_host(user_ip)
            if not user :
                pass
            thread=pcmd_thread("ssh",ip,user,password,args)
            thread.run()
    if  "file" in  conf.sections():
        print "here"
        ip_list=conf.get("file","ip_list")
        password=conf.get("file","password")
        file_path=conf.get("file","file_path")
        remote_path=conf.get("file","remote_path")
        args=[]
        args.append(file_path)
        args.append(remote_path)
        for user_ip in ip_list.split(","):
            user,ip=deal_host(user_ip)
            if not user :
                pass
            thread=pcmd_thread("scp",ip,user,password,args)
            thread.run()
    if "cmd_other" in  conf.sections():
        ip_list=conf.get("cmd_other","ip_list")
        cmd_list=conf.get("cmd_other","cmd_list")
        print ip_list
        print ip_list.split(",")
        args=[]
        args.append(cmd_list)
        for user_ip in ip_list.split(","):
            user,ip,password=deal_other(user_ip)
            if not user :
                pass
            thread=pcmd_thread("ssh",ip,user,password,args)
            thread.run()
    if  "file_other" in  conf.sections():
        print "here"
        ip_list=conf.get("file_other","ip_list")
        file_path=conf.get("file_other","file_path")
        remote_path=conf.get("file_other","remote_path")
        args=[]
        args.append(file_path)
        args.append(remote_path)
        for user_ip in ip_list.split(","):
            user,ip,password=deal_other(user_ip)
            if not user :
                pass
            thread=pcmd_thread("scp",ip,user,password,args)
            thread.run()
