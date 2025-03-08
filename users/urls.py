from django.urls import path
from users.views import CreateEnseignantView,LoginView,LogoutView, UserListView

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('create-enseignant/', CreateEnseignantView.as_view(), name='create_enseignant'),
    path('login/', LoginView.as_view(), name='login_user'),
    path("logout/", LogoutView.as_view(), name='logout_user'),

]
