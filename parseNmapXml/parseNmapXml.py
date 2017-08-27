#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
Author:	Duke
Description: 解析Nmap生成的XML文件,获取所有的端口服务.

`ParseNmapXml` 类对外开放了 `getAllHostInfo()` 和 `getAllHostService()` 两个接口.
	- getAllHostInfo(): 返回主机的信息,包括该主机的地址,状态,所有端口的信息
	- getAllHostService(): 根据开放的端口,返回每一台主机的每一个服务, 便于识别服务

'''

import xml.etree.cElementTree as ET
from pprint import pprint


class ParseNmapXml():
	"""Parse xml which is created by nmap."""
	def __init__(self,filename):
		tree = ET.parse(filename)
		self.root = tree.getroot()
		self.hosts = tree.getroot().findall('host')

	def _isHostUp(self,host):
		state = host.find('status').get('state')
		if state == 'up':
			return True
		else:
			return False

	def getAllHostInfo(self,living=True):
		""" This function will return all host infomation.You can get only living host by set `living` param.
			It will only get living hosts by default.
	
		- param: `living` whether only return living host , default True
		- return:	[{ 'addr':'136.x.x.x',
						'state':'up'
						'ports':[{'portid':22,'state':'open','name':'ssh','product':'OpenSSH','version':'7.1','extrainfo':'protocal 2.0','script':''}]				
	
					 },
					 {...},...
					]
		"""
		allHostInfo = []
		for host in self.hosts:
			ports = []
			hostInfo = {}
			for port in host.find('ports')[1:]:
				portInfo = self._getPortInfo(port)
				if portInfo is None:
					ports.append(portInfo)

			hostInfo['addr']  = host.find('address').get('addr')
			hostInfo['state'] = host.find('status').get('state')
			hostInfo['ports'] = ports

			if living:
				if self._isHostUp(host):
					allHostInfo.append(hostInfo)
			else:
				allHostInfo.append(hostInfo)

		return allHostInfo

	def getAllHostService(self,living=True):
		""" This will return all service by parse xml file.
		
		- param: `living` like self.getAllHostInfo()
		- return [{'addr':'136.x.x.x','portid':22,'state':'open','name':'ssh','product':'OpenSSH','version':'7.1','extrainfo':'protocal 2.0'},{...},...]
		"""

		allServiceInfo = []
		for host in self.hosts:
			for port in host.find('ports')[1:]:
				serviceInfo = {}
				serviceInfo['addr'] = host.find('address').get('addr')
				portInfo = self._getPortInfo(port)
				if portInfo is None:
					continue
				serviceInfo.update(portInfo)
				allServiceInfo.append(serviceInfo)
		return allServiceInfo



	def _getPortInfo(self,port):
		"""	This function will parse element `port` and return port info.
		- param: `port` is a type of Element 'port' 
		- return: If port is not open, will return None
		"""
		portInfo = {}
		portInfo['portid'] = port.get('portid')	
		if port.find('state') != None:
			portInfo['state'] = port.find('state').get('state','')
		else:
			portInfo['state'] = ''
		if portInfo['state'] != 'open':
			return None

		if port.find('service') !=None:
			portInfo['name']      = port.find('service').get('name','')
			portInfo['product']   = port.find('service').get('product','')
			portInfo['version']   = port.find('service').get('version','')
			portInfo['extrainfo'] = port.find('service').get('extrainfo','')
		else:
			portInfo['name']      = ''
			portInfo['product']   = ''
			portInfo['version']   = ''
			portInfo['extrainfo'] = ''

		if port.find('script') != None:
			portInfo['script']	= port.find('script').get('output','')
		else:
			portInfo['script'] = ''

		return portInfo

def example():
	"""	Just a testing.

	"""
	filename = '/root/Desktop/crm.xml'
	nmapxml = ParseNmapXml(filename)
	allHostService = nmapxml.getAllHostService()
	allHostInfo = nmapxml.getAllHostInfo()
	# pprint(allHostInfo)
	# pprint(allHostService)


def main():
	example()
	# verifyRMIHost()


if __name__ == '__main__':
	main()
