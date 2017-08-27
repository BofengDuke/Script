Nmap 的输出的XML格式文件解析小工具
---

简介
---
这小工具主要是方便对Nmap输出的XML文件进行提取内容,并批量处理操作.
除了`parseNmapXml.py`文件是主提取文件,其他文件均是小插件.

`ParseNmapXml` 类对外开放了 `getAllHostInfo()` 和 `getAllHostService()` 两个接口,方便获取数据.
    - getAllHostInfo(): 返回主机的信息,包括该主机的地址,状态,所有端口的信息
    - getAllHostService(): 根据开放的端口,返回每一台主机的每一个服务, 便于识别服务


小插件
---
目前的插件有:

* getAllWebService.py 提取所有的web服务,方便批量暴破路径等
* verifyRMIHost.py 批量验证ＲＭＩ远程攻击服务,依赖　attackRMI.jar 文件
