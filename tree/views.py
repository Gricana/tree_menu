from django.shortcuts import render


def test_menu(request, path):
    return render(request, 'test_menu.html')
