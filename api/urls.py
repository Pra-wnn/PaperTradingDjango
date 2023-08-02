from django.urls import path
from . import views
from .views import *



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('',apiOverView, name='api-overview'),
    path('balance/',BalanceList,name='balance'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('password_reset/<uidb64>/<token>/',password_reset,name='password_reset'),
    path('password_reset_request/',request_password_reset,name='password_reset_request'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Balance CRUD operations
    # path('balances_create/', balance_create, name='balance-create'),
    path('balances/<int:pk>/', balance_detail, name='balance-detail'),
    path('balances/<int:pk>/update/', balance_update, name='balance-update'),
    # path('balances/<int:pk>/delete/', balance_delete, name='balance-delete'),

    # Expenditure CRUD operations
    path('expenditures_create/', expenditure_create, name='expenditure-create'),
    path('expenditures/<int:pk>/', expenditure_detail, name='expenditure-detail'),
    path('expenditures_list/<int:pk>/', expenditure_list, name='expenditure-list'),
    path('expenditures_update/', expenditure_update, name='expenditure-update'),
    path('expenditures/<int:pk>/delete/', expenditure_delete, name='expenditure-delete'),

    # Income CRUD operations
    path('income_create/', Income_create, name='Income-create'),
    path('income/<int:pk>/', Income_detail, name='Income-detail'),
    path('income_list/<int:pk>/', Income_list, name='Income-list'),
    path('income_update/', Income_update, name='Income-update'),
    path('income/<int:pk>/delete/', Income_delete, name='Income-delete'),

    # Debt CRUD operations
    path('debt_create/', Debt_create, name='Debt-create'),
    path('debt/<int:pk>/', Debt_detail, name='Debt-detail'),
    path('debt_list/<int:pk>/', Debt_list, name='Debt-list'),
    path('debt_update/', Debt_update, name='Debt_update'),
    path('debt/<int:pk>/delete/', Debt_delete, name='Debt-delete'),
    path('debt_move/', Debt_move_to_expense, name='Debt-move'),



    # Transaction CRUD operations
    path('transactions_create/', transaction_create, name='transaction-create'),
    path('transactions_history/', transaction_history, name='transaction-history'),
    path('users/search/', views.search_users, name='search_users'),
    path('transactions/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('transactions/<int:pk>/update/', transaction_update, name='transaction-update'),
    path('transactions/<int:pk>/delete/', transaction_delete, name='transaction-delete'),

    path('stocks/', stock_api, name='stocks_api'),
    path('stocks_info/<str:stock_symbol>/', stock_info, name='stocks_info'),
    path('buy_stocks/',buy_stock, name='stocks_buy'),
    path('sell_stocks/',sell_stock, name='stocks_sell'),
    path('portfolio/',get_portfolio,name='get_portfolio'),
    path('stocks_price/',getStock_Price,name='get_stock_price'),
    path('stock_balance/<int:pk>/',stock_balance,name='get_stock_balance'),
    path('stock_change/',getStock_Change,name='stock_change'),
    path('yes_change/',yes_Change,name='stocks_change'),
    path('wishlist/<int:pk>/',Wishlist_display,name='wishlist'),
    path('wishlist_create/', Wishlist_create, name='wishlist_create'),
    path('wishlist_update/', Wishlist_update, name='wishlist_update'),
    path('wishlist/<int:pk>/delete/', Wishlist_delete, name='wishlist-delete'),


    path('export_data/<int:pk>/', export_user_data, name='export_financial_data'),
    path('export_pdf/<int:user_id>/', export_user_data_to_pdf, name='export_financial_pdf'),
    path('export_pdfs/<int:user_id>/', export_user_datapdf, name='export_financial_pdfs'),
    path('backup/<int:user_id>/<str:file_name>/', views.backup_detail, name='backup_detail'),
    path('backup_list/<int:user_id>/', views.backup_list, name='backup_list'),


    path('google-drive-callback/', google_drive_callback, name='google_drive_callback'),
    path('authenticate-user/', authenticate_user, name='authenticate_user'),
    path('init_user/', initiate_google_drive_auth, name='init_authenticate_user'),
    path('upload-to-google-drive/', upload_to_google_drive, name='upload_to_google_drive'),


    path('get_csv/<str:stock_symbol>/', get_stock_data, name='get_stock_data'),
    path('send_sms/',send_sms, name='send_sms'),



]