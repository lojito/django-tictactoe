from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.http import JsonResponse
from .forms import GameForm
from .models import Game
from .board import Board

def home(request):
    return render(request, 'game/home.html')

@login_required
def new_game(request):
    if request.method == 'GET':
        game = Game.objects.create(board='0000000000000000', user=request.user)
        return render(request, 'game/new_game.html', {'game': game})
    
@login_required
def unfinished_games(request):
    games = Game.objects.filter(user=request.user, finished__isnull=True)
    return render(request, 'game/unfinished_games.html', {'games': games})
    
@login_required
def finished_games(request):
    games = Game.objects.filter(user=request.user, finished__isnull=False).order_by('-finished')
    return render(request, 'game/finished_games.html', {'games': games})

@login_required
def view_game(request, game_pk):
    game = get_object_or_404(Game, pk=game_pk, user=request.user)
    if request.method == 'GET':
        form = GameForm(instance=game)
        if game.finished is None:
            return render(request, 'game/view_unfinished_game.html', {'game':game, 'form':form})
        else:
            return render(request, 'game/view_finished_game.html', {'game':game, 'form':form})     

@login_required
def update_game(request, game_pk, finished):
    game = get_object_or_404(Game, pk=game_pk, user=request.user)
    form = GameForm(request.GET, instance=game)
    form.save()
    newgame = form.save(commit=False)
    newgame.user = request.user
    if finished:
        newgame.finished = timezone.now()
    else:
        newgame.board = request.board
    newgame.save()
    
@login_required
def finish_game(request, game_pk):
    if request.method == 'GET':
        try:
            update_game(request, game_pk, True)
            return JsonResponse({'error': ""})
        except ValueError:
            return JsonResponse({'error': str(ValueError)})

@login_required
def delete_game(request, game_pk):
    game = get_object_or_404(Game, pk=game_pk, user=request.user)
    if request.method == 'POST':
        game.delete()
        return redirect('unfinished_games')
        
@login_required
def play_game(request, game_pk):
    try:
        board = Board(request.GET["board"])
        winning_square = board.get_winning_square(board.COMPUTER)
        if winning_square == Board.SQUARE_NOT_FOUND:
            winning_square = board.get_winning_square(board.USER)
        if winning_square != Board.SQUARE_NOT_FOUND:
            board.play(Board.COMPUTER, winning_square)
            request.board = str(board)
            update_game(request, game_pk, False)
            return JsonResponse({'square': winning_square, 'error':''})
        
        if board.is_full():
            return JsonResponse({'square': board.SQUARE_NOT_FOUND, 'error':''})
        else:
            random_empty_square = board.get_random_empty_square()
            if random_empty_square != board.SQUARE_NOT_FOUND:
                board.play(Board.COMPUTER, random_empty_square)
                request.board = str(board)
                update_game(request, game_pk, False)
            return JsonResponse({'square': random_empty_square, 'error':''})
            
    except Exception as e:
        return JsonResponse({'error': str(e)})        

def signup_user(request):
    if request.method == 'GET':
        return render(request, 'game/signup_user.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('unfinished_games')
            except IntegrityError:
                return render(request, 'game/signup_user.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'game/signup_user.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})
            
def login_user(request):
    if request.method == 'GET':
        return render(request, 'game/login_user.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'game/login_user.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('unfinished_games')

@login_required 
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')            