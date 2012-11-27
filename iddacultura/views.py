from django.shortcuts import redirect
from profiles.views import profile_detail

def user_profile(request):
    """
    Redireciona para a pagina do usuario.
    Talvez exista uma maneira de fazer isso diretamente no login.html
    """
    
    return redirect('/profiles/' + request.user.username + '/')
