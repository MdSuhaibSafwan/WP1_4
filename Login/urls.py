from django.urls import path
from . import views

#url for login page
urlpatterns = [
path('', views.login, name='login'),
path('register/', views.register, name = "register"),
path('mylogout/', views.logout),
path('edit_profile/', views.UserEditView, name = 'edit_profile'),
path('edit_password/', views.change_password, name = 'edit_password'),
path('contact/', views.contact, name='contact'),
path('faq/', views.faq, name='faq'),
path('edit_user_group/', views.edit_user_group, name='edit_user_group'),
path('auto_creation/', views.auto_creation, name="auto_creation")
]