from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'app/index.html')

def player(request):
    return render(request, 'app/player.html')