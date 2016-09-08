from django.conf.urls import patterns, url, include
from pizza_ml import views


urlpatterns = patterns('',
    # url patterns for pizza_ml app
    url(r'^$', views.index, name='index'),
    url(r'^test/predict/$', views.predict_pizza, name='predict'),

    
)