from django.contrib import admin
# Register your models here.

from .models import *

admin.site.register([User,Balance,Expenditure,Income,Transaction,Portfolio,Portfolio_History,Wishlist,Debt])
#omg i could just add all this hours omg why