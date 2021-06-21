**#Desafio Welligton S. De Oliveira**

**Instalação**
-   Requerimento:
    - => Python3.8
    - => Docker

-   Instalação:

    - Criar virtual env e ativar:
        -   $ python3 -m venv env
        -   $ source env/bin/activate (linux)
        -   $ .\Scripts\activate.bat (windows)

    - Baixar projeto do git:
        -   $ git clone https://github.com/wsoliveira/planisto_backend.git

    - Docker
        -   Para subir django e o banco postegres execute:
            -   $ docker-compose up #(subir app e banco)
        -   Você precisa buscar o CONTAINER_ID do Django:
            -   $ docker ps #(Para buscar o CONTAINER_ID)

    - Crie usuário de administração, lembre-se do  CONTAINER_ID:
        -   $ docker exec -it CONTAINER_ID python manage.py createsuperuser
        
    - Testes Unitários !
        -   $ docker exec -it CONTAINER_ID python manage.py test

    - Administração:
        - acesse: http://127.0.0.1:8000/admin/

    
**API's**
        - Documentação: http://127.0.0.1:8000/api/docs

    - API - TOKEN
        - /api/v1/token/ (POST)
            - API responsável pela autenticação do usuário e criação do Token de acesso.
            - payload:
            {
                "email": ...,
                "password": ...,
            }
            - response:
            {
                "refresh": ...,
                "access": ...,
            }
            - Com chave {access} utiliza-la no header da requisição para consumir as apis abaixo: 
            Authorization = 'JWT {access}'

    - API - USUARIOS
        - /api/v1/usuarios/dados/ (GET)
            - Retornar todos os usuários cadastrados
        - /api/v1/usuarios/registra_usuario/ (POST)
            - Para criar um novo usuário.
            - payload:
            {
                "email": ...,
                "nome": ...,
                "is_active": ...,
                "password": ...,
            }
    - API - CLIENTES
        - Metodos GET, POST, PUT e DELETE, utilizar o payload abaixo para o metodo POST e PUT:
        - payload:
        {
            "nome": ...,
            "email": ...,
        }
    - API - FAVORITOS
        - Metodos GET, POST e DELETE.
        - O metodo POST está flexivel para atender as situações:
            - Recebecer uma lista de produtos
            - Receber um unico produto
            - Receber produtos duplicados
            - Receber produtos já favoritados no cliente.
        payload:
	    {
		    "cliente":..., (API_CLIENTE.id)
		    "produtos":{...} ou [{...},{...},{...}]
	    }
        response:
        {
            "id": ...,
            "cliente": ...,
            "produtos": [
                {
                    "title": ...,
                    "image": ...,
                    "price": ...,
                    "link": ...,
                },
                {
                    "title": ...,
                    "image": ...,
                    "price": ...,
                    "link": ...,
                } 
            ]
        }        

