from django.urls import path
from ..views import work_volume



urlpatterns = [
    path(
        'work-type/create/',
        work_volume.work_type_list_create_api_view,
        name='work_type_create'
    ),
    path(
        'work-type/<int:obj>/list/',
        work_volume.work_type_list_create_api_view,
        name='work_type_list'
    ),
    path(
        'work-type/<int:pk>/detail/',
        work_volume.work_type_detail_update_delete_api_view,
        name='work_type_retrieve'
    ),
    path(
        'work-type/<int:pk>/update/',
        work_volume.work_type_detail_update_delete_api_view,
        name='work_type_update'
    ),
    path(
        'work-type/<int:pk>/delete/',
        work_volume.work_type_detail_update_delete_api_view,
        name='work_type_delete'
    ),

    # Work Category
    path(
        'work-category/create/',
        work_volume.work_category_list_create_api_view,
        name='work_category_create'
    ),
    path(
        'work-category/<int:obj>/list/',
        work_volume.work_category_list_create_api_view,
        name='work_category_list'
    ),
    path(
        'work-category/<int:pk>/detail/',
        work_volume.work_category_detail_update_delete_api_view,
        name='work_category_retrieve'
    ),
    path(
        'work-category/<int:pk>/update/',
        work_volume.work_category_detail_update_delete_api_view,
        name='work_category_update'
    ),
    path(
        'work-category/<int:pk>/delete/',
        work_volume.work_category_detail_update_delete_api_view,
        name='work_category_delete'
    ),

    # Work volume
    path(
        'create/',
        work_volume.work_volume_list_create_api_view,
        name='work_category_create'
    ),
    path(
        '<int:obj>/list/',
        work_volume.work_volume_list_create_api_view,
        name='work_category_list'
    ),
    path(
        '<int:pk>/detail/',
        work_volume.work_volume_detail_update_delete_api_view,
        name='work_category_retrieve'
    ),
    path(
        '<int:pk>/update/',
        work_volume.work_volume_detail_update_delete_api_view,
        name='work_category_update'
    ),
    path(
        '<int:pk>/delete/',
        work_volume.work_volume_detail_update_delete_api_view,
        name='work_category_delete'
    ),

    # Monthly Work volume
    path(
        'monthly/create/',
        work_volume.monthly_work_volume_list_create_api_view,
        name='work_category_create'
    ),
    path(
        'monthly/<int:obj>/list/',
        work_volume.monthly_work_volume_list_create_api_view,
        name='work_category_list'
    ),
    path(
        'monthly/<int:pk>/detail/',
        work_volume.monthly_work_volume_detail_update_delete_api_view,
        name='work_category_retrieve'
    ),
    path(
        'monthly/<int:pk>/update/',
        work_volume.monthly_work_volume_detail_update_delete_api_view,
        name='work_category_update'
    ),
    path(
        'monthly/<int:pk>/delete/',
        work_volume.monthly_work_volume_detail_update_delete_api_view,
        name='work_category_delete'
    ),
]