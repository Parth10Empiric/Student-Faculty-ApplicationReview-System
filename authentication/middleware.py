# from django.shortcuts import redirect
# from django.contrib import messages

# class HandleCsrfFailureMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
        
#         # Check if the response is a 403 error
#         if response.status_code == 403:
#             messages.error(request, "Security token invalid. Please try logging in again.")
#             return redirect('home')
            
#         return response
    

