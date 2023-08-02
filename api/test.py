# from django.contrib.auth.models import User

# # Assuming you have the user's username
# username = 'proteus69'

# # Get the user object
# user = User.objects.get(username=username)

# # Access the primary key (pk) of the user
# user_pk = user.pk

# # Print the user's pk
# print(user_pk)



# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def sell_stock(request):
#     stock_symbol = request.data.get('stockSymbol')
#     quantity = request.data.get('quantity')
#     quantity = int(quantity)
#     # Validate the input data
#     if not all([stock_symbol, quantity]):
#         return Response({'error': 'Incomplete data provided.'}, status=400)

#     # # Get the user's portfolio entry for the specified stock symbol
#     # try:
#     #     portfolio_entry = Portfolio.objects.get(user=request.user, stock_symbol=stock_symbol)
#     # except Portfolio.DoesNotExist:
#     #     return Response({'error': 'Portfolio entry not found.'}, status=404)
#     if quantity <= 0:
#         return Response({'error': 'Quantity must be a positive integer.'}, status=400)
# # Get the user's portfolio entries for the specified stock symbol
#     portfolio_entries = Portfolio.objects.filter(user=request.user, stock_symbol=stock_symbol)

#     # Check if any portfolio entries are found
#     if not portfolio_entries.exists():
#         return Response({'error': 'Portfolio entry not found.'}, status=404)

#     # If multiple entries are found, choose the appropriate one based on your criteria
#     portfolio_entry = portfolio_entries.first()  # You can modify this logic as per your requirements

#     # Calculate the selling price based on the current closing price
#     headers = {
#         'Authorization': 'YOU_API_KEY'
#     }
#     url = 'https://api.kitta.dev/stocks/live'

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return Response({'error': 'Failed to fetch stock data.'}, status=500)

#     stock_data = response.json()

#     # Find the matching stock based on the stock symbol
#     filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == stock_symbol), None)
#     if not filtered_stock:
#         return Response({'error': 'Stock symbol not found.'}, status=404)

#     closing_price = Decimal(filtered_stock.get('closingPrice'))

#     # Calculate the total selling price
#     sell_price = closing_price * Decimal(quantity)

#     # Update the portfolio entry with the selling price
#     portfolio_entry.sell_price = sell_price
#     portfolio_entry.save()

#     # Deduct the selling price from the user's balance
#     user = request.user
#     user.balance.amount += sell_price
#     user.balance.save()

#     # Deduct the quantity from the user's portfolio entry
#     if portfolio_entry.quantity <= 0:
#         portfolio_entry.delete()
#     else:
#         portfolio_entry.save()

#     return Response({'success': 'Stock sold successfully.'}, status=200)

# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def sell_stock(request):
#     stock_symbol = request.data.get('stockSymbol')
#     quantity = request.data.get('quantity')
#     quantity = int(quantity)
#     # Validate the input data
#     if not all([stock_symbol, quantity]):
#         return Response({'error': 'Incomplete data provided.'}, status=400)

#     if quantity <= 0:
#         return Response({'error': 'Quantity must be a positive integer.'}, status=400)

#     # Get the user's portfolio entries for the specified stock symbol
#     portfolio_entries = Portfolio.objects.filter(user=request.user, stock_symbol=stock_symbol)

#     # Check if any portfolio entries are found
#     if not portfolio_entries.exists():
#         return Response({'error': 'Portfolio entry not found.'}, status=404)

#     # If multiple entries are found, choose the appropriate one based on your criteria
#     portfolio_entry = portfolio_entries.first()  # You can modify this logic as per your requirements

#     # Check if the user has enough stocks to sell
#     if portfolio_entry.quantity < quantity:
#         return Response({'error': 'Not enough stocks to sell.'}, status=400)

#     # Calculate the selling price based on the current closing price
#     headers = {
#         'Authorization': 'YOU_API_KEY'
#     }
#     url = 'https://api.kitta.dev/stocks/live'

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return Response({'error': 'Failed to fetch stock data.'}, status=500)

#     stock_data = response.json()

#     # Find the matching stock based on the stock symbol
#     filtered_stock = next((stock for stock in stock_data if stock['stockSymbol'] == stock_symbol), None)
#     if not filtered_stock:
#         return Response({'error': 'Stock symbol not found.'}, status=404)

#     closing_price = Decimal(filtered_stock.get('closingPrice'))

#     # Calculate the total selling price
#     sell_price = closing_price * Decimal(quantity)

#     # Update the portfolio entry with the selling price
#     portfolio_entry.sell_price = sell_price
#     portfolio_entry.save()

#     # Deduct the selling price from the user's balance
#     user = request.user
#     user.balance.amount += sell_price
#     user.balance.save()

#     # Deduct the quantity from the user's portfolio entry
#     portfolio_entry.quantity -= int(quantity)
    
#     # Delete the portfolio entry if all stocks of this type were sold, else save the new quantity
#     if portfolio_entry.quantity == 0:
#         portfolio_entry.delete()
#     else:
#         portfolio_entry.save()

#     return Response({'success': 'Stock sold successfully.'}, status=200)


import requests

def authorize_user():
    client_id = "726472864224-i20lshqpug5rn0b46vn43dgk3ams3o2o.apps.googleusercontent.com"
    client_secret = "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"
    redirect_uri = "http://localhost:8000/google-drive-callback/"

    url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "scope": "https://www.googleapis.com/auth/drive",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # The user has authorized your application.
        return True
    else:
        # The user has not authorized your application.
        return False

if __name__ == "__main__":
    authorized = authorize_user()
    print(authorized)