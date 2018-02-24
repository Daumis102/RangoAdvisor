from django.conf.urls import url
from advisor import views

urlpatterns = [
    #url(r'^$',views.index, name='index'),
    url(r'^about/',views.about, name='about'),
    url(r'^login/',views.user_login, name='login'),
    
]
