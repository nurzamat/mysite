from django.conf.urls import url
from . import views, api_views

app_name = 'azat'
urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),  # root
    url(r'^test/', views.test, name='test'),  # test
    url(r'^user/(?P<id>\w{0,30})/$', views.user_posts, name='user_posts'),
    url(r'^post/(?P<post_id>\w{0,30})/$', views.post, name='post'),
    url(r'^category/(?P<category_id>\w{0,30})/$', views.category_posts, name='category_posts'),
    url(r'^orders/', views.orders, name='orders'),
    url(r'^carts/(?P<order_id>[0-9]+)$', views.carts, name='carts'),
    url(r'^export/csv/$', views.export_orders_csv, name='export_orders_csv'),
    #url(r'^search/', include('haystack.urls')),
    #url(r'^counter/ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
    #url(r'^identicon/', include(django_pydenticon.urls.get_patterns())),

    # API
    url(r'^api/categories/$', api_views.categories, name='categories'),
    url(r'^api/countries/$', api_views.countries, name='countries'),
    url(r'^api/regions/$', api_views.regions, name='regions'),
    url(r'^api/register/$', api_views.create_user, name='create_user'),
    url(r'^api/login/$', api_views.login, name='login'),
    url(r'^api/category/(?P<post_type>[0-9]+)/posts/$', api_views.posts, name='posts'),  # if type = 0 show all posts
    url(r'^api/user/(?P<user_id>[0-9]+)/posts/$', api_views.user_posts, name='api_user_posts'),
    url(r'^api/post/(?P<post_id>[0-9]+)/hitcount/$', api_views.post_hitcount, name='post_hitcount'),
    url(r'^api/posts/search/$', api_views.search_post, name='search_post'),  # if type = 0 search in all posts
    url(r'^api/posts/create/$', api_views.create_post, name='create_post'),
    url(r'^api/post/(?P<post_id>[0-9]+)/$', api_views.post_detail, name='post_detail'),
    url(r'^api/user/(?P<user_id>[0-9]+)/orders/$', api_views.user_orders, name='api_user_orders'),
    url(r'^api/orders/(?P<order_id>[0-9]+)/items/$', api_views.api_order_items, name='api_order_items'),
    url(r'^api/orders/create/$', api_views.create_order, name='api_create_order'),
    url(r'^api/orders/(?P<order_id>[0-9]+)/status/(?P<status>[0-9]+)$', api_views.update_order, name='api_update_order'),
    url(r'^api/order/(?P<order_id>[0-9]+)/item/add/$', api_views.add_item, name='api_add_item'),
    # url(r'^api/post/(?P<post_id>[0-9]+)/images/$', api_views.save_images, name='save_images'),  # todo
    # url(r'^api/user/(?P<user_id>[0-9]+)/profile/image/$', api_views.save_profile_image, name='save_profile_image'),  # todo
    # url(r'^api/post/(?P<post_id>[0-9]+)/$', api_views.update_post, name='update_post'),  # todo
    # url(r'^api/post/(?P<post_id>[0-9]+)/$', api_views.delete_post, name='delete_post'),  # todo
    # url(r'^api/user/(?P<user_id>[0-9]+)/profile/$', api_views.edit_profile, name='edit_profile'),  # todo
]
