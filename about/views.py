from django.shortcuts import render


def about(request):
    context = {
        'page_title': 'About Us - Fur Fun',
    }
    return render(request, 'about/about.html', context)
