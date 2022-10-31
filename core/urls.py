from django.urls import path
from .views import link_list, link_create, like, bookmarking, link_detail, ListUser
from django.views.generic import TemplateView
 #, link_detail, link_create, link_update


urlpatterns = [
    path('like', like   ),# havolalar/create
    path('create', link_create, name="link-create"),# havolalar/create
    path('success', TemplateView.as_view(template_name='success.html'), name="success"),# havolalar/create
    path('e/<str:link_slug>', link_detail),#link/5/bookmark
    path('users', ListUser.as_view(), name="users" ),   # /areas; /tools
    path('<str:slug>', link_list),   # /areas; /tools
    path('<str:slug>/<str:type_slug>', link_list, name="slug") ,  # /areas/design
    path('link/<int:link_id>/bookmark', bookmarking), #link/5/bookmark
#     path('<int:havola_idisi>', link_detail),  # havolalar/10
#     path('<int:link_id>/update', link_update)  # localhost:8000/havolalar/54987/update
]
