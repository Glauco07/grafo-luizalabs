# grafo-luizalabs

Esse projeto consiste em um serviço web, desenvolvido em python, que utiliza-se do framework [Flask](https://flask.palletsprojects.com/en/2.0.x/) para criar as rotas, e o banco de dados [Dgraph](https://dgraph.io/), um banco escrito em Go, orientado a grafos.

-----

Sumário
=======
* [Requisitos](#requisitos)
* [Instalação](#instalação)
* [Execução](#execução)
* [Rotas](#rotas)
  * [/](#/)
  * [/people](#/people)
  * [/people/name](#/people/name)
  * [/people/name/level2](#/people/name/level2)
* [Código](#código)
  * [Design Patterns](#design-patterns)
    * [repositories](#repositories)
    * [services](#services)
    * [views](#views)
* [Banco de Dados](#banco-de-dados)
* [Docker](#docker)
* [Observações](#observações)
* [Testes](#testes)
  
Requisitos
==========
Para rodar o serviço, é apenas necessário possuir o `docker` instalado.

Execução
========
Na pasta raiz do projeto, execute o comando
```bash
docker-compose -f .\deploy\docker-compose.yaml up -d
```

Para parar de rodar o container, execute o comando
```bash
docker-compose -f .\deploy\docker-compose.yaml down
```

Rotas
=====
Para acessar as rotas, é necessário fazer uma requisição http para os endereços disponibilizados em [localhost:5000](http://localhost:5000)<br><br>

**As rotas disponíveis são:**

/
---

```http
GET /
```
Retorna uma página em branco, útil para verificar se o Flask está rodando, pois independe da resposta esperada de qualquer consulta.

| Status Code | Descrição |
| :--- | :--- |
| 200 | `OK` |

---

/people
-------

```http
GET /people
```
Retorna um `JSON` com todas as pessoas cadastradas no banco.<br>
Caso o nome não esteja cadastrado, retorna um `JSON` vazio.

```javascript
["Vinicius", "Maria", "João", "Luiza", "Carlos", "Ana"]
```

| Status Code | Descrição |
| :--- | :--- |
| 200 | `OK` |

```http
POST /people
```

Recebe um payload no formato `JSON` em que a key é o nome da pessoa que vai ser adicionada, e o value é uma lista de valores representando os amigos dessa pessoa em questão.

Exemplo:
```python
import requests

url = 'http://localhost:5000/people'
requests.post(url, json={"Glauco": ["Carlos", "Ana"]})
```

Formato do payload:
```javascript
payload = {"Glauco": ["Carlos", "Ana"]}
```

| Status Code | Descrição | Stiuação |
| :--- | :--- |  :--- |
| 201 | `CREATED` | Pessoa inserida com sucesso
| 400 | `BAD REQUEST` | Corpo da requisição não é um `JSON` válido ou uma pessoa não pôde ser iserida

---

/people/name
------------

```http
GET /people/{name}
```

Retorna um `JSON` com todas as pessoas que a pessoa de nome {name} conhece.<br>
Substituir {name} por o nome desejado, respeitando acentuação.<br>
Caso seja inserido um nome que não está cadastrado, retorna uma lista vazia.

Exemplo:
```http
http://localhost:5000/people/João
```
Retorno:
```javascript
["Luiza", "Ana"]
```

| Status Code | Descrição
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |

---

/people/name/level2
-------------------

```http
GET /people/{name}/level2
```

Retorna um `JSON` com todas as pessoas que a pessoa de nome {name} não conhece, mas as pessoas que ela conhece, sim.<br>
Substituir {name} por o nome desejado, respeitando acentuação.

Exemplo:
```http
http://localhost:5000/people/João/level2
```
Retorno:
```javascript
["Luiza", "Ana"]
```

| Status Code | Descrição |
| :--- | :--- |
| 200 | `OK` |

---

Design Patterns
---------------
A fim de dividir os serviços em rotinas especializadas, com dependências bem definidas, segui um padrão inspirado no [Composite](https://refactoring.guru/design-patterns/composite), em que utiliza-se uma estrutura em árvore e no [Chain of Resposability](https://refactoring.guru/design-patterns/chain-of-responsibility).<br>
Seguindo esse princípio, o código está dividido em três pastas principais:
* [repositories](#repositories)
* [services](#services)
* [views](#views)

repositories
------------
Contém as funções que interagem diretamente com o banco. A intenção é apenas aplicar um processamento básico, vendo se a resposta obtida condiz com a esperada, e retornar esse valor para a próxima camada.

services
--------
Aplica um tratamento maior sobre os dados, preparando-os em um formato conveniente para a etapa seguinte.

views
-----
É onde encontram-se as funções do Flask responsáveis por definir as rotas e informações relacionadas, tal como corpo da resposta, código de status.<br>
Os dados, após os processamentos, são disponibilizados no formato JSON, seguindo os princípios REST.

Banco de Dados
==============
O banco escolhido para armazenar os dados dos usuários foi o **Dgraph**.<br>
A vantagem de utilizá-lo está na alta performance, além de facilitar a abstração para modelar relações que podem ser vistas como um grafo, tal como neste desafio, onde os nós representam pessoas, e as arestas são as relações entre elas.<br>
Nele, é possível utilizar **GraphQL**, ou **DQL** (sua própria linguagem de consultas, inspirada no Graphql).<br>
Optei por usar apenas o DQL para fazer as consultas e mutações (inserção).

Docker
======
Utilizei o **docker-compose** para criar um deploy com os containeres necessários.<br>
Enquanto um roda o flask, o outro roda o banco.<br>
Ambos são disponibilizados na localhost: o Flask utiliza a porta 5000, e o banco utiliza a porta [8000](http://localhost:8000) para disponibilizar uma interface que permite interação direta com o banco, em que podem ser feitas consultas e visualizar a resposta de forma visual, na forma de grafo; ou mutações.

Observações
===========
O DQL não utiliza o conceito de arestas bilaterais, em que dado que A conhece B, B também conhece A. Entretanto, utilizando o símbolo `~`, é possível ver o outro lado da relação.
Então, dessa forma, utilizo `knows` e `~knows` para representar **conhece** e **é conhecido por**.

Acessando [localhost:8000](http://localhost:8000), é possível visualizar o grafo com as pessoas e as relações entre elas.<br>
Clique em `console`, e insira a seguinte query:

```javascript
{
	people(func: has(name)) {
		name
    knows {
			name
    }
    ~knows {
			name
  	}
	}
}
```

Testes
======
Realizei vários testes de forma manual, a fim de evitar erros, sobretudo nos casos mais comuns.

`GET` em todas as rotas -> retornam listas com nomes, de acordo com o esperado. Lista vazia quando valor não é encontrado no banco<br>
`GET` na rota `/people/name` com nome não registrado no banco -> retorna uma lista vazia<br>
`GET` na rota `/people/name/level2` com nome não registrado no banco -> retorna uma lista vazia<br>
`POST` na rota `/people` com payload sendo um `JSON` vazio -> não aplica mudança nenhuma <br>
`POST` na rota `/people` com payload não sendo um `JSON` -> retorna 400, pois o payload precisa ser um `JSON` <br>
`POST` na rota `/people` com payload sendo um `JSON` válido -> insere uma ou mais pessoas <br>