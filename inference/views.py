from django.shortcuts import render

def index(request):
    return render(request, 'inference/index.html', {
        "title": "Scanner App built with Django, Tensorflow and Vue.js. Machine Learning models built using Google's Teachable Machine"
    })
