from background_task import background
import requests
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from api.models import Portfolio_History
import logging

from random import choice
from django.http import HttpRequest
from api.models import *




from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User

User = get_user_model()



logger = logging.getLogger(__name__)

@background(schedule=3600)  # Run every 1 hour
def update_stock_prices():
    headers = {
        'Authorization': 'YOU_API_KEY'
    }
    url = 'https://api.kitta.dev/stocks/live'

    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        logger.error('Failed to fetch stock data.')
        return
    
    stock_data = response.json()

    logger.info('Update stock prices task started')  # Log start of the task


    users = User.objects.all()
   

    for user in users:
        portfolio_entries = Portfolio_History.objects.filter(user=user)
        for entry in portfolio_entries:
            stock_symbol = entry.stock_symbol

            # Find the matching stock based on the stock symbol
            filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == stock_symbol), None)
            if not filtered_stock:
                logger.error('Stock symbol not found: ' + stock_symbol)
                continue  # Skip to next entry
            
            closing_price = Decimal(filtered_stock.get('closingPrice'))

            # closing_price = choice(list1)

            # Update the user's stock balance based on the current closing price
            entry.stock_balance = closing_price * entry.quantity 
            entry.save()
            logger.info(f'Stock balance updated for user {user.id}, new balance: {entry.stock_balance}')  # Log each update

        logger.info('Update stock prices task completed')  # Log end of the task



import json        


@background(schedule=3600)
def getStock_Change():
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
            # msg = "hi" 
            msg = str(exceeded_stocks)
            
            phone_number = user.phone_number
            if phone_number:
                service_plam_id = "SERVICE_PLAN_ID"
                logger.info('SMS PHONE_NUMBER')
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
                requests.post(
                f"https://sms.api.sinch.com/xms/v1/{service_plam_id}/batches",
                    headers=headers,
                    data=json.dumps(payload) )
                if response.status_code == 201:
                    logger.info('SMS sent successfully')
                    return HttpResponse('SMS sent successfully')
                else:
                    logger.info('Unable to send sms')
                    return HttpResponse('Failed to send SMS', status=response.status_code)


    if exceeded_stocks:
        return Response(
            {'message': f'Stocks that exceeded alert price: {exceeded_stocks}'},
            status=200
        )

    return Response({'message': 'No stocks exceeded alert price.'}, status=200)
