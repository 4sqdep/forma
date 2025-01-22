from django.db.models import Sum
from main.apps.reestr.models.construction import ConstructionTask
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField



def constructions_total_cost(next_stage_document=None):
    construction_task = ConstructionTask.objects.all()
    if next_stage_document:
        construction_task = construction_task.filter(next_stage_document=next_stage_document)
    total_cost = construction_task.aggregate(total_cost=Sum('total_cost'))['total_cost']
    return total_cost or 0


def constructions_total_cost_for_month(queryset):
    month_totals = (
        queryset.values(
            'year__id',
            'year__title',
            'month__id', 
            'month__title',
        ).annotate(total_month_sum=Sum('spent_amount')).order_by('month__title')
    )
    return [
        {
            'year_id': month['year__id'],
            'year_title': month['year__title'],
            'month_id': month['month__id'],
            'month_title': month['month__title'],
            'total_month_sum': month['total_month_sum'] or 0,
        }
        for month in month_totals
    ]


def get_total_year_sum(queryset):
    year_totals = (
        queryset.values(
            'year__id', 
            'year__title',
            'construction_task__id', 
            'construction_task__title'
        ).annotate(total_year_sum=Sum('spent_amount')).order_by('year__title')
    )
    return [
        {
            'year_id': year['year__id'],
            'year_title': year['year__title'],
            'total_year_sum': year['total_year_sum'] or 0,
            'task_title': year['construction_task__title']
        }
        for year in year_totals
    ]


def total_year_calculation_horizontally(queryset):
    total_year_sum = get_total_year_sum(queryset)
    year_totals = {}

    for item in total_year_sum:
        year_id = item["year_id"]
        year_title = item["year_title"]
        total_year_sum = item["total_year_sum"]

        if year_id in year_totals:
            year_totals[year_id]['total_year_sum'] += total_year_sum
        else:
            year_totals[year_id] = {
                'year_id': year_id,
                'year_title': year_title,
                'total_year_sum': total_year_sum
            }
    return list(year_totals.values())


def get_fact_sum(queryset):
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



def get_total_fact_sum(queryset):
    fact_sums = get_fact_sum(queryset)
    total = sum(item['total_spent'] for item in fact_sums)
    return total


def get_difference(queryset):
    fact_sum = get_fact_sum(queryset)

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


def get_total_difference(queryset):
    differences = get_difference(queryset)
    total = sum(item['task_difference_amount'] for item in differences)
    return total
