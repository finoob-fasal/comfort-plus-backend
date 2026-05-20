from django.urls import path
from AdminApp import views

urlpatterns= [
    path('login/', views.admin_login, name='admin_login'),

    path('view_users/', views.view_users, name='view_users'),

    path('add_service/', views.add_service, name='add_service'),
    path('view_services/', views.view_services, name='view_services'),
    path('v_single_services/<int:id>', views.v_single_services, name='v_single_services'),
    path('edit_service/<int:id>', views.edit_service, name='edit_service'),
    path('delete_service/<int:id>', views.delete_service, name='delete_service'),

    path('view_u_order/', views.view_u_order, name='view_u_order'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('view_user_orders/<int:id>', views.view_user_orders, name='view_user_orders'),
    path('view_user_order/<int:id>', views.view_user_order, name='view_user_order'),

    path('add_staff/', views.add_staff, name='add_staff'),
    path('view_all_staff/', views.view_all_staff, name='view_all_staff'),
    path('view_single_staff/<int:id>', views.view_single_staff, name='view_single_staff'),
    path('remove_staff/<int:id>', views.remove_staff, name='remove_staff'),
    path('edit_staff/<int:id>/', views.edit_staff, name='edit_staff'),

    path('add_item/<int:id>', views.add_item, name='add_item'),
    path('view_items', views.view_items, name='view_items'),
    path('view_single_item/<int:id>', views.view_single_item, name='view_single_item'),
    path('edit_service_item/<int:id>', views.edit_service_item, name='edit_service_item'),
    path('delete_service_item/<int:id>', views.delete_service_item, name='delete_service_item'),

]