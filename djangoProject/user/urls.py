from user import views
from rest_framework.routers import SimpleRouter
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()
router.register('user', views.UserInfoView, 'user')
router.register('userByPage', views.UserInfoByPageView, 'userByPage')
# router.register('user_rating', views.UserRatingView, 'user_rating')

urlpatterns = [
    # path('uploadImg/', views.uploadImg),
    re_path(r'user_update/(?P<pk>\d+)/', views.UserUpdateView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
