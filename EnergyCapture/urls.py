from django.urls import path
from . import views

urlpatterns = [
path('addPowerClamps<int:id>/', views.addPowerClamps, name='addPowerClamps'),
path('addStation/', views.addStation, name='addStation'),
path('addEquipment<int:id>/', views.addEquipment, name='addEquipment'),
path('energyCaptureDashboard/', views.energyCaptureDashboard, name="energyCaptureDashboard"),
path('overviewHierarchy/', views.overviewHierarchy, name="overviewHierarchy"),
path('grab_pie_kWh_station', views.grab_pie_kWh_station, name="grab_pie_kWh_station"),
path('grabEnergy_PowerClamp<int:id>', views.grabEnergy_PowerClamp, name="grabEnergy_PowerClamp"),
path('grabEnergy_Equipment<int:id>', views.grabEnergy_Equipment, name="grabEnergy_Equipment"),
path('grabEnergy_Station', views.grabEnergy_Station, name="grabEnergy_Station"),
path('grabCO2_Station', views.grabCO2_Station, name="grabCO2_Station"),
path('grab_pie_CO2_station', views.grab_pie_CO2_station, name="grab_pie_CO2_station"),
path('grab_line_kWh_all', views.grab_line_kWh_all, name="grab_line_kWh_all"),
path('grab_line_CO2_all', views.grab_line_CO2_all, name="grab_line_CO2_all"),
path('populate_bar_chart', views.populate_bar_chart, name="populate_bar_chart"),
path('stationDashboard<int:id>/', views.viewStationDashboard, name="viewStationDashboard"),
path('equipmentDashboard<int:id>/', views.viewEquipmentDashboard, name="viewEquipmentDashboard"),
path('grab_indiviudal_station_kWh<int:id>', views.grab_indiviudal_station_kWh, name= "grab_indiviudal_station_kWh"),
path('grab_individual_station_CO2<int:id>', views.grab_individual_station_CO2, name="grab_individual_station_CO2"),
path('grab_equipment_kWh_CO2<int:id>', views.grab_equipment_kWh_CO2, name="grab_equipment_kWh_CO2"),
path('grab_equipment_line_kWh<int:id>', views.grab_equipment_line_kWh, name="grab_equipment_line_kWh"),
path('grab_equipment_line_CO2<int:id>', views.grab_equipment_line_CO2, name="grab_equipment_line_CO2"),
path('grab_individual_equipment_kWh<int:id>', views.grab_individual_equipment_kWh, name="grab_individual_equipment_kWh"),
path('grab_individual_equipment_CO2<int:id>', views.grab_individual_equipment_CO2, name="grab_individual_equipment_CO2"),
path('grab_clamps_line_kWh<int:id>', views.grab_clamps_line_kWh, name="grab_clamps_line_kWh"),
path('grab_clamps_line_CO2<int:id>', views.grab_clamps_line_CO2, name="grab_clamps_line_CO2"),
path('grab_clamp_kWh_CO2<int:id>', views.grab_clamp_kWh_CO2, name="grab_clamp_kWh_CO2"),
] 