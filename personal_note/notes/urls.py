from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static


urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('topics/new/', views.topic_create, name='topic_create'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('topics/create/', views.create_topic, name='create_topic'),#第二版
    path('topics/<int:topic_id>/delete/', views.topic_delete, name='topic_delete'),
    path('topics/trash/', views.topic_trash, name='topic_trash'),
    path('topics/<int:topic_id>/restore/', views.topic_restore, name='topic_restore'),
    path('topics/<int:topic_id>/edit/', views.topic_edit, name='topic_edit'),
    path('trash/', views.trash_list, name='trash_list'),
    path('restore/<int:pk>/', views.restore_topic, name='restore_topic'),
    path('edit/<int:pk>/', views.edit_topic, name='edit_topic'),
    #path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    #path('topics/<int:topic_id>/note/<int:item_id>/edit/', views.edit_note_item, name='edit_note_item'),
    #path('topics/<int:topic_id>/note/<int:item_id>/delete/', views.delete_note_item, name='delete_note_item'),
    #path('note/<int:item_id>/edit/', views.edit_note_item, name='edit_note_item'),
    path('create_note/<int:topic_id>/', views.create_note_item, name='create_note'),
    path('edit_note/<int:note_id>/', views.edit_note_item, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note_item, name='delete_note'),
    path('topic/<int:topic_id>/note/create/', views.create_note_item, name='create_note_item'),
    #path('note/<int:topic_id>/delete/<int:note_item_id>/', views.delete_note_item, name='delete_note_item'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:topic_id>/delete/', views.topic_delete, name='topic_delete'),
    path('note/<int:topic_id>/delete/<int:note_item_id>/', views.delete_note_item, name='delete_note_item'),
    #path('note/<int:note_item_id>/edit/', views.edit_note_item, name='edit_note_item'),
    path('note/edit/<int:note_id>/', views.edit_note_item, name='edit_note_item'),
    #path('topic/<int:topic_id>/share/', views.share_topic, name='share_topic'),
    #path('accept_invite/<uuid:token>/', views.accept_invite, name='accept_invite'),
    path('topic/<int:topic_id>/share/', views.share_topic, name='share_topic'),
    path('note/<int:note_id>/edit/', views.edit_note_item, name='edit_note_item'),




    # 後續會加上 notes 主題功能
]
'''
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''    