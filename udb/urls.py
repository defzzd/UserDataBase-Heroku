from django.conf.urls import url

from udb import views

urlpatterns = [

    ## After much frustrated reading, rereading and rerereading of tutorials, the following lines are finalized.
    
    url(r'^$', views.userobject_index, name='userobject_index'),
    
    ## Second option for flexibility
    url(r'^userobject_index', views.userobject_index, name='userobject_index'),
    
    
    ## or perhaps this with refactoring...
    url(r'^(?P<userobject_id>\d+)/$', views.edit_userobject, name="edit_userobject"),
  

    url(r'^delete_userobject/(?P<userobject_id>\d+)/$', views.delete_userobject, name="delete_userobject"),
 
    
    url(r'^create_userobject/$', views.create_userobject, name='create_userobject'),
    
]