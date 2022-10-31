
import json
import datetime
from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm, AddProduct
from .models import Customer, Order, OrderItem, Product, ShippingAddress
# Create your views here.

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		print(username, password)
		user = authenticate(request, username= username, password = password)
		print(user)
		if user and user.is_staff is False:
			login(request, user)
			return redirect('store')
		elif user and user.is_staff is True:
			login(request, user)
			return redirect('company.product.list')
		else:
			return HttpResponse('Credentials do not match')
	else:
		form = UserLoginForm
		return render(request, 'authentication/login.html',context={'form':form} )

def logout_user(request):
	logout(request)
	return redirect('login')


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		print(form)
		if form.is_valid():
			print(form)
			form.save()
			return redirect('login')
		else:
			return redirect('register')
	else:
		form = UserRegisterForm
		return render(request, 'authentication/register.html',context={'form':form} )


def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete = False)
		cartItems = order.get_cart_items
	else:
		cartItems = 0
	product = Product.objects.all()
	context = {
		'products': product,
		'cartItems' : cartItems
	}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		redirect('login')
	context = {'items':items, 'order': order, 'cartItems' : cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		items = order.orderitem_set.all()
	else:
		redirect('login')
	context = {'items':items, 'order': order}
	return render(request, 'store/checkout.html', context)

def update_item(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	customer = request.user.customer
	product = Product.objects.get(id = productId)
	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	orderItem, created = OrderItem.objects.get_or_create(order= order, product = product)

	if action == 'add':
		orderItem.quantity = orderItem.quantity + 1
	elif action == 'remove':
		orderItem.quantity = orderItem.quantity - 1
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Successs', safe= False)

def order_list(request):
	if not request.user.is_staff:
		customer = request.user.customer
		orders = Order.objects.filter(customer = customer, complete = True)
		orderitems = []
		for order in orders:
			orderitems += order.orderitem_set.all()
	else:
		orders = Order.objects.filter(complete = True).all()
		orderitems = []
		for order in orders:
			orderitems += order.orderitem_set.all()
	context ={'orderitems': orderitems}
	return render(request, 'store/order.html', context)


@login_required(login_url='login')
def process_order(request):
	data = json.loads(request.body)
	shipping_form = data['shipping']
	total = float(data['form']['total'])
	customer = request.user.customer
	order,created = Order.objects.get_or_create(customer = customer, complete = False)
	transaction_id = datetime.datetime.now().timestamp()
	order.transaction_id = transaction_id
	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = shipping_form['address'],
			city = shipping_form['city'],
			state = shipping_form['state'],
			zipcode = shipping_form['city']
		)
	return JsonResponse('Payment submitted..', safe=False)

def product_view(request, id):
	product = Product.objects.get(id = id)
	context = {
		'product':product
	}
	return render(request,'store/product.html', context)

@login_required(login_url='login')
def adminUser(request):
	if request.method == 'POST':
		form = AddProduct(request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			return redirect('company.product.list')

	form = AddProduct
	context = {
		'form':form
	}
	return render(request, 'admin/company.html', context)


@login_required(login_url='login')
def admin_view_product(request):
	product = Product.objects.all()
	context = {
		'products': product
	}
	return render(request, 'admin/productView.html', context)

@login_required(login_url='login')
def admin_edit_product(request, id):
	if request.method == 'POST':
		product = Product.objects.get(id = request.POST.get('id'))
		productForm = AddProduct(request.POST, instance= product, files= request.FILES)
		if productForm.is_valid():
			productForm.save()
		return redirect('company.product.list')
	else:
		product = Product.objects.get(id = id)
		
		context = {
			'product':product
		}
		return render(request, 'admin/editProduct.html', context)

@login_required(login_url='login')
def product_delete(request, id):
	product = Product.objects.get(id = id)
	product.delete()
	return redirect('company.product.list')