from django.contrib import admin
from django.urls import path
from robots import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots/', views.get_robots, name='robots'),
    path('robots/data/', views.get_robots_data, name='robots data'),
    path('robot/<int:robot_id>', views.get_robot_data, name='get robot data'),
    path('location/', views.get_location, name='location'),
    path('telemetry/', views.get_telemetry, name='telemetry'),
    path('lastlocation/', views.get_latest_location, name='latest location'),
    path('modify/<int:robot_id>', views.modify_robot_brand, name='modify robot model')
]
