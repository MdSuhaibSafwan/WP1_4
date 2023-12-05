from django.urls import path
from . import views as v

urlpatterns = [
path('export<int:id>-<int:partID>', v.exportCSV, name='ExpCSV'),
path('exportPDF<int:id>-<int:partID>', v.exportPDF, name='ExpPDF'),
path('exportSysArchitectureCSV<int:id>', v.exportSysArchitectureCSV, name="exportSysArchitectureCSV"),
path('exportSysArchitecturePDF<int:id>', v.exportSysArchitecturePDF, name="exportSysArchitecturePDF"),
path('exportPartPDF<int:id>', v.exportPartPDF, name='exportPartPDF'),
path('exportPartCSV<int:id>', v.exportPartCSV, name='exportPartCSV'),
path('dash<int:pID>/exportDashboard<int:id>/<str:type>', v.exportDashboard, name='exportDashboardCSV'),
]
