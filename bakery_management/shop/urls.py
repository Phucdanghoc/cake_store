from django.shortcuts import redirect, render
from django.urls import path
from django.conf.urls import handler404
from shop.views.auth.views import LoginView, logout_view
from shop.views.manager.order.views import OrderAPI, OrderActionAPI, OrderDetailView, OrderListView
from shop.views.manager.product.views import AddProductView, DeleteProductView, EditProductView, ExcelUploadView, ProductAPI, ProductListView
from shop.views.manager.promotion.views import PromotionCreateView, PromotionDeleteView, PromotionListView, PromotionUpdateView
from shop.views.manager.saler.views import DetailSalerView, ResetPasswordView, SalerCreateView, SalerDeleteView, SalerListView, SalerUpdateView
from shop.views.manager.statistics.views import ExportOrderStatisticsToExcelView, OrderStatisticsByDateView, OrderStatisticsByStatusView, OrderStatisticsFromToView, StatisticsView
from shop.views.manager.views import ManagerHomeView
from shop.views.saler.views import ChangePasswordView, SaleHomeView, SaleOrderView, SaleProductView, SalerDashboardView, SalerMakeOrderView, SalerOrderDetailView, SalerProfileView, UpdateProductAvailability


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
handler404 = custom_404

def custom_base(request, exception=None):
    return redirect('manager_home')

urlpatterns = [
    path('', custom_base, name='base'),
    path('login', LoginView.as_view(), name='login'),
    path('manager', ManagerHomeView.as_view(), name='manager_home'),
    path('saler', SaleHomeView.as_view(), name='sale_home'),
    path('logout', logout_view, name='logout'),
    path('manager/products', ProductListView.as_view(), name='product_list'),  # View list of products
    path('manager/add_product', AddProductView.as_view(), name='add_product'),  # Add a new product
    path('manager/add_product_excel', ExcelUploadView.as_view(), name='add_product_excel'),  # View details of a product
    path('manager/edit_product/<int:pk>', EditProductView.as_view(), name='edit_product'),  # Edit an existing product
    path('manager/delete_product/<int:pk>', DeleteProductView.as_view(), name='delete_product'),  # Delete a product
    path('manager/saler', SalerListView.as_view(), name='saler_list'),
    path('manager/saler/create', SalerCreateView.as_view(), name='saler_create'),
    path('manager/saler/<int:pk>', DetailSalerView.as_view(), name='saler_detail'),
    path('manager/edit_saler/<int:pk>', SalerUpdateView.as_view(), name='saler_update'),
    path('manager/delete_saler/<int:pk>', SalerDeleteView.as_view(), name='saler_delete'),
    path('manager/saler/reset_password/<int:pk>', ResetPasswordView.as_view(), name='saler_reset_password'),
    path('manager/statistics', StatisticsView.as_view(), name='statistics'),
    # path("manager/promotions/", PromotionListView.as_view(), name="promotion_list"),
    # path("manager/promotion/create", PromotionCreateView.as_view(), name="promotion_create"),
    # path("manager/edit_promotion/<int:pk>", PromotionUpdateView.as_view(), name="promotion_update"),
    # path("manager/delete_promotion/<int:pk>", PromotionDeleteView.as_view(), name="promotion_delete"),
    path('manager/orders', OrderListView.as_view(), name='order_list'),
    path('manager/orders/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    # Saler URLs
    path('saler/profile', SalerProfileView.as_view(), name='saler_profile'),
    path('saler/order', SaleOrderView.as_view(), name='saler_order'),
    path('saler/order/<int:pk>', SalerOrderDetailView.as_view(), name='saler_order_detail'),
    path('saler/product', SaleProductView.as_view(), name='saler_product'),
    path('saler/dashboard', SalerDashboardView.as_view(), name='saler_dashboard'),
    path('saler/make_order', SalerMakeOrderView.as_view(), name='saler_make_order'),
    path('saler/change_password', ChangePasswordView.as_view(), name='change_password'),
    #  API URLs
    path('api/statistics/order_by_date/', OrderStatisticsByDateView.as_view(), name='order_by_date'),
    path('api/statistics/order_from_to/', OrderStatisticsFromToView.as_view(), name='order_from_to'),
    path('api/statistics/order_status/', OrderStatisticsByStatusView.as_view(), name='order_status'),
    path('api/products/', ProductAPI.as_view(), name='order_status'),
    # path('api/promotion/<int:pk>/', ProductAPI.as_view(), name='order_status'),
    path('api/orders/', OrderAPI.as_view(), name='order_status'),
    path('api/product/availability/<int:product_id>/', UpdateProductAvailability.as_view(), name='product_availability'),
    path('api/orders/pay/<int:pk>/', OrderActionAPI.as_view(), name='order_payment'),
    path('api/orders/cancel/<int:pk>/', OrderActionAPI.as_view(), name='order_cancel'),
    path('api/statistics/export_excel/', ExportOrderStatisticsToExcelView.as_view(), name='order_export_excel'),
]
