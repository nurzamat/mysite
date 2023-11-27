from django.conf.urls import url
from . import views

app_name = 'arzymo'
urlpatterns = [

    # API
    url(r'^api/categories/$', views.categories, name='categories'),
    url(r'^api/countries/$', views.countries, name='countries'),
    url(r'^api/regions/$', views.regions, name='regions'),
    url(r'^api/register/$', views.create_user, name='create_user'),
    url(r'^api/login/$', views.login, name='login'),
    url(r'^api/category/(?P<type>[0-9]+)/posts/$', views.posts, name='posts'), #if type = 0 show all posts
    url(r'^api/user/(?P<user_id>[0-9]+)/posts/$', views.user_posts, name='user_posts'),
    url(r'^api/post/(?P<post_id>[0-9]+)/hitcount/$', views.post_hitcount, name='post_hitcount'),
    url(r'^api/posts/search/$', views.search_post, name='search_post'),  # if type = 0 search in all posts
    url(r'^api/posts/create/$', views.create_post, name='create_post'),
    url(r'^api/post/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    #url(r'^api/post/(?P<post_id>[0-9]+)/images/$', views.save_images, name='save_images'),  # todo
    #url(r'^api/user/(?P<user_id>[0-9]+)/profile/image/$', views.save_profile_image, name='save_profile_image'),  # todo
    #url(r'^api/post/(?P<post_id>[0-9]+)/$', views.update_post, name='update_post'),  # todo
    #url(r'^api/post/(?P<post_id>[0-9]+)/$', views.delete_post, name='delete_post'),  # todo
    #url(r'^api/user/(?P<user_id>[0-9]+)/profile/$', views.edit_profile, name='edit_profile'),  # todo

    # API Chat
    #url(r'^api/user/(?P<user_id>[0-9]+)/profile/$', views.update_gcmId, name='update_gcmId'),  # todo
    #url(r'^api/chat_rooms/$', views.chat_rooms, name='chat_rooms'),  # todo
    #url(r'^api/user/(?P<user_id>[0-9]+)/chats/$', views.user_chats, name='user_chats'),  # todo
    #url(r'^api/chat_room/(?P<chatRoom__pk>[0-9]+)/message/$', views.sendToTopic, name='sendToTopic'),  # todo
    #url(r'^api/chat/(?P<chat_id>[0-9]+)/message/$', views.send_message, name='send_message'),  # todo
    #url(r'^api/user/(?P<user_id>[0-9]+)/message/$', views.send_push, name='send_push'),  # todo
    #url(r'^api/users/message/$', views.send_multiplePush, name='send_multiplePush'),  # todo
    #url(r'^api/chat/(?P<chat_id>[0-9]+)/messages/$', views.chat_messages, name='chat_messages'),  # todo
]




