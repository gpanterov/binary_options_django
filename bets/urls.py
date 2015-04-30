
from django.conf.urls import patterns, url
from bets import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
	 url(r'^login/$', views.user_login, name='login'),
	url(r'^place_bets/$', views.place_bets, name='place_bets'),
	url(r'^update/$', views.update, name='update'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^deposit/$', views.deposit, name='deposit'),

	)
