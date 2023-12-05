from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', views.index, name='index'),
path('showProjects/', views.showProjects, name='showProjects'),
path('<int:id>', views.showProcess, name='showProcess' ),
path('c<int:id>', views.showSubProcess, name='showSub' ),
path('p<int:id>', views.showAllProcess, name='showAllProcess' ),
path('environSensors<int:id>', views.showEnvironSensors, name='showEnvironSensors' ),
path('environGraph<int:id>', views.environGraph, name='environGraph'),
path('machineHealth<int:id>', views.machineHealth, name='machineHealth'),
path('machineHealthShow<int:id>', views.machineHealthShow, name='machineHealthShow'),
#path('showProcessGraph<int:id>', views.showProcessGraph, name='showProcessGraph'),
path('popUp<int:id>', views.popUp, name='popUp'),
path('systemArchitecture<int:id>', views.systemArchitecture, name='systemArchitecture'),
path('finalInspection<int:id>', views.showSubProcess, name='finalInspection'),
path('final<int:id>', views.final, name='final'),
path('partStart<int:id>', views.part_start, name='partStart'),
path('upload', views.showSubProcess, name='upload'),
path('viewImages<int:id>', views.viewImages, name='viewImages'),
path('viewImagesDetail<int:id>', views.viewImagesDetail, name='viewImagesDetail'),
path('viewImageSpecific<int:id>-<int:part>', views.viewImageSpecific, name='viewImageSpecific'),
path('viewFiles<int:id>', views.viewFiles, name='viewFiles'),
path('downloadFile<int:id>-<int:part>', views.downloadFile, name='downloadFile'),
path('part_approve<int:id>', views.part_approve, name='part_approve'),
path('part_bad<int:id>', views.part_bad, name='part_bad'),
] 

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
