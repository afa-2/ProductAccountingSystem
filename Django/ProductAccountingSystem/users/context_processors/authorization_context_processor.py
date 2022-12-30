from users.forms import UserAuthenticationForm


def authorization_form(request):
    form = UserAuthenticationForm()
    context = {'AuthenticationForm': form}
    return context

