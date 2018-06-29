# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def dashboard(request):
    #return HttpResponse(request,'hellow how are you')
    return render(request,'ServerAccess/homepage.html')

def result(request):
    serverInfo={}
    serverInfo['ipAddress']=request.GET.get("ip")
    serverInfo['uname'] = request.GET.get("un")
    serverInfo['pword'] = request.GET.get("pw")
    serverInfo['command'] = request.GET.get("cmd")
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(serverInfo['ipAddress'], username=serverInfo['uname'], password=serverInfo['pword'],timeout=10)
        print("connection success")
    except paramiko.SSHException:
        print("Connection Failed")
        quit()
    stdin, stdout, stderr = ssh.exec_command(serverInfo['command'])
    result = stdout.read()
    resultList = result.split('\n')

    serverInfo['result']=filter(None, resultList)
    print(serverInfo)

    return render(request,'ServerAccess/samplepage.html',{'dict':serverInfo})