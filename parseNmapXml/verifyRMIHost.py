#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
Author:	Duke
Description: 根据`ParseNmapXml`类对Nmap输出的xml文件进行解析,并对结果中的所有RMI服务进行验证是否有漏洞.
'''

from parseNmapXml import ParseNmapXml
import os,subprocess

def verifyRMIHost(output='rmi_verify_result.txt',filename):
	""" This function will verify all RMI host from xml file which is created by nmap.

	"""
	
	nmapxml  = ParseNmapXml(filename)
	allHostService = nmapxml.getAllHostService()
	if os.path.exists(output):
		os.remove(output)
	
	# Get all rmi service host
	rmiSericeHost = []
	for service in allHostService:
		if 'rmi' in service['name']:
			rmiSericeHost.append(service)

	
	for service in rmiSericeHost:
		host = service['addr']
		port = service['portid']
		_verify(host,port)

def _verify(host,port):
		CMD = "java -jar attackRMI.jar {host} {port}".format(host=host,port=port)
		
		child = subprocess.Popen(CMD,stdout=subprocess.PIPE,shell=True,close_fds=True,bufsize=40)
		try:
			content = child.stdout.read()
			print host+":"+str(port)+" "+ content.strip('\n')
		except KeyboardInterrupt as e:
			print 'There maybe a vuln in ' + host+' '+str(port)
			with open(output,'a+') as fp:
				fp.write(host+' '+str(port)+'\n')



if __name__ == '__main__':
	filename = 'nmap_output.xml'
	verifyRMIHost(filename=filename)