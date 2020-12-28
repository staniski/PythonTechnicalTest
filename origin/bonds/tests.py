from django.contrib.auth.models import User
from bonds.models import Bond
from bonds.serializers import BondSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase



class RegisterUserTestCase(APITestCase):
    def test_registration(self):
        data = {"username": "user", "password": "password"}
        response = self.client.post('/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BondViewTestCase(APITestCase):
   

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password")
        self.token = Token.objects.get(user=self.user)
        self.authorization()

    def authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_post(self):
        data = {"isin": "FR0000131104", 
                "size": 1000000, 
                "currency": "USD", 
                "maturity": "2025-09-25", 
                "lei": "R0MUWSFPU8MPRO8K5P83", 
                "legal_name": "X"}
        
        res = self.client.post('/bonds/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['legal_name'], "BNPPARIBAS")

    def test_post_false_lei_provided(self):
        data = {"isin": "FR0000131104", 
                "size": 1000000, 
                "currency": "USD", 
                "maturity": "2025-09-25", 
                "lei": "R0MUWSFPU8MPRO8K5P84", 
                "legal_name": "X"}
        
        res = self.client.post('/bonds/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['legal_name'], "False lei provided")

    def test_post_not_200_res(self):
        data = {"isin": "FR0000131104", 
                "size": 1000000, 
                "currency": "USD", 
                "maturity": "2025-09-25", 
                "lei": "1", 
                "legal_name": "X"}
        
        res = self.client.post('/bonds/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['legal_name'], "Unknown")
    
    def test_get_all_authorized(self):
        response = self.client.get("/bonds/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_all_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/bonds/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    

    def test_filter_legalname(self):
        response = self.client.get('/bonds/?legal_name=BNPPARIBAS')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



  
 


