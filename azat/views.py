import csv
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from .models import Post, Image, Category, Order, OrderItem


def index(request):
    return render(request, 'azat/index.html', )


def post(request, post_id=""):
    if post_id:
        # Show a post
        post = Post.objects.get(pk=post_id)
        images = Image.objects.filter(post=post)

        return render(request, 'azat/post.html', {'post': post, 'images': images})


def user_posts(request, id=""):
    if id:
        # Show a profile
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404
        posts_list = Post.objects.filter(user=user.id)
        paginator = Paginator(posts_list, 8)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        images = []
        no_image_posts = []
        for post in posts_list:
            images.extend(list(Image.objects.filter(post=post).order_by('id')[:1]))
            if not Image.objects.filter(post=post):
                no_image_posts.append(post)

        return render(request, 'azat/user.html', {'user': user, 'posts': posts, 'images': images, 'no_image_posts': no_image_posts})


def category_posts(request, category_id=""):
    if category_id:
        # Show posts in category
        try:
            category = Category.objects.get(id=category_id)
            # Family is category with subcategories
            family = category.get_descendants(include_self=True)
        except Category.DoesNotExist:
            raise Http404
        posts_list = Post.objects.filter(category__in=family)
        paginator = Paginator(posts_list, 8)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)
        images = []
        no_image_posts = []
        for post in posts_list:
            images.extend(list(Image.objects.filter(post=post).order_by('id')[:1]))
            if not Image.objects.filter(post=post):
                no_image_posts.append(post)

        return render(request, 'azat/category.html', {'category': category, 'posts': posts, 'images': images, 'no_image_posts': no_image_posts})


def orders(request):
    orders_list = Order.objects.filter(status=1).order_by('-creation_date')[:1000]
    context = {'orders_list': orders_list}
    return render(request, 'azat/orders.html', context)


def carts(request, order_id):
    items = OrderItem.objects.filter(order__pk=order_id).order_by('-id')[:1000]
    context = {'carts_list': items}
    return render(request, 'azat/carts.html', context)


def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Номер заказа', 'Клиент', 'Id товара', 'Товар', 'Количество', 'Сумма', 'Дата', 'Статус'])
    orders_list = Order.objects.all().values_list('pk', 'owner', 'post', 'post', 'amount', 'sum', 'creation_date',
                                                  'status')
    for order in orders_list:
        writer.writerow(order)

    return response


def test(request):
    posts_list = Post.objects.all().order_by('-creation_date')  # [:100]
    # Get 1st image of each post and set no_image_post flag if no image found.
    images = []
    no_image_posts = []
    for post in posts_list:
        images.extend(list(Image.objects.filter(post=post).order_by('id')[:1]))
        if not Image.objects.filter(post=post):
            no_image_posts.append(post)

    paginator = Paginator(posts_list, 8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'azat/test.html',
                  {'next_url': '/',
                   'posts': posts, 'images': images, 'no_image_posts': no_image_posts})
