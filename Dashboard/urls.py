from django.urls import path, re_path
from . import views

urlpatterns = [
path('dash<int:id>/', views.dashboard, name='dashboard'),    
path('partGraph/', views.part_graph, name='partGraph'),
path('blankGraph/', views.blank_graph, name='blankGraph'),
path('plyGraph/', views.ply_graph, name='plyGraph'),
path('projectDash/', views.project_dash, name='projectDash'),
path('pieChart<int:id>', views.pie_chart, name='pieChart'),
path('subChart-<int:id>-<str:choice>/', views.sub_chart, name='subChart'),
path('pieCostChart<int:id>', views.pie_cost_chart, name='pieCostChart'),
path('costModelChart<int:id>-<str:error>-<int:mID>/', views.cost_model_chart, name='costModelChart'),
]
