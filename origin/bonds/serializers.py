from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bond
from rest_framework import permissions

class BondSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Bond
        fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name', 'owner']

    def create(self, validated_data):
        """
        Create and return a new `Bond` instance, given the validated data.
        """
        return Bond.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
     