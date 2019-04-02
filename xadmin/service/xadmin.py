from django.urls import path,include
from django.shortcuts import render,HttpResponse
from django.utils.safestring import mark_safe
from django.urls import reverse

class ModelXadmin:
    def Edit(self,obj=None):
        model_name=self.model._meta.model_name
        app_label=self.model._meta.app_label
        _url=reverse("%s_%s_edit"%(app_label,model_name),args=(obj.pk,))
        return mark_safe("<a href='%s' id='edit'>编辑</a>"%_url)


    def Del(self,obj=None):
        model_name=self.model._meta.model_name
        app_label=self.model._meta.app_label
        _url = reverse("%s_%s_del" % (app_label, model_name), args=(obj.pk,))
        return mark_safe("<a href='%s' >删除</a>"%_url)

    def Check(self,obj=None):
        return mark_safe('<input type="checkbox" class="choice_class" />')

    list_display=[Check,"id","__str__",Edit,Del]
    get_model_form = []


    def __init__(self,model,site):
        #保存model和站点配置
        self.model=model
        self.site=site

    def show(self, request):
        # app_name=request.path.split('/')[2]
        # model_name = request.path.split('/')[3]
        # print(app_name,model_name)
        model_name=self.model._meta.model_name
        app_name=self.model._meta.app_label

        obj_list = self.model.objects.all()

        #处理数据
        new_data_list=list()
        label_list = []
        ADD_LABEL=True # 处理表头,只在第一次循环时候添加，之后改为False
        for obj in obj_list:      #[obj, obj, obj]
            lines=[]
            for line in self.list_display:
                if isinstance(line,str):#如果是字段而不是自定义函数，比如delete，edit等等操作
                    tmp=getattr(obj,line)   #getattr(obj,id)

                    if ADD_LABEL:
                        #如果model存在自定义的汉字名字，则使用
                        #如果没有就是用哪个英文名
                        try:
                            verbose_name=obj._meta.get_field(line).verbose_name
                            if verbose_name:
                                label_list.append(verbose_name)
                            else:
                                label_list.append(line)
                        except Exception as e:
                            #print('[Warning]',e)
                            label_list.append("默认字段")

                elif callable(line):    #如果是一个自定义函数，就是可回调的，走这一条路
                    tmp=line(self,obj)      #加入的是自定义函数的返回值，也就是一个url链接（a标签）

                    if ADD_LABEL:
                        label_list.append("操作")

                lines.append(tmp)
            ADD_LABEL=False
            new_data_list.append(lines)

        label_list[0]=mark_safe('<input type="checkbox" id="choice" />')
        add_url=reverse("%s_%s_add"%(app_name,model_name))
        return render(request, "show.html",locals())

    def delete(self, request, id):
        self.model.objects.filter(id=id).delete()
        return self.show(request)

    # 自定义model样式
    def get_form(self):
        if not self.get_model_form:
            from django.forms import ModelForm, widgets as wid
            class ModelAdd(ModelForm):
                class Meta:
                    model = self.model
                    fields = '__all__'

            return ModelAdd
        else:
            return self.get_model_form

    def add(self, request):
        Modeldemo=self.get_form()
        form=Modeldemo()
        if request.method=='POST':
            form=Modeldemo(request.POST)
            if form.is_valid():
                obj=form.save()
                return self.show(request)
        return render(request, "add.html",locals())

    def edit(self, request, id):
        obj = self.model.objects.get(id=id)
        ModelAdd=self.get_form()
        form=ModelAdd(instance=obj)
        if request.method=='POST':
            print(request.POST)
            form=ModelAdd(request.POST,instance=obj)
            if form.is_valid():
                form.save()
                return self.show(request)
        return render(request,'edit.html',locals())

    @property
    def get_urls2(self):
        tmp = []
        # 添加增删改查
        model_name=self.model._meta.model_name
        app_name=self.model._meta.app_label

        tmp.append(path('show', self.show,name="%s_%s_show"%(app_name,model_name)))
        tmp.append(path('add', self.add,name="%s_%s_add"%(app_name,model_name)))
        tmp.append(path('<int:id>/delete', self.delete,name="%s_%s_del"%(app_name,model_name)))
        tmp.append(path('<int:id>/edit', self.edit,name="%s_%s_edit"%(app_name,model_name)))
        return tmp, None
        
#单例类
class XadminConfig:
    def __init__(self):
        self._registry=dict()
    
    def register(self,model,xadmin_class=None,**options):
        if not xadmin_class:
            xadmin_class=ModelXadmin
        self._registry[model]=xadmin_class(model,self)  #{Questions:ModelXadmin(Questions)}

    @property
    def get_urls(self):
        tmp = []
        # 模型与模型配置的实例类
        for model, xadmin_class_obj in self._registry.items():
            app_name = model._meta.app_label  # app名字
            model_name = model._meta.model_name  # model名字
            tmp.append(path('{0}/{1}/'.format(app_name, model_name), include(xadmin_class_obj.get_urls2), None), )
        return tmp, None

site=XadminConfig()