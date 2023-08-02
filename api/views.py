from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate

import jwt
from .serializers import *
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Sum,Value
from django.db.models.functions import Coalesce
from django.conf import settings
from django.urls import reverse

from django.shortcuts import get_object_or_404
from django.http import FileResponse,HttpResponse,HttpRequest
from django.core.exceptions import PermissionDenied


from rest_framework import status
# Create your views here.



#Reminder: Authorization ie specific user is left 
# @permission_classes([IsAuthenticated])
# keepping it above is useless has to be above func not top of ceorator
@api_view(['GET'])
def apiOverView(request):
    api_urls = {
        'list':'/transaction_list/',
        'Balance':'/Balance/',
        'Expenditure':'/Expenditure/'
    }

    return Response((api_urls))

# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def BalanceList(request):
    balance = Balance.objects.filter(user=request.user)
    serializer = BalanceSerializer(balance, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')

    if not username or not password or not email:
        return Response({'error': 'Please provide username and password and email'}, status=status.HTTP_400_BAD_REQUEST)

    # user, created = User.objects.get_or_create(username=username)
    # if created:
    #     user.set_password(password)
    #     user.email = email #assign email to user
    #     user.save()
       
    # else:
    #     return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)


    if len(password) < 8:
        return Response({'error': 'Password should be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=username)
        return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)
    except User.DoesNotExist:
        pass

    try:
        User.objects.get(email=email)
        return Response({'error': 'Email already exists'}, status=status.HTTP_409_CONFLICT)
    except User.DoesNotExist:
        pass
    if phone_number:
        try:
            User.objects.get(phone_number=phone_number)
            return Response({'error': 'Phone number already exists'}, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            pass

    user = User(username=username)
    user.set_password(password)
    user.email = email
    if phone_number:
        user.phone_number = phone_number
    user.save()

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def register_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
    
#     if not username or not password:
#         return Response({'error': 'Both username and password are required'})
    
#     try:
#         # User from default django models
#         user = User.objects.create_user(username=username, password=password)

#         payload = {'username':username}

#         token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')

#         login(request, user)
#         return Response({'message': 'User registered successfully','token': token})
#     except IntegrityError:
#         return Response({'error': 'Username already exists'})



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    # access_token = str(refresh.access_token)

    access_token = AccessToken.for_user(user)
    # Add custom claims to the access token payload
    access_token['username'] = user.username
    access_token['email'] = user.email


    # Create a new dictionary to hold the token payload
    # payload = {
    #     'access_token': access_token,
    #     'username': user.username,
    #     'email': user.email,
  
    
    # }
    

    return Response({'refresh': str(refresh), 'access': str(access_token)})


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     if not username or not password:
#         return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.create_user(username=username, password=password)
#     except IntegrityError:
#         return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)

#     if user:
#         refresh = RefreshToken.for_user(user)
#         return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
#     else:
#         return Response({'error': 'Unable to create user'}, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework_simplejwt.views import TokenObtainPairView

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     if not username or not password:
#         return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.create_user(username=username, password=password)
#     except IntegrityError:
#         return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)

#     if user:
#         token_obtain_pair_view = CustomTokenObtainPairView.as_view()
#         response = token_obtain_pair_view(request=request._request)
#         return response
#     else:
#         return Response({'error': 'Unable to create user'}, status=status.HTTP_400_BAD_REQUEST)

# Balance CRUD operations
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def balance_create(request):
#     user = request.user
#     serializer = BalanceSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=user)
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if not user:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    base_url = "http://localhost:3000" 

    password_reset_link = f"{base_url}/reset-password/{uid}/{token}"

    mail_subject = 'Reset your password'
    # message = render_to_string(password_reset_link, {
    #     'user': user,
    #     'domain': get_current_site(request).domain,
    #     'uid': uid,
    #     'token': token,
    # })

    
    
    # send_mail(mail_subject, message, 'noreply@mywebsite.com', [user.email])
    send_mail(mail_subject, password_reset_link, 'settings.EMAIL_HOST_USER', [user.email],
        fail_silently=False)
  



    return Response({'status': 'Password reset link was sent to your email address'})

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request, uidb64, token):
    password = request.data.get('password')
    if not password:
        return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'status': 'Password reset was successful'})
        else:
            return Response({'error': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def balance_detail(request, pk):
    try:
        balance = Balance.objects.get(pk=pk)
    except Balance.DoesNotExist:
        return Response(status=404)
    
    if balance.user != request.user:
        return Response({'error': 'You do not have permission to update this balance'}, status=status.HTTP_403_FORBIDDEN)

    serializer = BalanceSerializer(balance)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def balance_update(request, pk):
    try:
        balance = Balance.objects.get(pk=pk)
    except Balance.DoesNotExist:
        return Response(status=404)
    
    if balance.user != request.user:
        return Response({'error': 'You do not have permission to update this balance'}, status=status.HTTP_403_FORBIDDEN)


    serializer = BalanceSerializer(balance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# @permission_classes([IsAuthenticated])
# @api_view(['DELETE'])
# def balance_delete(request, pk):
#     try:
#         balance = Balance.objects.get(pk=pk)
#     except Balance.DoesNotExist:
#         return Response(status=404)

#     balance.delete()
#     return Response(status=204)


# Expenditure CRUD operations


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def expenditure_create(request):
    serializer = ExpenseSerializer(data=request.data,context={'request': request})
    # context={'request': request} add this too post data
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# @permission_classes([IsAuthenticated])
# @api_view(['GET'])
# def expenditure_detail(request, pk):
#     try:
#         # expenditure = Expenditure.objects.get(pk=pk)
#         # expenditures = Expenditure.objects.filter(user__id=pk)
#         expenditures = Expenditure.objects.filter(user__id=pk).aggregate(total=Sum('amount'))
#     except Expenditure.DoesNotExist:
#         return Response(status=404)

#     serializer = ExpenseSerializer(expenditures,many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expenditure_detail(request, pk):
    expenditures = Expenditure.objects.filter(user__id=pk).aggregate(total=Coalesce(Sum('amount'), Decimal('0.00')))
    return Response(expenditures)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expenditure_list(request, pk):
    expenditures = Expenditure.objects.filter(user__id=pk)
    # expenditure_listv = []
    # for exp in expenditures:
    #     expenditure_listv.append({
    #         'amount':exp.amount,
    #         'expenditure_type':exp.expenditure_type,
    #     })
    serializer = ExpenseSerializer(expenditures, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def expenditure_update(request):
    #get the id not the pk else it iwll look fro pk as the data id in db
    expense_id = request.data.get('id')
    try:
        expense = Expenditure.objects.get(pk=expense_id)
    except Expenditure.DoesNotExist:
        raise Http404("Expenditure not found")

    serializer = ExpenseSerializer(expense, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)







@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def expenditure_delete(request, pk):
    try:
        expenditure = Expenditure.objects.get(pk=pk)
    except Expenditure.DoesNotExist:
        return Response(status=404)

    expenditure.delete()
    return Response(status=204)

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def Debt_delete(request, pk):
#     try:
#         debt = Debt.objects.get(pk=pk)
#     except Debt.DoesNotExist:
#         return Response(status=404)

#     debt.delete()
#     return Response(status=204)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Income_detail(request, pk):
    Incomes = Income.objects.filter(user__id=pk).aggregate(total=Coalesce(Sum('amount'), Decimal('0.00')))
    return Response(Incomes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Income_list(request, pk):
    Incomes = Income.objects.filter(user__id=pk)
    # Income_listv = []
    # for exp in Incomes:
    #     Income_listv.append({
    #         'amount':exp.amount,
    #         'Income_type':exp.Income_type,
    #     })
    serializer = IncomeSerializer(Incomes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Income_create(request):
    serializer = IncomeSerializer(data=request.data,context={'request': request})
    # context={'request': request} add this too post data
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Income_update(request):
    #get the id not the pk else it iwll look fro pk as the data id in db
    income_id = request.data.get('id')
    try:
        income = Income.objects.get(pk=income_id)
    except Income.DoesNotExist:
        raise Http404("Income not found")
        

    serializer = IncomeSerializer(income, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Income_delete(request, pk):
    try:
        income = Income.objects.get(pk=pk)
    except Income.DoesNotExist:
        return Response(status=404)

    income.delete()
    return Response(status=204)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Debt_detail(request, pk):
    Debts = Debt.objects.filter(user__id=pk).aggregate(total=Coalesce(Sum('amount'), Decimal('0.00')))
    return Response(Debts)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Debt_list(request, pk):
    Debts = Debt.objects.filter(user__id=pk)
    serializer = DebtSerializer(Debts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Debt_create(request):
    serializer = DebtSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

from django.http import Http404


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Debt_update(request):

    #get the id not the pk else it iwll look fro pk as the data id in db
    debt_id = request.data.get('id')
    try:
        debt = Debt.objects.get(pk=debt_id)
    except Debt.DoesNotExist:
        raise Http404("Debt not found")

    serializer = DebtSerializer(debt, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Debt_delete(request, pk):
    try:
        debt = Debt.objects.get(pk=pk)
    except Debt.DoesNotExist:
        return Response(status=404)

    debt.delete()
    return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Debt_move_to_expense(request):
    debt_id = request.data.get('id')
    try:
        debt = Debt.objects.get(pk=debt_id)

    except Debt.DoesNotExist:
        return Response(status=404)
    
    Expense = Expenditure(
        user=debt.user,
        expenditure_type=debt.debt_type,
        amount=debt.amount,
        created_at=debt.created_at,
    )
    Expense.save()
    debt.delete()
    # user = request.user
    return Response(status=204)




# Transaction CRUD operations
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transaction_create(request):
    serializer = TransactionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=404)

    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def transaction_update(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=404)

    serializer = TransactionSerializer(transaction, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def transaction_delete(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=404)

    transaction.delete()
    return Response(status=204)
    
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    transactions = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    transaction_data = []

    for transaction in transactions:
        transaction_data.append({
            'sender': transaction.sender.username,
            'receiver': transaction.receiver.username,
            'amount': transaction.amount,
            'created_at': transaction.created_at,
        })

    return JsonResponse({'transactions': transaction_data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_users(request):
    username = request.data.get('username', '')  # Retrieve the search query parameter
    # gets the data
    # Check if user with the provided username exists
    user_exists = User.objects.filter(username=username).exists()

    response_data = {
        'exists': user_exists
    }

    return JsonResponse(response_data)


@api_view(['GET'])
def stock_info(request, stock_symbol):
    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/misc/companies/'

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        # Find the stock with the given symbol
        filtered_stocks = [stock for stock in data if stock['symbol'] == stock_symbol]

        if filtered_stocks:
            stock_info = filtered_stocks[0]  # Get the first matching stock
            return JsonResponse(stock_info)
        else:
            return JsonResponse({'error': 'Stock not found'}, status=404)
    except requests.exceptions.RequestException as e:
        # Handle any exceptions or errors
        return JsonResponse({'error': str(e)})

@api_view(['GET'])
def stock_api(request):
    
    # url = 'https://www.nepalipaisa.com/api/GetStockLive'
    # wishlist_stocks = Wishlist.objects.filter(user=request.user)

    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/stocks/live'

    try:
        response = requests.get(url,headers=headers)

        data = response.json() # Corrected here

        # Extract specific fields from each item in the response data
        extracted_data = []
        # for item in data[:20]:  # Limit to the top 20 companies
        for item in data:
            extracted_item = {
                'stockSymbol': item['stockSymbol'],
                'closingPrice': item['closingPrice'],
                'companyName': item['companyName'],
                'amount': item['amount'],
                'volume': item['volume'],
                'previousClosing': item['previousClosing'],
                'maxPrice': item['maxPrice'],
                'minPrice': item['minPrice'],
                'openingPrice': item['openingPrice'],
                'percentChange': item['percentChange'],
                'tradeDate' : item['tradeDate']
            }
            extracted_data.append(extracted_item)

        #  Return the extracted data as a JSON response
        print(JsonResponse(extracted_data,safe=False))
        return Response(extracted_data)
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions or errors
        return JsonResponse({'error': str(e)})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_stock(request):
    stock_symbol = request.data.get('stockSymbol')
    quantity = int(request.data.get('quantity'))

    # Validate the input data
    if not all([stock_symbol, quantity])  or not str(quantity).isdigit():
        return Response({'error': 'Incomplete data provided.'}, status=400)

    quantity = int(quantity)

    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/stocks/live'

    # Fetch the stock data from your real-time database or API
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        return Response({'error': 'Failed to fetch stock data.'}, status=500)

    stock_data = response.json()

    # Find the matching stock based on the stock symbol
    filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == stock_symbol), None)
    if not filtered_stock:
        return Response({'error': 'Stock symbol not found.'}, status=404)

    closing_price = Decimal(filtered_stock.get('closingPrice'))

    buy_price = closing_price * quantity

    # Check if user already has a portfolio entry for this stock_symbol
    portfolio_history, created = Portfolio_History.objects.get_or_create(
        user=request.user, 
        stock_symbol=stock_symbol,
        defaults={'quantity':0,'stock_balance':0,'stock_sold':0})

    

    if created:
        # If the portfolio was just created, the quantity is just the quantity bought
        portfolio_history.quantity = quantity
        portfolio_history.stock_balance = buy_price

    else:
        # If the portfolio already existed, add the quantity bought to the current quantity
        portfolio_history.quantity += quantity
        portfolio_history.stock_balance += buy_price


    # Save the portfolio_history object
    portfolio_history.save()

    # Create a new portfolio object to record this transaction
    Portfolio.objects.create(
        user=request.user,
        stock_symbol=stock_symbol,
        portfolio_history=portfolio_history,
        quantity=quantity,
        trade_type="buy",
        buy_price=buy_price,
        sell_price=0,  # Set the initial sell price to 0
    )

    return Response({'success': 'Stock bought successfully.'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell_stock(request):
    stock_symbol = request.data.get('stockSymbol')
    quantity = int(request.data.get('quantity'))
    
    # Validate the input data
    if not all([stock_symbol, quantity]):
        return Response({'error': 'Incomplete data provided.'}, status=400)
    if quantity <= 0:
        return Response({'error': 'Quantity must be a positive integer.'}, status=400)


    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/stocks/live'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return Response({'error': 'Failed to fetch stock data.'}, status=500)

    stock_data = response.json()
    filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == stock_symbol), None)
    if not filtered_stock:
        return Response({'error': 'Stock symbol not found.'}, status=404)

    closing_price = Decimal(filtered_stock.get('closingPrice'))
    sell_price = closing_price * quantity
    portfolio_history, created = Portfolio_History.objects.get_or_create(
        user=request.user, 
        stock_symbol=stock_symbol, 
        defaults={'quantity': 0,'stock_balance': 0,'stock_sold':0}
    )

    if created or portfolio_history.quantity < quantity:
        return Response({'error': 'Not enough stocks to sell.'}, status=400)

    # Deduct the quantity sold from the portfolio_history entry and save it
    portfolio_history.quantity -= quantity
    portfolio_history.stock_balance -= sell_price
    portfolio_history.stock_sold += sell_price

    portfolio_history.save()
     
    user = request.user

    user.balance.amount += sell_price
    user.balance.save()

    # Create a new portfolio entry to record this transaction
    Portfolio.objects.create(
        user=request.user,
        stock_symbol=stock_symbol,
        portfolio_history=portfolio_history,
        quantity=quantity,
        trade_type="sell",
        buy_price=0,
        sell_price=sell_price,  
    )


  
    total_stocks = f"{stock_symbol}quantity{quantity}"
    Income.objects.create(
        user=request.user,
        income_type=total_stocks,
        amount=sell_price
    )
    

    # user = request.user
    return Response(status=204)

    return Response({'success': 'Stock sold successfully.'}, status=200)


# Auhtoriztion is lfet to add
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_portfolio(request):
    # Get the portfolio history for the logged in user
    portfolio_histories = Portfolio_History.objects.filter(user=request.user)

    # Transform the data into a format suitable for the response
    data = []
    for portfolio_history in portfolio_histories:
        trades = Portfolio.objects.filter(portfolio_history=portfolio_history)
        trades_data = [{'trade_type': trade.trade_type, 'quantity': trade.quantity, 
                        'buy_price': str(trade.buy_price), 'sell_price': str(trade.sell_price), 
                        'created_at': trade.created_at.strftime('%Y-%m-%d %H:%M:%S')} 
                        for trade in trades]

        data.append({
            'stock_symbol': portfolio_history.stock_symbol,
            'quantity': portfolio_history.quantity,
            'stock_balance' :portfolio_history.stock_balance,
            'stock_sold': portfolio_history.stock_sold,
            'trades': trades_data
        })

    return Response(data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_balance(request, pk):
    stock_balance =Portfolio_History.objects.filter(user__id=pk).aggregate(total=Coalesce(Sum('stock_balance'), Decimal('0.00')))
    return Response(stock_balance)

# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def getStock_Price(request):
    stock_symbol = request.data.get('stockSymbol')


    # Validate the input data
    if not all([stock_symbol]):
        return Response({'error': 'Incomplete data provided.'}, status=400)


    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/stocks/live'
    # Fetch the stock data from your real-time database or API
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        return Response({'error': 'Failed to fetch stock data.'}, status=500)

    stock_data = response.json()

    # Find the matching stock based on the stock symbol
    filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == stock_symbol), None)
    if not filtered_stock:
        return Response({'error': 'Stock symbol not found.'}, status=404)

    closing_price = Decimal(filtered_stock.get('closingPrice'))

import json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStock_Change(request):
    # stock_symbol = request.data.get('stockSymbol')

    # watchlist_stock = "AHL"

    # Validate the input data
    # if not all([stock_symbol]):
    #     return Response({'error': 'Incomplete data provided.'}, status=400)

    wishlist_stocks = Wishlist.objects.filter(user=request.user)

    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/stocks/live'
    # Fetch the stock data from your real-time database or API
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        return Response({'error': 'Failed to fetch stock data.'}, status=500)

    stock_data = response.json()


    # # Find the matching stock based on the stock symbol
    # filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == wishlist_stocks.stock_symbol), None)
    # if not filtered_stock:
    #     return Response({'error': 'Stock symbol not found.'}, status=404)

    exceeded_stocks = []


    for wishlist_stock in wishlist_stocks:
        filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == wishlist_stock.stock_symbol), None)
        if not filtered_stock:
            continue  # Skip to next wishlist_stock if the current one is not found

        closing_price = Decimal(filtered_stock.get('closingPrice'))
        # closing_price += 5
        if closing_price >= wishlist_stock.alert_price:
            # Add stock symbol and closing price to the exceeded_stocks list
            exceeded_stocks.append((wishlist_stock.stock_symbol, format(closing_price, '.2f')))

    if exceeded_stocks:

        user = request.user
        phone_number = user.phone_number
        email = user.email
        send_mail('SYSTEM ALERT #1',#title
        f"Stocks that exceeded alert price: {exceeded_stocks}",#message
        'settings.EMAIL_HOST_USER',
        [email],
        fail_silently=False)
        msg = str(exceeded_stocks)
        # if phone_number:
        #     send_sms(request,msg,phone_number)
        #     notification = f'check phone {phone_number}'
        if phone_number:
            http_request = HttpRequest()  # Create an instance of HttpRequest
            http_request.method = request.method  # Set the method
            http_request.GET = request.GET  # Set the GET parameters
            http_request.POST = request.POST  # Set the POST data
            # Copy other relevant attributes as needed

            response = send_sms(http_request, msg, phone_number)
            if response.status_code == 200:
                notification = 'Check phone'
            # Handle successful SMS sending
            else:
                notification = f'sms unavailable'

            # Handle failed SMS sending
                    
    
        else:
            notification = 'no phone_number exists for sms services'


      
        return Response({'message': f'Stocks that exceeded alert price: {exceeded_stocks} & {notification} & mail'}, status=200)
    
      
    return Response({'closing_price':closing_price},status=200)



# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def send_sms(request,msg,phone_number):
    service_plam_id = "SERVICE_PLAN_ID"
    access_token = "API_TOKEN"

    from_ = "phone_number"
  


   

    headers = {
        "Authorization":f"Bearer {access_token}",
        "Content-Type":"application/json"
    }

    payload= {
        "from":from_,
        "to":[phone_number],
        "body": msg
    }
    response=requests.post(
       f"https://sms.api.sinch.com/xms/v1/{service_plam_id}/batches",
        headers=headers,
        data=json.dumps(payload) )
    if response.status_code == 201:
        return HttpResponse('SMS sent successfully')
    else:
        return HttpResponse('Failed to send SMS', status=response.status_code)

        
        
  




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Wishlist_display(request,pk):
    try:
        wishlist = Wishlist.objects.filter(user__id=pk)
    except Wishlist.DoesNotExist:
        return Response(status=404)

    serializer = WishlistSerializer(wishlist, many=True)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Wishlist_create(request):
    serializer = WishlistSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Wishlist_update(request):

    #get the id not the pk else it iwll look fro pk as the data id in db
    wishlist_id = request.data.get('id')
    try:
        wishlist = Wishlist.objects.get(pk=wishlist_id)
    except Wishlist.DoesNotExist:
        raise Http404("Wishlist not found")

    serializer = WishlistSerializer(wishlist, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Wishlist_delete(request, pk):
    try:
        wishlist = Wishlist.objects.get(pk=pk)
    except Wishlist.DoesNotExist:
        return Response(status=404)

    wishlist.delete()
    return Response(status=204)

from django.core.mail import send_mail




from django.http import JsonResponse,HttpResponse
from django.core import serializers

@api_view(['GET'])
def export_user_data(request, pk):
    user = User.objects.get(id=pk)
    balance = Balance.objects.get(user=user)
    expenditures = Expenditure.objects.filter(user=user)
    incomes = Income.objects.filter(user=user)
    transactions = Transaction.objects.filter(sender=user)
    portfolio_histories = Portfolio_History.objects.filter(user=user)
    portfolios = Portfolio.objects.filter(user=user)
    wishlists = Wishlist.objects.filter(user=user)

    user_data = {
        'user': {
            'username': user.username,
            'email': user.email,
            # Add other User fields you want to export
        },
        'balance': str(balance.amount),
        'expenditures': list(expenditures.values()),
        'incomes': list(incomes.values()),
        'transactions': list(transactions.values()),
        'portfolio_histories': list(portfolio_histories.values()),
        'portfolios': list(portfolios.values()),
        'wishlists': list(wishlists.values()),
    }
    return JsonResponse(user_data)



from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import io
import calendar
from datetime import datetime

@api_view(['GET'])
def export_user_data_to_pdf(request, user_id):
    # Fetch your data here...
    user = User.objects.get(id=user_id)
    balance = Balance.objects.get(user=user)
    expenditures = Expenditure.objects.filter(user=user)
    incomes = Income.objects.filter(user=user)
    transactions = Transaction.objects.filter(sender=user)
    # Include more if you have more models related to user...

    data = [
        ['Username', 'Email', 'Balance'],
        [user.username, user.email, balance.amount],
        ['Expenditures'],
        ['Type', 'Amount', 'Created At']
    ]

    for expenditure in expenditures:
        data.append([expenditure.expenditure_type, expenditure.amount, expenditure.created_at])

    data.append(['Incomes'])
    data.append(['Type', 'Amount', 'Created At'])
    
    for income in incomes:
        data.append([income.income_type, income.amount, income.created_at])

    data.append(['Transactions'])
    data.append(['Receiver', 'Amount', 'Created At'])

    for transaction in transactions:
        data.append([transaction.receiver.username, transaction.amount, transaction.created_at])

    # Include more data according to your models...

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Create a table with the data and add it to the document
    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])

    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.bisque
        else:
            bc = colors.beige

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    elements = []
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    #Add datetime name calendar
    now = datetime.now()
    month_word = calendar.month_name[now.month]
    file_name = f'user_data_{user_id}_{month_word.lower()}_{now.year}.pdf'


    # Generate the link to the backup file
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    #CHanges from here
    file_path = f'api/backup/{file_name}'
    with open(file_path, 'wb') as file:
        file.write(pdf)
    #till here
    buffer.close()

    # backup_link = reverse('backup_detail', args=[user_id]) #this change too 

    #gmail part
    # Authenticate the user and obtain their credentials
    user_credentials = authenticate_user()

    # Upload the PDF to the user's Google Drive
    drive_file_id = upload_to_google_drive(file_path, file_name, user_credentials)
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename=user_data_{user_id}.pdf'
    # return response

    #gmail part
    backup_link = f'https://drive.google.com/file/d/{drive_file_id}/view?usp=sharing'
    return HttpResponse(f'Backup created. Access your backup in Google Drive: <a href="{backup_link}">Open Backup</a>')

    # return HttpResponse(f'Backup created. Download link: <a href="{backup_link}">Download Backup</a>')

@api_view(['GET'])
def export_user_datapdf(request, user_id):
    # Fetch your data here...
    user = User.objects.get(id=user_id)
    balance = Balance.objects.get(user=user)
    expenditures = Expenditure.objects.filter(user=user)
    incomes = Income.objects.filter(user=user)
    transactions = Transaction.objects.filter(sender=user)
    # Include more if you have more models related to user...

    data = [
        ['Username', 'Email', 'Balance'],
        [user.username, user.email, balance.amount],
        ['Expenditures'],
        ['Type', 'Amount', 'Created At']
    ]

    for expenditure in expenditures:
        data.append([expenditure.expenditure_type, expenditure.amount, expenditure.created_at])

    data.append(['Incomes'])
    data.append(['Type', 'Amount', 'Created At'])
    
    for income in incomes:
        data.append([income.income_type, income.amount, income.created_at])

    data.append(['Transactions'])
    data.append(['Receiver', 'Amount', 'Created At'])

    for transaction in transactions:
        data.append([transaction.receiver.username, transaction.amount, transaction.created_at])

    # Include more data according to your models...

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Create a table with the data and add it to the document
    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])

    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.bisque
        else:
            bc = colors.beige

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table.setStyle(ts)

    elements = []
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    #Add datetime name calendar
    now = datetime.now()
    data_date = now.strftime("%Y-%m-%d %H-%M-%S")
    date_new = str(data_date)
    month_word = calendar.month_name[now.month]
    file_name = f'user_data_{user_id}_{month_word.lower()}_{now.year}{date_new}.pdf'


    # Generate the link to the backup file
    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    #CHanges from here
    file_path = f'api/backup/{file_name}'
    with open(file_path, 'wb') as file:
        file.write(pdf)
    #till here
    buffer.close()

    # backup_link = reverse('backup_detail', args=[user_id]) #this change too 
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename=user_data_{user_id}.pdf'
    # return response
    # return HttpResponse(f'Backup created. Download link: <a href="{backup_link}">Download Backup</a>')
    return HttpResponse('backup created')


from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.core.exceptions import PermissionDenied

@api_view(['GET'])
def backup_detail(request, user_id,file_name):

    # if user_id != request.user.id:
    #     raise PermissionDenied

    # CHange here who can see the PDF

    file_path = f'api/backup/{file_name}'
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


    # <a href="{% url 'backup_detail' user_id=user.id %}">Download Backup</a>


import os

# ...


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def backup_list(request, user_id):
    backup_folder = 'api/backup/'  # Update with your backup folder path
    backup_links = []

    for filename in os.listdir(backup_folder):
        if filename.startswith(f'user_data_{user_id}'):
            file_path = os.path.join(backup_folder, filename)
            backup_link = reverse('backup_detail', args=[user_id,filename])
            backup_links.append({'file_name': filename, 'backup_link': backup_link})

    context = {'backup_links': backup_links}
    return JsonResponse(context)




@api_view(['GET'])
def backup_detail(request, user_id,file_name):

    # if user_id != request.user.id:
    #     raise PermissionDenied

    # CHange here who can see the PDF

    file_path = f'api/backup/{file_name}'
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


    # <a href="{% url 'backup_detail' user_id=user.id %}">Download Backup</a>


import os

# ...


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def backup_list(request, user_id):
    backup_folder = 'api/backup/'  # Update with your backup folder path
    backup_links = []

    for filename in os.listdir(backup_folder):
        if filename.startswith(f'user_data_{user_id}'):
            file_path = os.path.join(backup_folder, filename)
            backup_link = reverse('backup_detail', args=[user_id,filename])
            backup_links.append({'file_name': filename, 'backup_link': backup_link})

    context = {'backup_links': backup_links}
    return JsonResponse(context)


import io
import os
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']




from django.shortcuts import redirect
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_user(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        'api/client_secrets.json', SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/api/google-drive-callback/'
    authorization_url, state = flow.authorization_url(
        access_type='offline', prompt='consent')
    return redirect(authorization_url)



def upload_to_google_drive(file_path, file_name, user_credentials):
    drive_service = build('drive', 'v3', credentials=user_credentials)

    file_metadata = {'name': file_name}
    media = MediaIoBaseUpload(file_path, mimetype='application/pdf')

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')



from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from django.http import HttpResponseBadRequest

def google_drive_callback(request):
    flow = Flow.from_client_secrets_file(
        'api/client_secrets.json', SCOPES, redirect_uri='http://localhost:8000/google-drive-callback/')
    authorization_response = request.build_absolute_uri()
    try:
        flow.fetch_token(authorization_response=authorization_response)
    except Exception as e:
        print(str(e))
        return HttpResponseBadRequest(f'Failed to fetch user credentials.{str(e)}')


    credentials = flow.credentials
    # Save the user's credentials for future use (e.g., storing in the database)

    # Continue with further processing or redirection
    return HttpResponse('Authorization successful!')



from django.shortcuts import redirect

def initiate_google_drive_auth(request):
    return redirect('authenticate_user')


import pandas as pd


# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_stock_data(request, stock_symbol):
    try:
        # Read the data from the CSV file
        df = pd.read_csv(f'api/csv/{stock_symbol}.csv')

        # Convert the DataFrame to a dictionary
        data = df.to_dict('records')

        # Return the data as JSON
        return JsonResponse(data, safe=False)

    except FileNotFoundError:
        # If the CSV file does not exist, return an error message
        return JsonResponse({'error': 'Stock symbol not found'}, status=404)


@api_view(['GET'])
def yes_Change(request):
    users = User.objects.all()  # Retrieve all users
    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/stocks/live'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return Response({'error': 'Failed to fetch stock data.'}, status=500)

    stock_data = response.json()
    exceeded_stocks = []

    for user in users:
        wishlist_stocks = Wishlist.objects.filter(user=user)

        for wishlist_stock in wishlist_stocks:
            filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == wishlist_stock.stock_symbol), None)
            if not filtered_stock:
                continue

            closing_price = Decimal(filtered_stock.get('closingPrice'))

            if closing_price >= wishlist_stock.alert_price:
                exceeded_stocks.append((wishlist_stock.stock_symbol, format(closing_price, '.2f')))

        if exceeded_stocks:
            email = user.email
            send_mail(
                'SYSTEM ALERT #1',
                f"Stocks that exceeded alert price: {exceeded_stocks}",
                'settings.EMAIL_HOST_USER',
                [email],
                fail_silently=False
            )

    if exceeded_stocks:
        return Response(
            {'message': f'Stocks that exceeded alert price: {exceeded_stocks}'},
            status=200
        )

    return Response({'message': 'No stocks exceeded alert price.'}, status=200)