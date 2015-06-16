
from django.conf.urls import patterns, url
from bets import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^usdjpy/$', views.usdjpy, name='usdjpy'),
	url(r'^eurchf/$', views.eurchf, name='eurchf'),
	url(r'^usdchf/$', views.usdchf, name='usdchf'),
	url(r'^oil/$', views.oil, name='oil'),
	url(r'^gold/$', views.gold, name='gold'),
	url(r'^uk100/$', views.uk100, name='uk100'),
	url(r'^jpn225/$', views.jpn225, name='jpn225'),
	url(r'^spx500/$', views.spx500, name='spx500'),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
	 url(r'^login/$', views.user_login, name='login'),
	url(r'^place_bets/$', views.place_bets, name='place_bets'),
	url(r'^update/$', views.update, name='update'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^deposit/promo/$', views.promo, name='promo'),	
	url(r'^deposit/', views.deposit2, name='deposit'),
	url(r'^deposit_received/', views.deposit_received, name='deposit_receieved'),
	url(r'^update_results/$', views.update_results, name='update_results'),
	url(r'^withdraw/$', views.withdraw, name='withdraw'),
	)
