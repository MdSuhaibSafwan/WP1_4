from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('AMOTAdmin/', views.admin_start, name='admin_start'),
path('adminRequestHard<int:id>/', views.admin_request_hard, name='admin_request'),
path('adminAssignHardware<int:id>/', views.admin_assign_machine, name='admin_assign_hardware'),
path('adminEditProcess<int:id>/', views.admin_edit, name='admin_edit'),
path('adminTotalEditProcess<int:id>/', views.admin_total_edit, name='admin_total_edit'),
path('adminViewAllProcess<int:id>/', views.admin_view_all_process, name='admin_view_all_process'),
path('adminViewProcess<int:id>/', views.admin_view_process, name='admin_view_process'),
path('adminViewSub<int:id>/', views.admin_view_sub, name='admin_view_sub'),
path('adminEditRepeatBlock<int:id>/', views.admin_edit_repeat_block, name='admin_edit_repeat_block'),
path('updatePositions<int:id>', views.updatePositions, name='updatePositions'),
path('updateProPositions<int:id>', views.updateProPositions, name='updateProPositions'),
]