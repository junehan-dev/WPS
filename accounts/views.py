from config.utils import response_error_handler
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework import status
from accounts.serializers import (
    UserListSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    StaffSerializer,
    AdminSerializer,
)
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class UserListView(viewsets.generics.ListCreateAPIView):
    """A function, able to get list of user and Create normal user
    
    Arguments:
        viewsets {[ListCreateAPIView]} -- [GET, POST handler]
    Raises:
        ValidationError: [POST-HTTP_400_BAD_REQUEST]
    Returns:
        [GET-status] -- [GET-201-HTTP_201_CREATED]
        [POST-status] -- [GET-200-HTTP_200_OK]
    """
    queryset = get_user_model().objects.filter(is_staff=False)
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        else:
            return UserListSerializer

    @response_error_handler
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(viewsets.generics.RetrieveUpdateAPIView):
    """A function, able to get specific user data and update
    
    Arguments:
        viewsets {[RetirieveUpdateAPIView]} -- [GET, PUT handler]
    Raises:
        PermissionError: [PUT-HTTP_401_UNAUTHORIZED]
        ValidationError: [PUT-HTTP_400_BAD_REQUEST]
        ValueError: [GET-HTTP_404_NOT_FOUND]
    Returns:
        [status] -- [GET-200-HTTP_200_OK]
        [status] -- [PUT-204-HTTP_204_NO_CONTENT]
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        else:
            return UserDetailSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        queryset = get_user_model().objects.filter(id=pk, is_staff=False)
        return queryset

    @response_error_handler
    def put(self, request, *args, **kwargs):
        if (
            request.user == self.get_queryset()[0]
            or request.user.is_staff
            or request.user.is_superuser
        ):
            response = super().put(request, *args, **kwargs)
            response.status_code = 204
            return response
        else:
            raise PermissionError("you are not user or staff", "do not do that")
    @response_error_handler
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args,**kwargs)
        except Exception:
            raise ValueError("User id Not found", "check user id")


class AdminListCreateView(viewsets.generics.ListCreateAPIView):
    """A function, able to create and list admin user list
    Arguments:
        viewsets {[ListCreateAPIView]} -- [GET, POST handler]
    
    Raises:
        PermissionError: [GET-HTTP_401_UNAUTHORIZED]
        PermissionError: [POST-HTTP_401_UNAUTHORIZED]
        ValidationError: [POST-HTTP_400_BAD_REQUEST]
    
    Returns:
        [status] -- [GET-200-HTTP_200_OK]
        [status] -- [POST-201-HTTP_CREATED]
    """

    queryset = get_user_model().objects.filter(is_superuser=True)
    permission_classes = (IsAdminUser,)

    @response_error_handler
    def get(self, request, *args, **kwargs):
        staffs = [_ for _ in self.get_queryset()]
        if request.user in staffs:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionError("not staff or admin", "login as staff or admin first")

    @response_error_handler
    def post(self, request: Request, *args, **kwargs):
        username = request.POST.get("username")
        key_a = "FBI_B"
        if all([key_a not in username]):
            raise PermissionError("not registered id for staff", "dont do it")
        return super().post(request, args, kwargs)

    def get_serializer_class(self):
        serializer_class = UserListSerializer
        if self.request.method == "POST":
            serializer_class = StaffSerializer
        return serializer_class



class StaffListCreateView(viewsets.generics.ListCreateAPIView):
    """A function, able to create and list staff user list
    
    Arguments:
        viewsets {[ListCreateAPIView]} -- [GET, POST handler]
    
    Raises:
        PermissionError: [GET-HTTP_401_UNAUTHORIZED]
        PermissionError: [POST-HTTP_401_UNAUTHORIZED]
        ValidationError: [POST-HTTP_400_BAD_REQUEST]
        
    Returns:
        [status] -- [GET-200-HTTP_200_OK]
        [status] -- [POST-201-HTTP_CREATED]
    """

    queryset = get_user_model().objects.filter(is_staff=True, is_superuser=False)
    permission_classes = (AllowAny, )

    @response_error_handler
    def get(self, request, *args, **kwargs):
        # print(request.user)
        staffs = [_ for _ in self.get_queryset()]
        if request.user in staffs:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionError("not staff or admin", "login as staff or admin first")

    @response_error_handler
    def post(self, request: Request, *args, **kwargs):
        username = request.POST.get("username")
        key_a = "FBI_I"
        key_b = "FBI_F"
        if all([key_a not in username, key_b not in username]):
            raise PermissionError("not registered id for staff", "dont do it")
        return super().post(request, args, kwargs)

    def get_serializer_class(self):
        serializer_class = UserListSerializer
        if self.request.method == "POST":
            serializer_class = StaffSerializer
        return serializer_class
