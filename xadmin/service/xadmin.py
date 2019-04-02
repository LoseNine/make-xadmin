from django.urls import path,include
from django.shortcuts import render,HttpResponse

class ModelXadmin:
    def __init__(self,model,site):
        self.model=model
        self.site=site
        
#单例类
class XadminConfig:
    def __init__(self):
        self._registry=dict()
    
    def register(self,model,xadmin_class=None,**options):
        if not xadmin_class:
            xadmin_class=ModelXadmin
        self._registry[model]=xadmin_class(model,self)  #{Questions:ModelXadmin(Questions)}

    def show(self,request):
        # app_name=request.path.split('/')[2]
        # model_name = request.path.split('/')[3]
        # print(app_name,model_name)

        return render(request,"show.html")

    def delete(self,request, id):
        return render(request, "delete.html")

    def add(self,request):
        return render(request, "add.html")

    def edit(self,request, id):
        return render(request, "edit.html")
    
    @property
    def get_urls2(self):
        tmp = []
        # 添加增删改查
        tmp.append(path('show', self.show))
        tmp.append(path('add', self.add))
        tmp.append(path('<int:id>/delete', self.delete))
        tmp.append(path('<int:id>/edit', self.edit))
        return tmp,None
    
    @property
    def get_urls(self):
        tmp = []
        for model, xadmin_class_obj in self._registry.items():
            app_name = model._meta.app_label  # app名字
            model_name = model._meta.model_name  # model名字
            tmp.append(path('{0}/{1}/'.format(app_name, model_name), include(self.get_urls2), None), )
        return tmp,None
        
site=XadminConfig()