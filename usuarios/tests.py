from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from faker import Factory

from .models import Usuario

faker = Factory.create('pt_BR')
# Create your tests here.


def criaUsuarios() -> list:
    """
        param: None
        return: list(email_usuario, email_superusuario, senha)
        Objective: Criar usuario e superusuario na table Usuario.
    """
    email_usuario = faker.email()
    email_superusuario = faker.email()
    senha = faker.password()
    Usuario.objects.create_user(
        email=email_usuario,
        nome=faker.name(),
        password=senha,
    )
    super_user = Usuario.objects.create_superuser(
        email=email_superusuario,
        nome=faker.name(),
        password=senha
    )        

    return [email_usuario, email_superusuario, senha]

def getApiCliente(email: str, senha: str) -> object:
    """
        param: (email, senha)
        return: Objeto APIClient com token de autorização setado.
        Objective: Buscar token e inseri-lo no HEADER do APIClient
    """    
    api_client = APIClient()
    resp = api_client.post(reverse('token_obtain_pair'), {'email':email, 'password':senha})
    api_client.credentials(HTTP_AUTHORIZATION='JWT ' + resp.data.get("access"))
    return api_client


class UsuariosModelTest(TestCase):
    def setUp(self):
        self.email_usuario, self.email_superusuario, self.senha = criaUsuarios()

    def testValidaQtdInserts(self):
        saved_models = Usuario.objects.count()
        self.assertEqual(saved_models, 2)

    def testExistsSuperUser(self):
        saved_models = Usuario.objects.get(email=self.email_superusuario)
        self.assertEqual(saved_models.is_superuser, True)

class UsuariosAPITest(TestCase):
    def setUp(self):
        self.email_usuario, self.email_superusuario, self.senha = criaUsuarios()
        self.api_client = getApiCliente(self.email_usuario, self.senha)

    def testRegistraNovoUsuario(self):
        email=faker.email()
        password=faker.password()
        response = self.api_client.post(
            '/api/v1/usuarios/registra_usuario/',
            {
                "nome":faker.name(),
                "email":email, 
                "password":password,
                "is_active":True
            }
        ) #criando usuario via API
        self.failUnlessEqual(response.status_code, 201)
        
        response = self.api_client.get('/api/v1/usuarios/dados/') #Buscando dados do novo usuario
        self.failUnlessEqual(3, len(response.data.get("results")))
        resp = self.api_client.post(reverse('token_obtain_pair'), {'email':email, 'password':password})
        self.assertEqual(resp.status_code, 200) #validando com a senha correta                

class UsuariosTokenTest(TestCase):
    def setUp(self):
        self.email_usuario, self.email_superusuario, self.senha = criaUsuarios()
        self.api_client = APIClient()

    def testValidaTokenJWT(self):        
        resp = self.api_client.post(reverse('token_obtain_pair'), {'email':self.email_usuario, 'password':self.senha})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('access' in resp.data)
        
        token = resp.data.get("access")
        refresh = resp.data.get("refresh")

        resp = self.api_client.post(reverse('token_verify'), {'token': token})
        self.assertEqual(resp.status_code, 200) #validando token

        resp = self.api_client.post(reverse('token_verify'), {'token': 'abc'})
        self.assertEqual(resp.status_code, 401) #verificando se retorna erro com token invalido

        resp = self.api_client.post(reverse('token_refresh'), {'refresh': refresh})
        self.assertEqual(resp.status_code, 200) #validando refresh token

        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        resp = self.api_client.get('/api/v1/usuarios/dados/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 401) #GET com authorization errado

        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        resp = self.api_client.get('/api/v1/usuarios/dados/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200) #GET com authorization valido
    
