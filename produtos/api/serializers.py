from rest_framework.serializers import ModelSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from produtos.models import Produto, Favorito
from clientes.models import Cliente
from requests import get


def getExistsProdutoUrl(produto_id: str) -> bool:
    """
        param: produto_id (ID da api)
        return: Boolean
        Objective: Valida se URL existe, se sim retorna True senão False.
    """    
    link    = f'http://challenge-api.luizalabs.com/api/product/{produto_id}/'
    ret     = get(link)
    return True if ret.status_code == 200 else False
    
def getDetalhesProduto(produto_id: str) -> dict:
    """
        param: produto_id (ID da api)
        return: Dicionário
        Objective: Buscar detalhes do produto via API
    """        
    dic_produto = {}
    link = f'http://challenge-api.luizalabs.com/api/product/{produto_id}/'
    ret = get(link)
    if ret.status_code != 200: #Se URL não existir sera criado um json com a chave 'detail'
        dic_produto['detail']   = 'Produto nao encontrado na API !'
        dic_produto['link']     = link
        return dic_produto

    response = ret.json()
    dic_produto['title']   = response.get('title')
    dic_produto['image']   = response.get('image')
    dic_produto['price']   = response.get('price')
    dic_produto['link']    = link

    return dic_produto

class FavoritosSerializer(ModelSerializer):
    class Meta:
        model   = Favorito
        #many = True
        fields  = '__all__'

    def to_internal_value(self, data):
        """
            Alterando o comportamento do metodo original para deixar a API flexível
            recebendo um dicionário ou uma lista de dicionário com N chaves sendo
            que a unica chave de interesse é o "ID".
        """
        def getProduto(produto_id: int) -> object:
            """
                param: produto_id (ID da api)
                return: Objeto Produto (table)
                Objective: Buscar ou inserir o produto_id na tabela Produto.
            """
            tb_produto = Produto.objects.get_or_create(produto_id=produto_id) #inserindo/buscando product_id na tabela produto
            return tb_produto[0]

        produtos = data.get('produtos')
        lst_produtos = []
        if isinstance(produtos, dict):
            lst_produtos.append(getProduto(produtos.get('id')))
        elif isinstance(produtos, list):
            for produto in produtos:
                lst_produtos.append(getProduto(produto.get('id')))

        data['produtos'] = lst_produtos
        return data        

    def to_representation(self, data):
        """
            Customizando a funcao para retornar os valores no layout especificado !
        """
        data = super(FavoritosSerializer, self).to_representation(data)
        lst_produtos = []
        for produto in data['produtos']:
            tb_produto = get_object_or_404(Produto, id=produto) #Buscando id produto
            if getExistsProdutoUrl(tb_produto.produto_id): #valida se o produto existe consultando o link
                lst_produtos.append(getDetalhesProduto(tb_produto.produto_id)) #Criando dicionario com detalhes do produto
        data['produtos'] = lst_produtos
   
        return data
        

    def create(self, validated_data):
        """
            Re-escrevendo o metodo create() para ter um controle de cliente/produto que
            ja existe ou não na tabela de Favoritos.
            Se o cliente já existir em Favoritos sera feito apenas o append dos novos
            produtos na sua lista de favoritos.
            Senão existir o cliente em Favoritos é feito uma criação.
        """
        tb_cliente = get_object_or_404(Cliente, id=validated_data.get('cliente')) #buscando cliente
        if Favorito.objects.filter(cliente=tb_cliente).exists(): #Se cliente ja existir em favoritos e feito somente o append dos novos produtos
            tb_favorito = Favorito.objects.get(cliente=tb_cliente)
            for produto in validated_data.get('produtos'):
                if not Favorito.objects.filter(produtos=produto, cliente=tb_cliente).exists(): #se não contem produto no favorito do cliente é adicionado !
                    tb_favorito.produtos.add(produto)
                    tb_favorito.save()
        else:
            tb_favorito = Favorito.objects.create(cliente=tb_cliente) #criando um novo favorito
            tb_favorito.produtos.set(validated_data.get('produtos')) #inserindo os produtos no novo favorito
            tb_favorito.save()
        #raise serializers.ValidationError({"detail": "Já existe uma lista de favorito para esse cliente !"})

        return tb_favorito
