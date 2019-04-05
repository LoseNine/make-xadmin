from django.urls import path,include
from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields import related

import copy
from urllib.parse import urlencode


class ModelXadmin:
    def __init__(self,model,site):
        #保存model和站点配置
        self.model=model
        self.site=site

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
        return mark_safe('<input type="checkbox" class="choice_class" value="%s" name="items" />'%(obj.pk))

    list_display=[Check,"id","__str__",Edit,Del]
    get_model_form = []
    list_filter=[]


    def default_action(self,item):
        print(item)
    def delete_action(self,queryset):
        queryset.delete()

    default_action.description='默认操作'
    delete_action.description='delete_action'
    actions=[delete_action]


    def new_acctions(self):
        tmp=[]
        tmp.append(ModelXadmin.default_action)
        tmp.extend(self.actions)
        return tmp

    def show_actions(self):
        #actions=self.actions   #增加默认批量操作
        actions=self.new_acctions()
        temp=[]
        for a in actions:
            temp.append({
                "name":a.__name__,
                'desc':a.description
            })
        return temp

    #自定义分页
    def pagein(self,request,new_data_list,p=1):
        pages = Paginator(new_data_list, 5)
        page = request.GET.get('p', None)
        if page:
            cc = pages.page(page)
        else:
            cc = pages.page(p)
        return cc,pages

    def get_list_filter(self,request):
        #params=copy.deepcopy(request.GET)#放在外边，之后还在里边加，就是说一个模型关联的两张表的信息

        link_dict={}
        for filter_field in self.list_filter:
            params = copy.deepcopy(request.GET)
            cid = request.GET.get(filter_field,0)#用于前端变色

            #根据字段获取关联表
            filter_field_obj=self.model._meta.get_field(filter_field)
            # print('filter_field_obj:',filter_field_obj)
            # print(type(filter_field_obj))
            # if isinstance(filter_field_obj,related.RelatedField):
            #     print('related_model:',filter_field_obj.related_model.objects.all())

            #关联表的全部数据,只适用于一对多，多对多
            if isinstance(filter_field_obj,related.RelatedField):
                data_list=filter_field_obj.related_model.objects.all()
            else:
                #普通字段
                data_list=self.model.objects.values('pk',filter_field)

            temp=[]

            #添加全部标签，有全部的时候删除其他键值
            if params.get(filter_field,None):
                del params[filter_field]
                temp.append('<a href="?%s">全部</a>'%(urlencode(params)))
            else:
                temp.append('<a href="#">全部</a>' )

            #处理关联数据
            for obj in data_list:

                #分开普通字段和多对多
                if isinstance(filter_field_obj,related.RelatedField):
                    pk=obj.pk
                    text=str(obj)
                    params[filter_field] = pk
                else:
                    pk=obj.get('pk')
                    text=obj.get(filter_field)
                    params[filter_field] = text

                _url=urlencode(params)

                if cid==str(pk) or cid==text:
                    link_tag = "<a href='?%s' class='active'>%s</a>" % (_url, text)
                else:
                    link_tag="<a href='?%s'>%s</a>"%(_url,text)
                temp.append(link_tag)

            link_dict[filter_field]=temp

        return link_dict

    def get_filter_condition(self,request):
        filter_condition=Q()
        for filter_field,val in request.GET.items():
            if filter_field in self.list_filter:#排除分页标签的干扰
                filter_condition.children.append((filter_field,val))

        return filter_condition

    def show(self, request):
        filter_fields=self.get_list_filter(request)
        p=request.GET.get('p',1)
        if request.method=='POST':
            actions=request.POST.get('action')
            if actions:
                items=request.POST.getlist("items")
                queryset=self.model.objects.filter(id__in=items)
                try:
                    action_func=getattr(self,actions)
                    action_func(queryset)
                except Exception as e:
                    print(e)
        # app_name=request.path.split('/')[2]
        # model_name = request.path.split('/')[3]
        # print(app_name,model_name)
        model_name=self.model._meta.model_name
        app_name=self.model._meta.app_label

        #为分页添加路由
        show_link='/xadmin/%s/%s/show'%(app_name,model_name)

        #过滤
        filter_condition=self.get_filter_condition(request)

        obj_list = self.model.objects.all().filter(filter_condition)

        #处理数据
        new_data_list=list()
        label_list = []
        # filter_fields=self.list_filter
        # print(filter_fields)
        ADD_LABEL=True # 处理表头,只在第一次循环时候添加，之后改为False
        for obj in obj_list:      #[obj, obj, obj]
            lines=[]
            for line in self.list_display:

                if isinstance(line,str):#如果是字段而不是自定义函数，比如delete，edit等等操作
                    tmp=getattr(obj,line)   #getattr(obj,id)

                    #多对多
                    field_obj = self.model._meta.get_field(line)
                    if isinstance(field_obj,ManyToManyField):
                        tmps=tmp.all()
                        tmp=[]
                        for i in tmps:
                            tmp.append(str(i))
                        tmp=','.join(tmp)

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
        if label_list:
            label_list[0]=mark_safe('<input type="checkbox" id="choice" />')
        add_url=reverse("%s_%s_add"%(app_name,model_name))

        actions=self.show_actions()

        #分页
        cc,pages=self.pagein(request,new_data_list,p)

        return render(request, "show.html",locals())

    def delete(self, request, id):
        model_name=self.model._meta.model_name
        app_name=self.model._meta.app_label
        self.model.objects.filter(id=id).delete()
        return redirect("%s_%s_show"%(app_name,model_name))

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

                model_name = self.model._meta.model_name
                app_name = self.model._meta.app_label
                return redirect("%s_%s_show" % (app_name, model_name))
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

                model_name = self.model._meta.model_name
                app_name = self.model._meta.app_label
                return redirect("%s_%s_show" % (app_name, model_name))
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