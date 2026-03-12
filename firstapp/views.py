from django.http import HttpResponse

def function_view(request):
    return HttpResponse("Hello from function!")

# Create your views here.
