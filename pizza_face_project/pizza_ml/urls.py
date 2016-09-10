from django.conf.urls import patterns, url, include
from pizza_ml import views


urlpatterns = patterns('',
    # url patterns for pizza_ml app
    url(r'^$', views.index, name='index'),
    url(r'^test/predict/$', views.predict_pizza, name='predict'),
    url(r'^details/$', views.details, name='details'),
    url(r'^register/$', views.register, name='register'),
    

    
)