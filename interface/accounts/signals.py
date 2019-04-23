from django.contrib.auth.signals import user_logged_in, user_logged_out

print('\n\ninterface signals')

def user_login(sender, user, request, **kwargs):
    print('\n\n User login', sender, user, request, kwargs)


def user_logout(sender, user, request, **kwargs):
    print('\n\n User logout', sender, user, request, kwargs)

user_logged_in.connect(user_login)
user_logged_out.connect(user_logout)
