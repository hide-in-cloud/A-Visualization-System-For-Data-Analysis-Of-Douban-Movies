from django.urls import path, re_path
from app import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('movie/info', views.MovieInfoView, basename='movie/info')
router.register('movie/page', views.MovieInfoByPageView, 'movie/page')
router.register('movie/chart', views.ChartView, 'movie/chart')

urlpatterns = [
    # 电影
    # path('movie/detail/', views.MovieDetailView.as_view()),
    # re_path(r'movie/detail/(?P<pk>\d+)/', views.MovieDetailRawView.as_view()),
    re_path(r'movie_update/(?P<pk>\d+)/', views.MovieUpdateView.as_view()),
]

urlpatterns += router.urls
