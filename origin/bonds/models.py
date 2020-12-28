from django.db import models
import requests
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


class Bond(models.Model):
    isin = models.CharField(max_length=12)
    size = models.PositiveIntegerField()
    currency = models.CharField(max_length=10)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='bonds', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        
        lei_url = f"https://leilookup.gleif.org/api/v2/leirecords?lei={self.lei}"
        response = requests.get(lei_url)
            
        if response.status_code == 200:
            name = response.json()
            try:
                legal_name = str(name[0]['Entity']['LegalName']['$'])
                
                legal_name = legal_name.replace(" ", "")
                self.legal_name = legal_name
            except:
                self.legal_name = "False lei provided"
           
        else:
            self.legal_name = "Unknown"
        
        super(Bond, self).save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)