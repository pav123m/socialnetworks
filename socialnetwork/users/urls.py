from django.urls import path
from .views import UserSignup, UserLogin, UserSearch, SendFriendRequest, HandleFriendRequest, ListFriends, ListPendingFriendRequests

urlpatterns = [
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('search/', UserSearch.as_view(), name='search'),
    path('send-request/<int:to_user_id>/', SendFriendRequest.as_view(), name='send_request'),
    path('handle-request/<int:request_id>/<str:action>/', HandleFriendRequest.as_view(), name='handle_request'),
    path('friends/', ListFriends.as_view(), name='friends_list'),
    path('pending-requests/', ListPendingFriendRequests.as_view(), name='pending_requests'),
]
