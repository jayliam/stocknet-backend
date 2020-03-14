from django.shortcuts import render
from django.http import HttpResponse
from .models import Service
# Create your views here.
def home(request):
    s1 = Service()
    s1.title="L’efficacité aux commandes"
    s1.desc="Passez moins de temps devant l’écran et davantage auprès de vos clients."
    return render(request,"index.html",{'s1':s1})
