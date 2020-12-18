from django.urls import path,include
from .views import home,post,blog,about,search,post_update,post_delete,post_create,post_by_tag

urlpatterns=[
    path("",home,name='home'),
    path("blog/",blog,name='blog'),
    path("post/<id>/",post,name="post"),
    path("about/",about,name="about"),
    path("search/",search,name="search"),
    path("post/<id>/update",post_update,name="update-post"),
    path("post/<id>/delete",post_delete,name="delete-post"),
    path("create/",post_create,name="create-post"),
    path("post_by_tag/<tag>",post_by_tag,name="post_by_tag"),

]