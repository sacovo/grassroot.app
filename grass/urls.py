from django.urls import path
from django.views.generic.base import TemplateView

from grass import views

urlpatterns = [
    path('signup-group/', views.SignupWizzard.as_view(), name="create-group"),
    path('complete-signup/', views.login_or_signup, name="login_or_signup"),
    path('link-account/', views.link_account, name="link-account"),
    path('grassroot/<int:pk>/', views.landing_page, name="landing-page"),
    path('dashboard/<int:pk>/', views.dashboard, name="dashboard"),
    path('map/', views.map_view, name="map"),
    path('impressum/', TemplateView.as_view(
        template_name='grass/impressum.html'
    ), name="impressum"),
    path('about/', views.about_view, name="about"),
    path('', views.home, name="home"),
]
