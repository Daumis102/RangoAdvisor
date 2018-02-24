from django.conf.urls import url
from advisor import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^about/',views.about, name='about'),
    url(r'^login/',views.user_login, name='login'),
    url(r'^add_place/',views.add_place, name='add_place'),
    url(r'^logout/',views.user_logout, name='logout'),
    
]
