from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CommentViewSet,
    BadgeViewSet,
    UserBadgeViewSet,
    PostLikeViewSet,
    UserRegistrationView,
    TripGroupViewSet,
    PostViewSet,
    GroupPostsView,
    GenerateQRCodeView,
    JoinGroupByQRCodeView,
    UserProfileView,
    UserDetailView,
)
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('groups/join/', JoinGroupByQRCodeView.as_view(), name='join_group_by_qr'),
    path('groups/<int:group_id>/posts/', GroupPostsView.as_view(), name='group-posts'),
    path('groups/<int:group_id>/generate_qr/', GenerateQRCodeView.as_view(), name='generate_qr'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
]

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'badges', BadgeViewSet)
router.register(r'user-badges', UserBadgeViewSet)
router.register(r'post-likes', PostLikeViewSet)
router.register(r'groups', TripGroupViewSet)
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'post-likes', PostLikeViewSet, basename='post-likes')

urlpatterns += [
    path('', include(router.urls)),
]