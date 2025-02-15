from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render, redirect
from realDealz.models import Game
from django.db.models import Q
from django.db import connection
from realDealz.library import Library
from django.core.paginator import Paginator
from django.core import serializers
from realDealz.updateData import updateGamePrices


def home(request):
    l = Library()
    context = {
        'title': 'Homepage',
        'msg': 'Home',
    }
    if request.method == 'POST':
        if 'load' in request.POST:
            Game.initial_load()
            updateGamePrices()
            # return redirect('Catalog')
        if 'reset' in request.POST:
            Game.clear_all()
            # return redirect('Catalog')
        if 'steam-login' in request.POST:
            if request.user.is_authenticated:
                return redirect('catalog/')
            return redirect('accounts/steam/login/')

    return render(request, "home.html", context=context)

def profile(request):
    return render(request, "profile.html")


def about(request):
    context = {
        'msg': 'About Us',
    }
    return render(request, "about.html", context=context)


def contact(request):
    context = {
        'msg': 'Contact',
    }
    return render(request, "contact.html", context=context)


def game_search(request):

    games = Game.objects.all()
    filtered_table = None

    query = request.GET.get('filtered_name')
    if query:
        filtered_table = Game.objects.filter(
            Q(name__icontains=query) or Q(
                platform__P__icontains=query) or Q(genre__G__icontains=query))
    else:
        filtered_table = Game.objects.all()

    #paginator = Paginator(filtered_table, 80)    
    #page_number = request.GET.get('page')    
    #current_page = paginator.get_page(page_number)    

    context = {
        'games': games,
        'filtered_table': filtered_table,
        #'games_page': current_page,  
    }
    return render(request, 'game_list.html', context)


def game_detail(request, game_id):
    game = Game.objects.get(appid=game_id)
    return render(request, 'game_detail.html', {'Game': game})


def game_list(request):

    games = Game.objects.all()
    filtered_table = None
    filtered_table = Game.objects.all()

    if request.method == 'POST':
        filter_id = request.POST.get('filtered_id')
        filter_developer = request.POST.get('filtered_developer')

        if filter_id:
            filtered_table = Game.objects.filter(appid=filter_id)
        elif filter_developer:
            filtered_table = Game.objects.filter(Q(developer__icontains=filter_developer))
        else:
            filtered_table = Game.objects.all()
    else:
        filtered_table = Game.objects.all()

    #Issues with Paginator: Filters don't stay when changing pages
    #paginator = Paginator(filtered_table, 50)    
    #page_number = request.GET.get('page')    
    #current_page = paginator.get_page(page_number)    
    

    context = {
        'games': games,
        'filtered_table': filtered_table,
        #'games_page': current_page,  
    }
    return render(request, 'game_list.html', context)