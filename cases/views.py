import json

import requests
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from cases.models import Case, Testplan, Caseplan


class IndexView(View):
    """首页"""

    def get(self, request):
        return render(request, 'index.html')


class HomeView(View):
    """home页"""

    def get(self, request):
        return render(request, 'home.html')

class CaseListView(View):
    """测试用例列表"""

    def get(self, request,page):
        case_list = Case.objects.all().order_by("-id")
        print(case_list)
        # 分页
        paginator = Paginator(case_list, 1)
        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        cases_page = paginator.page(page)
        num_pages = paginator.num_pages

        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        context = {'casea_page': cases_page,
                   'pages': pages,
                   'page': 'case',
                   'case_list': case_list}
        print(context)
        for i in context['casea_page']:
            print(i)

        return render(request, 'case_list.html', context)


class PlanListView(View):
    """测试计划"""

    def get(self, request, page):
        plan_list = Testplan.objects.filter(is_del=0).order_by('-id')
        return render(request, 'test_plan.html', {'plan_list': plan_list})



class SaveCaseView(View):

    def post(self, request):
        print(request)
        case_id = request.POST.get('id')
        module = request.POST.get('module')
        clazz = request.POST.get('clazz')
        method = request.POST.get('method')
        remark = request.POST.get('remark')

        if case_id:
            case = Case.objects.get(id=case_id)
            case.module = module
            case.clazz = clazz
            case.method = method
            case.remark = remark
            case.save()
            return JsonResponse({'status': True, 'msg': '保存成功'})
        else:
            Case.objects.create(module=module, clazz=clazz, method=method, remark=remark)
            return JsonResponse({'status': True, 'msg': '保存成功'}, json_dumps_params={'ensure_ascii': False})

class OptionlistView(View):
    """获取全部的用例选项"""

    def get(self, request):
        module_list = Case.objects.values('module').distinct()
        print(module_list)
        module = []
        for m in module_list:
            module.append({'name': m['module'], 'children': []})
        print(module)
        clazz_list = Case.objects.values('module', 'clazz')
        for c in clazz_list:
            for m in module:
                if c['module'] == m['name']:
                    if not {'name': c['clazz'], 'children': []} in m['children']:
                        m['children'].append({'name': c['clazz'], 'children': []})
        method_list = Case.objects.values('id', 'clazz', 'method')
        for i in method_list:
            for k in module:
                for j in k['children']:
                        if i['clazz'] == j['name']:
                            j['children'].append({'name': i['method'], 'id': i['id']})
        return JsonResponse({'status': True, 'option': module}, json_dumps_params={'ensure_ascii': False})


class CreateTestPlanView(View):

    def get(self, request):
        pass

    def post(self, request):
        _id = request.POST.get('id')
        name = request.POST.get('name')
        module = request.POST.get('module')
        report = request.POST.get('report')
        remark = request.POST.get('remark')
        case_id_list = str(request.POST.get('case_id_list'))
        if not _id:
            if case_id_list:
                plan = Testplan(name=name, module=module, report=report, remark=remark)
                plan.save()
                for i in case_id_list.split(','):
                    if i:
                        Caseplan.objects.create(case_id=int(i), plan_id=plan.id)
            else:
                return JsonResponse({'status': False, 'msg': " test case not be null"})
            return JsonResponse({'status': True, 'msg': "新增计划成功"}, json_dumps_params={'ensure_ascii': False})


class DelPlanView(View):

    def post(self, request):
        plan_id = request.POST.get('plan_id')
        if plan_id:
            for i in str(plan_id).split(','):
                if i:
                    try:
                        plan = Testplan.objects.get(id=i)
                        plan.is_del = 1
                        plan.save()
                        Caseplan.objects.filter(plan_id=i).update(is_del=1)
                    except:
                        return JsonResponse({'status': False, 'msg': "删除测试任务失败"}, json_dumps_params={'ensure_ascii': False})
            return JsonResponse({'status': True, 'msg': "删除测试任务成功"}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': False, 'msg': "操作失败"}, json_dumps_params={'ensure_ascii': False})


class RunPlanView(View):

    def get(self, request, planid):
        planid = int(planid)
        params = {'test_list': []}
        plan_case = Caseplan.objects.filter(plan_id=planid)
        plan = Testplan.objects.filter(id=planid)[0]
        params['id'] = plan.id
        params['name'] = plan.name
        for i in plan_case:
            case = Case.objects.filter(id=i.case_id)[0]
            params['test_list'].append({'module': case.module, 'clazz': case.clazz, 'method': case.method})
        print(params)
        headers = {
            "Content-Type": "application/json;charset=UTF-8"}
        r = requests.post('http://127.0.0.1:5000/execute_test_plan', data=json.dumps(params), verify=False, headers=headers)
        print(r.text)
        res = json.loads(r.text)
        if res['code'] == 200:
            return JsonResponse({'status': True, 'msg': "请求运行成功，等待运行结果"}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': False, 'msg': res['message']}, json_dumps_params={'ensure_ascii': False})