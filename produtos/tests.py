from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Factory

from .models import Produto, Favorito
from clientes.models import Cliente
from usuarios.tests import getApiCliente, criaUsuarios

def criaFavorito() -> object:
    """
        param: None
        return: Boolean
        Criar usuario, 2 produtos e inseri-los na tabela de favoritos !
    """    
    produto_1 = "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
    tb_produto_1 = Produto.objects.create(
        produto_id=produto_1
    )
    produto_2 = "b66897ea-4f5a-b8a9-dc7b-3011f37a18fc"
    tb_produto_2 = Produto.objects.create(
        produto_id=produto_2
    )
    email_cliente = faker.email()
    tb_cliente = Cliente.objects.create(
        email=email_cliente,
        nome=faker.name()
    )     
    tb_favorito = Favorito.objects.create(
        cliente=tb_cliente
    )
    tb_favorito.produtos.set([tb_produto_1, tb_produto_2])

    return tb_favorito

faker = Factory.create('pt_BR')
# Create your tests here.
class ProdutosModelTest(TestCase):
    def setUp(self):
        self.produto_id = "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
        Produto.objects.create(
            produto_id=self.produto_id
        )

    def testValidaQtdInserts(self):
        saved_models = Produto.objects.count()
        self.assertEqual(saved_models, 1)

class FavoritosModelTest(TestCase):
    def setUp(self):
        _ = criaFavorito()

    def testValidaQtdInserts(self):
        saved_models = Favorito.objects.count()
        self.assertEqual(saved_models, 1)

class FavoritosAPITest(TestCase):
    def setUp(self):
        self.tb_favorito = criaFavorito()
        self.list_produtos = [
            {"price": 1699.0, "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg", "brand": "b\u00e9b\u00e9 confort", "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f", "title": "Cadeira para Auto Iseos B\u00e9b\u00e9 Confort Earth Brown"},
            {"price": 805.0, "image": "http://challenge-api.luizalabs.com/images/b66897ea-4f5a-b8a9-dc7b-3011f37a18fc.jpg", "brand": "narciso rodriguez", "id": "b66897ea-4f5a-b8a9-dc7b-3011f37a18fc", "title": "Narciso Rodriguez For Her L?absolu"},
            {"price": 667.8, "image": "http://challenge-api.luizalabs.com/images/f8cb4a82-910e-6654-1240-d994c2997d2c.jpg", "brand": "burigotto", "id": "f8cb4a82-910e-6654-1240-d994c2997d2c", "title": "Cadeira para Auto Burigotto Matrix p/ Crian\u00e7as"},
            {"price": 199.0, "image": "http://challenge-api.luizalabs.com/images/b2968188-458c-3860-7729-2e2ec30dabd6.jpg", "brand": "doctor cooler", "id": "b2968188-458c-3860-7729-2e2ec30dabd6", "title": "Cooler 6 Latas Doctor Cooler"}
        ]
        self.endpoint = '/api/v1/favoritos/'
        email_usuario, email_superusuario, senha = criaUsuarios() #criando usuario
        self.api_client = getApiCliente(email_usuario, senha) #buscando Token


    def testValidaGET(self):
        response = self.api_client.get(self.endpoint)
        self.failUnlessEqual(response.status_code, 200)

    def testValidaPOST(self):
        #tb = Favorito.objects.get(email=self.email_usuario)
        response = self.api_client.post(
             self.endpoint,
            {
                "cliente":self.tb_favorito.cliente.id,
                "produtos":{"price": 149.9, "image": "http://challenge-api.luizalabs.com/images/93bd9fbf-5cd3-6385-1600-8eb9d9ee705d.jpg", "brand": "love", "id": "93bd9fbf-5cd3-6385-1600-8eb9d9ee705d", "title": "Banheira Infl\u00e1vel"}
            },
            format='json'
        )
        self.failUnlessEqual(response.status_code, 201)
        
        response = self.api_client.get(self.endpoint)
        response = response.json()
        self.failUnlessEqual(1, len(response.get('results')))
        self.failUnlessEqual(3, len(response['results'][0].get('produtos'))) #conferindo se existe 3 produtos, 2 do setUp e um novo     

    def testValidaPOSTList(self):
        response = self.api_client.post(
             self.endpoint,
            {
                "cliente":self.tb_favorito.cliente.id,
                "produtos":self.list_produtos
            },
            format='json'
        )
        self.failUnlessEqual(response.status_code, 201)
        
        response = self.api_client.get(self.endpoint)
        response = response.json()
        self.failUnlessEqual(1, len(response.get('results')))
        self.failUnlessEqual(4, len(response['results'][0].get('produtos'))) #conferindo se existe 4 produtos, 2 do setUp e 4 da nova lista sendo 2 duplicados

    def testValidaDELETE(self):
        response = self.api_client.delete(f'{self.endpoint}{self.tb_favorito.id}/')
        self.failUnlessEqual(response.status_code, 204)