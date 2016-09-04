from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import *

# For API's
from pizza_ml import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pizza_face_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('pizza_ml.urls')),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    
    # APIs
    url(r'^pizzas/', views.PizzaList.as_view()),
    url(r'^pizzas/(?P<pk>[0-9]+)/$', views.PizzaList.as_view()),
    url(r'^ingredients/', views.IngredientList.as_view()),
    url(r'^ingredients/(?P<pk>[0-9]+)/$', views.IngredientList.as_view()),
    url(r'^userdetails/', views.UserPreferanceView.as_view()),
    url(r'^userdetails/(?P<pk>[0-9]+)/$', views.UserPreferanceView.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
        