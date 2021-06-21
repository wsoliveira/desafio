from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Factory

from .models import Cliente
from usuarios.tests import getApiCliente, criaUsuarios


faker = Factory.create('pt_BR')
# Create your tests here.
class ClientesModelTest(TestCase):
    def setUp(self):
        self.email_usuario = faker.email()
        Cliente.objects.create(
            email=self.email_usuario,
            nome=faker.name()
        )

    def testValidaQtdInserts(self):
        saved_models = Cliente.objects.count()
        self.assertEqual(saved_models, 1)

class ClientesAPITest(TestCase):
    def setUp(self):
        self.email_usuario = faker.email()
        Cliente.objects.create(
            email=self.email_usuario,
            nome=faker.name()
        )
        self.endpoint = '/api/v1/clientes/'
        email_usuario, email_superusuario, senha = criaUsuarios() #criando usuario
        self.api_client = getApiCliente(email_usuario, senha) #buscando Token


    def testValidaGET(self):
        response = self.api_client.get(self.endpoint)
        self.failUnlessEqual(response.status_code, 200)

    def testValidaPOST(self):
        response = self.api_client.post(
             self.endpoint,
            {
                "nome":faker.name(),
                "email":faker.email()
            }
        )
        self.failUnlessEqual(response.status_code, 201)
        
        response = self.api_client.get(self.endpoint)
        self.failUnlessEqual(2, len(response.data.get("results")))


    def testValidaPUTParcial(self):
        tb = Cliente.objects.get(email=self.email_usuario)
        response = self.api_client.patch(
            f'{self.endpoint}{tb.id}/',
            {
                "nome":"Desafio",
            },
            format='json'            
        )
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.data.get('nome'), 'Desafio')

    def testValidaPUT(self):
        tb = Cliente.objects.get(email=self.email_usuario)
        response = self.api_client.put(
            f'{self.endpoint}{tb.id}/',
            {
                "nome":tb.nome,
                "email":'validaPUT@validaPUT.com',
            },
            format='json'        
        )
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual('validaPUT@validaPUT.com', response.data.get("email"))
        self.failUnlessEqual(response.data.get('nome'), tb.nome)

    def testValidaDELETE(self):
        tb = Cliente.objects.get(email=self.email_usuario)
        response = self.api_client.delete(f'{self.endpoint}{tb.id}/')
        self.failUnlessEqual(response.status_code, 204)
