from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

from cases.models import Case, Testplan


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
        plan_list = Testplan.objects.all().order_by("-id")
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
            return JsonResponse({'status': True, 'msg': '保存成功'})