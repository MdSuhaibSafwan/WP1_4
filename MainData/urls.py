from django.urls import path
from . import views

urlpatterns = [
path('parts<int:id>', views.viewProjectParts, name='viewProjectParts' ),
path('partDetail<int:id>', views.viewPartDetail, name='viewPartDetail' ),
path('blankDetail<int:id>', views.viewBlankDetail, name='viewBlankDetail' ),
path('plyDetail<int:id>', views.viewPlyDetail, name='viewPlyDetail' ),
path('partSubDetail<int:id>', views.viewPartSubDetail, name='viewPartSubDetail' ),
path('partSubSensorDetail<int:id>', views.viewPartSubSensorDetail, name='viewPartSubSensorDetail' ),
path('processPartSensor<int:id>', views.processPartSensor, name='processPartSensor' ),
path('updateProcessGraph<int:id>', views.updateProcessGraph, name='updateProcessGraph')

]