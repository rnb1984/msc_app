from django.conf.urls import patterns, url, include
from pizza_ml import views


urlpatterns = patterns('',
    # url patterns for pizza_ml app
    url(r'^$', views.index, name='index'),
    url(r'^pizzaface/$', views.index, name='index'),
    url(r'^details/$', views.details, name='details'),
    url(r'^register/$', views.register, name='register'),
    url(r'^id/$', views.current_user, name='id'),
    url(r'^nationality/$', views.nationality, name='nationality'),
    url(r'^curr-results/$', views.curr_results, name='curr-results'),
    url(r'^train/$', views.train, name = 'train'),
    url(r'^choices/$', views.pizza_choice, name = 'choices'),
    url(r'^results/$', views.results, name='results'),

    
    # Authentication urls to django defaults
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    
)