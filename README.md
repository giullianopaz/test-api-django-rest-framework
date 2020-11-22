# Projeto Teste  - Company Hero

### Desenvolvimento de uma RESTful API utilizando Django REST Framework para gerenciar empresas e seus funcionários.

## Tecnologias utilizadas:

- Django 3.1.3
- Python 3.6.9
- Django REST Framework 3.12.2
- Postgres 12.2

## Referencial da Web API

### Empresa (Company)

**Cadastrar uma empresa**

Request:

> POST →  /companies

```json
{
	"name": "Company Hero LTDA",
	"trading_name": "Company Hero",
	"registered_number": "34532325435224",
	"email": "contatto@ch.com",
	"phone": "999999999"
}
```

Response:

> Status: 200 OK

```json
{
	"pk": 1,
	"name": "Company Hero LTDA",
	"trading_name": "Company Hero",
	"registered_number": "34532325435224",
	"email": "contatto@ch.com",
	"phone": "999999999",
	"employees": []
}
```

**Listar empresas**

Request:

> GET →  /companies

Response:

> Status 200 OK

```json
[
    {
        "pk": 1,
        "name": "Company Hero LTDA",
        "trading_name": "Company Hero",
        "registered_number": "34532325435224",
        "email": "contato@ch.com",
        "phone": "9999999999",
        "employees": []
    },
    {
        "pk": 2,
        "name": "Company Test LTDA",
        "trading_name": "Company Test",
        "registered_number": "34324242432",
        "email": "contato@test.com",
        "phone": "9999999999",
        "employees": [
            {
                "pk": 1,
                "username": "employee1",
                "email": "employee@email.com",
                "first_name": "Fulando",
                "last_name": "de Tal",
                "companies": [
                    1
                ]
            }
        ]
    }
]
```

**Buscar empresa**

Request:

> GET →  /companies/2/

Response:

> Status 200 OK

```json
{
    "pk": 2,
    "name": "Company Test LTDA",
    "trading_name": "Company Test",
    "registered_number": "34324242432",
    "email": "contato@test.com",
    "phone": "9999999999",
    "employees": [
        {
            "pk": 1,
            "username": "employee1",
            "email": "employee@email.com",
            "first_name": "Fulando",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        }
    ]
}
```

**Editar dados de uma empresa**

Request:

> PUT →  /companies/2/

```json
{
    "name": "Company Test LTDA",
    "trading_name": "Company Test",
    "registered_number": "34324242432",
    "email": "updated_email_contato@test.com",
    "phone": "9999999999",
}
```

Response:

> Status 200 OK

```json
{
    "pk": 2,
    "name": "Company Test LTDA",
    "trading_name": "Company Test",
    "registered_number": "34324242432",
    "email": "updated_email_contato@test.com",
    "phone": "9999999999",
    "employees": [
        {
            "pk": 1,
            "username": "employee1",
            "email": "employee@email.com",
            "first_name": "Fulando",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        }
    ]
}
```

**Editar dados de uma empresa parcialmente**

Request:

> PATCH →  /companies/2/

```json
{    
    "email": "updated_email_contato@test.com"
}
```

Response:

> Status 200 OK

```json
{
    "pk": 2,
    "name": "Company Test LTDA",
    "trading_name": "Company Test",
    "registered_number": "34324242432",
    "email": "updated_email_contato@test.com",
    "phone": "9999999999",
    "employees": [
        {
            "pk": 1,
            "username": "employee1",
            "email": "employee@email.com",
            "first_name": "Fulando",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        }
    ]
}
```

**Deletar empresa**

Request:

> DELETE →  /companies/2/

Response:

> Status 204 NO CONTENT

**Adicionar funcionários à empresa**

É possível adicionar um ou mais funcionários ao mesmo tempo. 

Request:

> POST /companies/1/add_employees/

```json
{
    "employees": [1,2,3]
}
```

Response:

> Status 200 OK

```json
{
    "pk": 1,
    "name": "Company Hero LTDA",
    "trading_name": "Company Hero",
    "registered_number": "34324242432",
    "email": "contato@companyhero.com",
    "phone": "9999999999",
    "employees": [
        {
            "pk": 1,
            "username": "employee1",
            "email": "employee@email.com",
            "first_name": "Fulando",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        },
				{
            "pk": 2,
            "username": "employee2",
            "email": "employee2@email.com",
            "first_name": "Fulando 2",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        },
				{
            "pk": 3,
            "username": "employee3",
            "email": "employee3@email.com",
            "first_name": "Fulando 3",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        }
    ]
}
```

**Atualizar funcionários da empresa**

É possível atualizar um ou mais funcionários ao mesmo tempo. 

Request:

> PUT /companies/1/update_employees/

```json
{
    "employees": [1,2]
}
```

Response:

> Status 200 OK

```json
{
    "pk": 1,
    "name": "Company Hero LTDA",
    "trading_name": "Company Hero",
    "registered_number": "34324242432",
    "email": "contato@companyhero.com",
    "phone": "9999999999",
    "employees": [
        {
            "pk": 1,
            "username": "employee1",
            "email": "employee@email.com",
            "first_name": "Fulando",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        },
				{
            "pk": 2,
            "username": "employee2",
            "email": "employee2@email.com",
            "first_name": "Fulando 2",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        }
    ]
}
```

**Deletar funcionários da empresa**

É possível deletar um ou mais funcionários ao mesmo tempo. 

Request:

> DELETE /companies/1/delete_employees/

```json
{
    "employees": [1]
}
```

Response:

> Status 200 OK

```json
{
    "pk": 1,
    "name": "Company Hero LTDA",
    "trading_name": "Company Hero",
    "registered_number": "34324242432",
    "email": "contato@companyhero.com",
    "phone": "9999999999",
    "employees": [
				{
            "pk": 2,
            "username": "employee2",
            "email": "employee2@email.com",
            "first_name": "Fulando 2",
            "last_name": "de Tal",
            "companies": [
                1
            ]
        }
    ]
}
```

**Limpar, deletar todos os funcionários da empresa**

Request:

> DELETE /companies/1/clean_employees/

Response:

> Status 200 OK

```json
{
    "pk": 1,
    "name": "Company Hero LTDA",
    "trading_name": "Company Hero",
    "registered_number": "34324242432",
    "email": "contato@companyhero.com",
    "phone": "9999999999",
    "employees": []
}
```

### Usuário (User)

**Cadastrar um usuário**

Request:

> POST →  /users

```json
{
    "password": "secret",
    "username": "giullianopaz",
    "email": "giulliano@email.com",
    "first_name": "Giulliano",
    "last_name": "Paz"
}
```

Response:

> Status: 200 OK

```json
{
    "pk": 1,
    "username": "giullianopaz",
    "email": "giulliano@email.com",
    "first_name": "Giulliano",
    "last_name": "Paz",
    "companies": []
}
```

**Listar usuários**

Request:

> GET →  /users

Response:

> Status 200 OK

```json
[
    {
        "pk": 1,
        "username": "giullianopaz",
        "email": "giulliano@email.com",
        "first_name": "Giulliano",
        "last_name": "Paz",
        "companies": []
    },
    {
        "pk": 2,
        "username": "fulano",
        "email": "fulano@email.com",
        "first_name": "Fulano",
        "last_name": "de Tal",
        "companies": [
            1,
            2
        ]
    }
]
```

**Buscar usuário**

Para buscar um usuário, usa-se o *username* dele.

Request:

> GET →  /users/fulano/

Response:

> Status 200 OK

```json
{
    "pk": 2,
    "username": "fulano",
    "email": "fulano@email.com",
    "first_name": "Fulano",
    "last_name": "de Tal",
    "companies": [
        1,
        2
    ]
}
```

**Editar dados de um usuário**

Request:

> PUT →  /users/giullianopaz/

```json
{
	"password": "secret",
	"username": "giullianopaz",
	"email": "updated_giulliano@email.com",
	"first_name": "Giulliano",
	"last_name": "Paz"
}
```

Response:

> Status 200 OK

```json
{
	"pk": 1,
	"username": "giullianopaz",
	"email": "updated_giulliano@email.com",
	"first_name": "Giulliano",
	"last_name": "Paz",
	"companies": []
}
```

**Editar dados de um usuário parcialmente**

Request:

> PATCH →  /users/giullianopaz/

```json
{    
    "email": "updated_email_contato@test.com"
}
```

Response:

> Status 200 OK

```json
{
	"pk": 1,
	"username": "giullianopaz",
	"email": "updated_giulliano@email.com",
	"first_name": "Giulliano",
	"last_name": "Paz",
	"companies": []
}
```

**Deletar usuário**

Request:

> DELETE →  /users/fulano/

Response:

> Status 204 NO CONTENT

**Adicionar empresas ao usuário**

É possível adicionar uma ou mais empresas ao mesmo tempo. 

Request:

> POST /users/giullianopaz/add_companies/

```json
{
    "companies": [1,2,3]
}
```

Response:

> Status 200 OK

```json
{
	"pk": 1,
	"username": "giullianopaz",
	"email": "updated_giulliano@email.com",
	"first_name": "Giulliano",
	"last_name": "Paz",
	"companies": [
		1,
		2,
		3
	]
}
```

**Atualizar empresas do usuário**

É possível atualizar uma ou mais empresas ao mesmo tempo. 

Request:

> PUT /users/giullianopaz/update_companies/

```json
{
    "companies": [1,3]
}
```

Response:

> Status 200 OK

```json
{
	"pk": 1,
	"username": "giullianopaz",
	"email": "updated_giulliano@email.com",
	"first_name": "Giulliano",
	"last_name": "Paz",
	"companies": [
		1,
		3
	]
}
```

**Deletar empresas do empresa**

É possível deletar uma ou mais empresas ao mesmo tempo. 

Request:

> DELETE /users/giullianopaz/delete_companies/

```json
{
    "companies": [1]
}
```

Response:

> Status 200 OK

```json
{
	"pk": 1,
	"username": "giullianopaz",
	"email": "updated_giulliano@email.com",
	"first_name": "Giulliano",
	"last_name": "Paz",
	"companies": [
		3
	]
}
```

**Limpar, deletar todas as empresa do usuário**

Request:

> DELETE /users/giullianopaz/clean_companies/

Response:

> Status 200 OK

```json
{
	"pk": 1,
	"username": "giullianopaz",
	"email": "updated_giulliano@email.com",
	"first_name": "Giulliano",
	"last_name": "Paz",
	"companies": []
}
```