from users.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect


def authorization(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        else:
            messages.error(request, 'Хм... Что-то пошло не так. Попробуйте еще разок')
    else:
        pass

    return redirect('/')
