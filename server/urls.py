from django.urls import path
from . import views

urlpatterns=[
  path('login/',views.login),
  path('logout/',views.logout),
  path('poststory/',views.poststory),
  path('getstories/',views.getstories),
  path('deletestory/',views.deletestory),

]
