from django.shortcuts import render

# Create your views here.
def home(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            return render(request, "pages/home.html")
        return render(request, "pages/landing-page.html")