from django.conf.urls import url
from advisor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^write_review/$', views.write_review, name='write_review'),
    url(r'^add_location/$', views.add_location, name='add_location'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^location/(?P<location_name_slug>[\w\-]+)/$', views.location_details, name='location_details'),
    url(r'^location/toggle-visited$', views.toggle_visited, name='toggle_visited'),
    
]
