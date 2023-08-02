# from django.core.management.commands.runserver import Command as RunServerCommand
# from api.tasks import update_stock_prices,getStock_Change,send_sms

# import threading
# class Command(RunServerCommand):
#     help = 'Starts the Django server and triggers the stock update task'

#     def inner_run(self, *args, **options):

#         user_id = self.get_user_id()
#         print("Custom runserver command is running")  # New print statement
#         # Trigger the stock update task
#         self.stdout.write(self.style.SUCCESS('Triggering the stock update task...'))
#         self.stdout.write(self.style.SUCCESS('Adding the stock update task to queue...'))
#         self.stdout.write(self.style.SUCCESS('check the stock change...'))
#         update_stock_prices()
#         getStock_Change(user_id)


#         # Start the Django server
#         super().inner_run(*args, **options)

#         def get_user_id(self):
#         # Extract the user ID from the request object
#             request = self.get_request()
#             user_id = None

#             if request and request.user and request.user.is_authenticated:
#                 user_id = request.user.id

#             return user_id

#         def get_request(self):
#         # Get the request object from the thread-local storage
#             request = getattr(threading.current_thread(), "_request", None)
#             return request



# # from django.core.management.base import BaseCommand

# # from django.utils import timezone

# # class Command(BaseCommand):
# #     help = 'Displays current time'

# #     def handle(self, *args, **kwargs):
# #         time = timezone.now().strftime('%X')
# #         self.stdout.write("It's now %s" % time)






# # # # moving avrage,rsi
# # # # wish_list


from django.core.management.commands.runserver import Command as RunServerCommand
from api.tasks import update_stock_prices, getStock_Change

class Command(RunServerCommand):
    help = 'Starts the Django server and triggers the stock update task'

    def inner_run(self, *args, **options):
        # Retrieve the user ID from the request object
        # user_id = self.get_user_id()
        # print(user_id)

        print("Custom runserver command is running")
        self.stdout.write(self.style.SUCCESS('Triggering the stock update task...'))
        self.stdout.write(self.style.SUCCESS('Adding the stock update task to queue...'))
        self.stdout.write(self.style.SUCCESS('check the stock change...'))

        # Pass the user ID to the stock update tasks
        # update_stock_prices()
        # Pass the user ID to the background task
        # if user_id is not None:

        #     getStock_Change(user_id)
        # else:
        #     print("User ID is None. Task not triggered.")
        getStock_Change()
        update_stock_prices()



        # Start the Django server
        super().inner_run(*args, **options)

    def get_user_id(self):
        # Extract the user ID from the request object
        request = self.get_request()
        user_id = None

        if request and request.user and request.user.is_authenticated:
            user_id = request.user.id

        return user_id

    def get_request(self):
        # Get the request object from the thread-local storage
        import threading
        request = getattr(threading.current_thread(), "_request", None)
        return request
