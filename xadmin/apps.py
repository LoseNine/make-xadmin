from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class XadminConfig(AppConfig):
    name = 'xadmin'

    def ready(self):
        #查看admin源码，发现django自启动的时候调用这个，全局的admin都会被调用
        autodiscover_modules('xadmin', register_to=None)
