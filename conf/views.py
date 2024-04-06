from itertools import groupby
from operator import attrgetter

from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.shortcuts import redirect
from conf.models import Category, Product, Task
from django.shortcuts import render
from django.contrib import messages

from .forms import TaskForm, UserForm, RegisterForm
from .models import Cart


def main_page(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    search = request.GET.get("search", None)
    categories = Category.objects.annotate(count2=Count("product")).values('title', 'count2', 'id')
    pro = Product.objects.aggregate(procount=Count('id'))
    if search:
        products = Product.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
    else:
        products = Product.objects.all()
    context = {
        "categories": categories,
        "products": products,
        "pro": pro
    }
    return render(request, 'index.html', context)


def product(request, id):
    search = request.GET.get("search", None)
    categories = Category.objects.annotate(count2=Count("product")).values('title', 'count2', 'id')
    pro = Product.objects.aggregate(procount=Count('id'))
    if search:
        products = Product.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
    else:
        products = Product.objects.filter(category_id=id)

    context = {
        "categories": categories,
        "products": products,
        "pro": pro
    }
    return render(request, 'index.html', context)


def add_to_cart(request, id):
    if id:
        products = Cart.objects.filter(product_id=id)
        if products:
            product = products.first()
            product.count += 1
            product.save()
        else:
            Cart.objects.create(product_id=id, count=1, user=request.user)
    return redirect("/cart/")


def cart(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    carts = Cart.objects.filter(user=request.user).select_related('product')

    if request.method == "GET":
        context = {
            "carts": carts
        }

        if carts.exists():
            return render(request, 'cart.html', context)
        else:
            messages.error(request, "Корзина пуста. Нет товаров.")
            return render(request, 'cart.html')

    return render(request, 'cart.html')


def task_process(request):
    tasks = Task.objects.all().order_by('-id')
    tasks2 = Task.objects.all().annotate(registered_date=TruncDate('created_date')).values(
        'created_date', 'title')
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form = TaskForm()
    else:
        form = TaskForm()

    context = {
        "tasks": tasks,
        "task_form": form,
        "task2": tasks2
    }

    return render(request, 'task.html', context)


def auth(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Добро пожаловать")
                return redirect("/")
            else:
                messages.error(request, "Введите корректные данные")
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, "login.html", {"form": form})


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect("/login/")


def task_done(request, id):
    task = Task.objects.get(id=id)
    task.finished = True
    task.save()
    return redirect("/tasks/")


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    product.visit = product.visit + 1
    product.save()

    context = {
        "product": product
    }
    return render(request, 'detail.html', context)


