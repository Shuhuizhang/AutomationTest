from django.db import models

# Create your models here.
from db.base_model import BaseModel


class Case(BaseModel):
    # 测试用例模型

    module = models.CharField(max_length=128, verbose_name="模块")
    clazz = models.CharField(max_length=128, verbose_name="类名")
    method = models.CharField(max_length=128, verbose_name="方法名")
    remark = models.CharField(max_length=500, null=True, verbose_name="备注")

    class Meta:
        db_table = 'tb_test_case'
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name


class Testplan(BaseModel):
    # 测试计划模型

    name = models.CharField(max_length=128, verbose_name="测试任务名称")
    module = models.CharField(max_length=128, verbose_name="模块")
    remark = models.CharField(max_length=128, null=True, verbose_name="备注")
    report = models.CharField(max_length=128, null=True, verbose_name="报告")

    class Meta:
        db_table = 'test_plan'
        verbose_name = '测试任务'
        verbose_name_plural = verbose_name


class Caseplan(BaseModel):

    plan = models.ForeignKey('cases.Testplan', verbose_name='测试任务', on_delete=models.CASCADE)
    case = models.ForeignKey('cases.Case', verbose_name='测试用例', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_plan_case'
        verbose_name = '测试任务用例'
        verbose_name_plural = verbose_name


class Report(BaseModel):
    plan_id = models.IntegerField(verbose_name='测试任务ID')
    report_url = models.CharField(max_length=500, null=True, verbose_name="报告地址")

    class Meta:
        db_table = 'tb_plan_report'
        verbose_name = '测试报告'
        verbose_name_plural = verbose_name