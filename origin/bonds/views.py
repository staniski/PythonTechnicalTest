from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from bonds.serializers import BondSerializer, UserSerializer
from bonds.models import Bond
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

    


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
   

class BondView(generics.ListCreateAPIView):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['legal_name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset

    

    
    

