

# Projeto de Automação RPA na Plataforma da Celesc

## Descrição do Projeto

Este projeto visa automatizar processos na plataforma da Celesc utilizando Robotic Process Automation (RPA). O objetivo é aumentar a eficiência e reduzir o tempo de execução de tarefas manuais. O script tem como função baixar os PDF's da plataforma da Celesc, processar os arquivos, coletar informações do PDF e subir na plataforma nova da Spring (Connect).

## Tecnologias Utilizadas

* Python como linguagem de programação
* Bibliotecas como `requests` e `json` para interagir com a API da Celesc
* Ferramentas como `poetry` para gerenciamento de dependências
* Docker para containerização do projeto

## Estrutura do Projeto

O projeto está organizado em pastas e arquivos da seguinte forma:

* `app`: Pasta principal do projeto, contendo os arquivos de código Python
	+ `main.py`: Arquivo principal de execução do projeto
	+ `functions.py`: Pasta contendo funções auxiliares utilizadas no projeto
	+ `Objects`: Pasta contendo classes e objetos utilizados no projeto
		- `Obj_Logger.py`: Classe para gerenciamento de logs
		- `Obj_ApiSpring.py`: Classe para interagir com a API da Spring
* `api_postman`: Pasta contendo API da Celesc
	+ `CELESC.postman_collection.json`: Arquivo da API da Celesc para abrir no postman
* `Dockerfile`: Arquivo de configuração do Docker para containerização do projeto

## Funcionalidades do Projeto

* Automação de processos na plataforma da Celesc
* Integração com a API da Celesc para coleta de dados e execução de ações
* Gerenciamento de logs para monitoramento e depuração do projeto

## Configuração do .env

É extremamente importante definir o .env do script, para isso, cria um arquivo .env e preencha os seguintes campos:


**Produção**
* prod_login_email
* prod_login_password
* prod_end_get_token
* prod_end_get_fornecedores_id
* prod_end_get_unidades_by_id
* prod_end_logins
* prod_end_get_invoices
* prod_end_up_invoice
* prod_end_send_error_log
* prod_end_get_account_type_id

**Homologação**
* hml_login_email
* hml_login_password
* hml_end_get_token
* hml_end_get_fornecedores_id
* hml_end_get_unidades_by_id
* hml_end_logins
* hml_end_get_invoices
* hml_end_up_invoice
* hml_end_send_error_log
* hml_end_get_account_type_id


## Como Executar o Projeto

1. Clone o repositório do projeto
2. Instale o poetry com o comando `pip install poetry`
3. Instale as dependências do projeto utilizando `poetry install`
4. Execute o projeto utilizando `poetry run python main.py`