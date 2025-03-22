from main.apps.dashboard.models.construction_installation_work import ConstructionInstallationProject, MonthlyCompletedTask
from django.db.models import Sum, DecimalField
from django.db.models.functions import ExtractYear, ExtractMonth, Coalesce



def constructions_total_cost(section=None):
    completed_task = MonthlyCompletedTask.objects.all()
    if section:
        completed_task = completed_task.filter(construction_installation_project__section=section)
    total_cost = completed_task.aggregate(total_cost=Sum('construction_installation_project__allocated_amount', distinct=True))['total_cost']
    return total_cost or 0


def constructions_total_cost_for_month(queryset, section=None):
    if section:
        queryset = queryset.filter(construction_installation_project__section=section)

    month_totals = (
        queryset.annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        )
        .values('year', 'month')
        .annotate(total_month_sum=Sum('monthly_amount'))
        .order_by('year', 'month')
    )
    return [
        {
            'year': month['year'],
            'month': month['month'],
            'total_month_sum': month['total_month_sum'] or 0,
        }
        for month in month_totals
    ]


def get_total_year_sum(queryset, section=None):
    if section:
        queryset = queryset.filter(construction_installation_project__section=section)

    year_totals = (
        queryset.annotate(year=ExtractYear('date'))  
        .values('construction_installation_project__id', 'construction_installation_project__title', 'year')  
        .annotate(total_year_sum=Sum('monthly_amount'))  
        .order_by('year') 
    )
    grouped_data = {}
    for year in year_totals:
        task_id = year['construction_installation_project__id']
        if task_id not in grouped_data:
            grouped_data[task_id] = {
                'task_title': year['construction_installation_project__title'],
                'year_sums': []
            }
        grouped_data[task_id]['year_sums'].append({
            'year': year['year'],
            'total_year_sum': year['total_year_sum'] or 0
        })
    return grouped_data


def total_year_calculation_horizontally(queryset, section=None):
    total_year_sum = get_total_year_sum(queryset, section)
    year_totals = {}

    for task_id, task_data in total_year_sum.items():
        for item in task_data['year_sums']:
            year = item["year"]
            total_year_sum = item["total_year_sum"]

            if year in year_totals:
                year_totals[year]['total_year_sum'] += total_year_sum
            else:
                year_totals[year] = {
                    'year': year,
                    'total_year_sum': total_year_sum
                }
    return list(year_totals.values())


def get_fact_sum(queryset, section=None):
    if section:
        queryset = queryset.filter(construction_installation_project__section=section)

    grouped_data = (
        ConstructionInstallationProject.objects.annotate(
            total_spent=Coalesce(
                Sum('monthly_tasks__monthly_amount', filter=queryset.filter(construction_installation_project__isnull=False)),
                0
            )
        )
        .values('id', 'title')
        .annotate(total_spent=Sum('monthly_tasks__monthly_amount', output_field=DecimalField()))
        .order_by('id') 
    )

    return [
        {
            'construction_installation_project_id': task['id'],
            'construction_installation_project_title': task['title'],
            'total_spent': task['total_spent'] or 0 
        }
        for task in grouped_data
    ] 


def get_total_fact_sum(queryset, section=None):
    fact_sums = get_fact_sum(queryset, section)
    total = sum(item['total_spent'] for item in fact_sums)
    return total


def get_difference(queryset, section=None):
    fact_sum = get_fact_sum(queryset, section)

    difference_each_task = []
    processed_task_ids = set()

    grouped_data = queryset.values(
        'construction_installation_project__id', 
        'construction_installation_project__title', 
        'construction_installation_project__allocated_amount'
    )
    for task in grouped_data:
        if task['construction_installation_project__id'] in processed_task_ids:
            continue
        processed_task_ids.add(task['construction_installation_project__id'])

        task_fact_sum = next((item['total_spent'] for item in fact_sum if item['construction_installation_project_id'] == task['construction_installation_project__id']), 0)
        
        allocated_amount = task['construction_installation_project__allocated_amount'] or 0
        difference_amount = allocated_amount - task_fact_sum
        
        difference_each_task.append({
            'task_id': task['construction_installation_project__id'],
            'task_title': task['construction_installation_project__title'],
            'task_difference_amount': difference_amount,
        })
    return difference_each_task


def get_total_difference(queryset, section=None):
    differences = get_difference(queryset, section)
    total = sum(item['task_difference_amount'] for item in differences)
    return total

