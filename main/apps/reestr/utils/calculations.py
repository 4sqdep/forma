from main.apps.reestr.models.construction import ConstructionTask, MonthlyExpense
from django.db.models import Sum, DecimalField
from django.db.models.functions import ExtractYear, ExtractMonth, Coalesce




def constructions_total_cost(next_stage_document=None):
    monthly_expense = MonthlyExpense.objects.all()
    if next_stage_document:
        monthly_expense = monthly_expense.filter(construction_task__next_stage_document=next_stage_document)
    total_cost = monthly_expense.aggregate(total_cost=Sum('construction_task__total_cost'))['total_cost']
    return total_cost or 0


def constructions_total_cost_for_month(queryset, next_stage_document=None):
    if next_stage_document:
        queryset = queryset.filter(construction_task__next_stage_document=next_stage_document)

    month_totals = (
        queryset.annotate(
            year=ExtractYear('date'),
            month=ExtractMonth('date')
        )
        .values('year', 'month')
        .annotate(total_month_sum=Sum('spent_amount'))
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


def get_total_year_sum(queryset, next_stage_document=None):
    if next_stage_document:
        queryset = queryset.filter(construction_task__next_stage_document=next_stage_document)

    year_totals = (
        queryset.annotate(year=ExtractYear('date'))  
        .values('construction_task__id', 'construction_task__title', 'year')  
        .annotate(total_year_sum=Sum('spent_amount'))  
        .order_by('year') 
    )
    grouped_data = {}
    for year in year_totals:
        task_id = year['construction_task__id']
        if task_id not in grouped_data:
            grouped_data[task_id] = {
                'task_title': year['construction_task__title'],
                'year_sums': []
            }
        grouped_data[task_id]['year_sums'].append({
            'year': year['year'],
            'total_year_sum': year['total_year_sum'] or 0
        })
    return grouped_data


def total_year_calculation_horizontally(queryset, next_stage_document=None):
    total_year_sum = get_total_year_sum(queryset, next_stage_document)
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


def get_fact_sum(queryset, next_stage_document=None):
    if next_stage_document:
        queryset = queryset.filter(construction_task__next_stage_document=next_stage_document)

    grouped_data = (
        ConstructionTask.objects.annotate(
            total_spent=Coalesce(
                Sum('monthly_construction_task__spent_amount', filter=queryset.filter(construction_task__isnull=False)),
                0
            )
        )
        .values('id', 'title')
        .annotate(total_spent=Sum('monthly_construction_task__spent_amount', output_field=DecimalField()))
        .order_by('id') 
    )

    return [
        {
            'construction_task_id': task['id'],
            'construction_task_title': task['title'],
            'total_spent': task['total_spent'] or 0 
        }
        for task in grouped_data
    ] 


def get_total_fact_sum(queryset, next_stage_document=None):
    fact_sums = get_fact_sum(queryset, next_stage_document)
    total = sum(item['total_spent'] for item in fact_sums)
    return total


def get_difference(queryset, next_stage_document=None):
    fact_sum = get_fact_sum(queryset, next_stage_document)

    difference_each_task = []
    processed_task_ids = set()

    grouped_data = queryset.values(
        'construction_task__id', 
        'construction_task__title', 
        'construction_task__total_cost'
    )
    for task in grouped_data:
        if task['construction_task__id'] in processed_task_ids:
            continue
        processed_task_ids.add(task['construction_task__id'])

        task_fact_sum = next((item['total_spent'] for item in fact_sum if item['construction_task_id'] == task['construction_task__id']), 0)
        
        total_cost = task['construction_task__total_cost'] or 0
        difference_amount = total_cost - task_fact_sum
        
        difference_each_task.append({
            'task_id': task['construction_task__id'],
            'task_title': task['construction_task__title'],
            'task_difference_amount': difference_amount,
        })
    return difference_each_task


def get_total_difference(queryset, next_stage_document=None):
    differences = get_difference(queryset, next_stage_document)
    total = sum(item['task_difference_amount'] for item in differences)
    return total

