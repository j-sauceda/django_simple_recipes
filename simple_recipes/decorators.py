from django.shortcuts import redirect

# if user already authenticated, redirect
def user_is_not_authenticated(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)
        
    return wrapper_function
