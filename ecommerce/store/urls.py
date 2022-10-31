from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('product/<int:id>', views.product_view, name='product-view'),
	path('update_item/', views.update_item, name='update_item'),
	path('process_order/', views.process_order, name='process_order'),
	path('order_list/', views.order_list, name = 'order_list'),

	path('user/company/', views.admin_view_product, name='company.product.list'),
	path('user/company/addproduct', views.adminUser, name = "admin.company"),
	path('user/company/edit/<int:id>', views.admin_edit_product, name = 'product-edit'),
	path('user/company/delete/<int:id>', views.product_delete, name = 'product-delete'),


	path('user/login', views.login_user, name='login'),
	path('user/logout', views.logout_user, name='logout'),
	path('user/register', views.register, name='register')

]