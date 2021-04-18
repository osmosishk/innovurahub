from rest_framework import routers
from slaves_app import views
from django.urls import path

router = routers.SimpleRouter()

router.register(r'Slaves', views.SlaveViewSet, basename="Slaves_list")
router.register(r'Setting', views.SettingViewSet, basename="Setting_list")
router.register(r'MemoryZone', views.MemoryZoneViewSet, basename="Memory_Zone_list")
router.register(r'DataHistory', views.DataHistoryViewSet, basename="Data_History_list")


urlpatterns = [path('slave_search/', views.look_for_slaves),
               path('control/start', views.start),
               path('control/stop', views.stop),
               path('control/status', views.dataloggerstatus),
               path('control/slaveenable/<int:slave_id>/', views.slaveenable),
               path('control/slavedisable/<int:slave_id>/', views.slavedisable),
               path('data/<int:job_id>/', views.showdata),
               path('instantdata/<int:job_id>/', views.showinstantdata),
               path('deletedata/<int:job_id>/', views.deletedata),
               path('redis/', views.getredisdata),

               ]
urlpatterns += router.urls
