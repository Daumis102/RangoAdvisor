from django.conf.urls import url
from advisor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # test done
    url(r'^index/$', views.index, name='index'),  # test done
    url(r'^about/$', views.about, name='about'),  # test done
    url(r'^contacts/$', views.contacts, name='contacts'),  # test done
    url(r'^login/$', views.user_login, name='login'),  # test done
    url(r'^write_review/$', views.write_review, name='write_review'),  # test done
    url(r'^add_location/$', views.add_location, name='add_location'),  # test done
    url(r'^logout/$', views.user_logout, name='logout'),  # test done
    url(r'^register/$', views.register, name='register'),  # test done
    url(r'^location/(?P<location_name_slug>[\w\-]+)/$', views.location_details, name='location_details'),  # test done
    url(r'^location/toggle-visited$', views.toggle_visited, name='toggle_visited'),  # test done
    url(r'^profile/$', views.profile, name='profile'),  # test done
    url(r'^change_pw/$', views.change_pw, name='change_pw'),  # test done
    url(r'^change_pp/$', views.change_pp, name='change_pp'),  # test done
    url(r'^photo/upload/$', views.upload_location_photo, name='photo_upload'),  # test done
    url(r'^profile/deleteaccount/$', views.delete_account, name='delete_account'),  # test done
]
