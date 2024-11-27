import os
import dotenv
import warnings
import requests as req

from typing import Literal
from functools import cache

from Objects.Obj_ApiSpringBase import BaseControleDownload, BaseInvoice, BaseUnit

dotenv.load_dotenv()
warnings.filterwarnings("ignore")


# ------------------------------------------------- Exceções
class AmbientError(Exception):
    pass


class LoginError(Exception):
    pass


class UploadError(Exception):
    pass


class API_Spring_Error(Exception):
    pass


# ------------------------------------------------- Classes
class API_Spring:
    _token = {}

    def __init__(self, ambient: Literal['prod', 'hml', 'qas', 'local']) -> None:
        self.ambient = ambient
        self.__get_envs__()

        if API_Spring._token.get(self.ambient, None):
            self.token = API_Spring._token.get(self.ambient)

        else:
            self.token = API_Spring._token.get(self.ambient) or self.get_token()
            API_Spring._token[self.ambient] = self.token

    def __get_envs__(self) -> None:
        match self.ambient:
            case 'hml' | 'hms':
                self.email = os.getenv('hml_login_email')
                self.password = os.getenv('hml_login_password')
                self.end_token = os.getenv('hml_end_get_token')
                self.end_logins = os.getenv('hml_end_logins')
                self.end_up_invoice = os.getenv('hml_end_up_invoice')
                self.end_get_invoices = os.getenv('hml_end_get_invoices')
                self.end_send_error_log = os.getenv('hml_end_send_error_log')
                self.end_get_fornecedores_id = os.getenv('hml_end_get_fornecedores_id')
                self.end_get_unidades_by_id = os.getenv('hml_end_get_unidades_by_id')
                self.end_get_account_type_id = os.getenv('hml_end_get_account_type_id')
                self.end_up_invoice_with_digital = os.getenv('hml_end_up_invoice_with_digital')
                self.referer = 'https://portal-hms.springsmartsolutions.com/'

            case 'prod':
                self.email = os.getenv('prod_login_email')
                self.password = os.getenv('prod_login_password')
                self.end_token = os.getenv('prod_end_get_token')
                self.end_logins = os.getenv('prod_end_logins')
                self.end_up_invoice = os.getenv('prod_end_up_invoice')
                self.end_get_invoices = os.getenv('prod_end_get_invoices')
                self.end_send_error_log = os.getenv('prod_end_send_error_log')
                self.end_get_fornecedores_id = os.getenv('prod_end_get_fornecedores_id')
                self.end_get_unidades_by_id = os.getenv('prod_end_get_unidades_by_id')
                self.end_get_account_type_id = os.getenv('prod_end_get_account_type_id')
                self.end_up_invoice_with_digital = os.getenv('prod_end_up_invoice_with_digital')
                self.referer = 'https://portal.springsmartsolutions.com.br/'

            case 'qas':
                self.email = os.getenv('qas_login_email')
                self.password = os.getenv('qas_login_password')
                self.end_token = os.getenv('qas_end_get_token')
                self.end_logins = os.getenv('qas_end_logins')
                self.end_up_invoice = os.getenv('qas_end_up_invoice')
                self.end_get_invoices = os.getenv('qas_end_get_invoices')
                self.end_send_error_log = os.getenv('qas_end_send_error_log')
                self.end_get_fornecedores_id = os.getenv('qas_end_get_fornecedores_id')
                self.end_get_unidades_by_id = os.getenv('qas_end_get_unidades_by_id')
                self.end_get_account_type_id = os.getenv('qas_end_get_account_type_id')
                self.end_up_invoice_with_digital = os.getenv('qas_end_up_invoice_with_digital')
                self.referer = 'https://portal-hms.springsmartsolutions.com/'

            case 'local':
                self.email = os.getenv('local_login_email')
                self.password = os.getenv('local_login_password')
                self.end_token = os.getenv('local_end_get_token')
                self.end_logins = os.getenv('local_end_logins')
                self.end_up_invoice = os.getenv('local_end_up_invoice')
                self.end_get_invoices = os.getenv('local_end_get_invoices')
                self.end_send_error_log = os.getenv('local_end_send_error_log')
                self.end_get_fornecedores_id = os.getenv('local_end_get_fornecedores_id')
                self.end_get_unidades_by_id = os.getenv('local_end_get_unidades_by_id')
                self.end_get_account_type_id = os.getenv('local_end_get_account_type_id')
                self.end_up_invoice_with_digital = os.getenv('local_end_up_invoice_with_digital')
                self.referer = 'https://portal-hms.springsmartsolutions.com/'

            case _:
                raise AmbientError('Ambiente inválido, utilize os ambientes '
                                   '[hml | prod | qas | local] sendo "hml" para homologação, '
                                   '"prod" para produção, "qas" para servidor teste e '
                                   '"local" para ambiente local.')

    def get_controle_download(self, fornecedor_id: str = None, cliente_id: str = None) -> dict:
        url = self.end_logins
        headers = {}
        headers['Authorization'] = self.token
        headers['Referer'] = self.referer

        params = {}
        params['status'] = 'ATIVO'

        if fornecedor_id:
            params['fornecedorId'] = fornecedor_id

        if cliente_id:
            params['clienteId'] = cliente_id

        r = req.get(url, headers=headers, params=params, verify=False)

        return r.json()

    def get_fornecedores_by_name(self, name: str) -> list:
        url = self.end_get_fornecedores_id
        headers = {}
        headers['Authorization'] = self.token
        headers['Referer'] = self.referer

        params = {}
        params['NomeFantasia'] = name

        r = req.get(url, headers=headers, params=params, verify=False)

        return [(x['id'], x['clienteAdmId']) for x in r.json()['data']]

    def get_unidade_by_id(self, id: int) -> list:
        url = self.end_get_unidades_by_id
        url = url.replace('{id}', str(id))
        headers = {}
        headers['Authorization'] = self.token
        headers['Referer'] = self.referer

        r = req.get(url, headers=headers, verify=False)

        return r.json()

    def get_account_type_id(self, name: str, client_id: int = None) -> int:
        url = self.end_get_account_type_id

        headers = {}
        headers['Authorization'] = self.token
        headers['Referer'] = self.referer

        params = {}
        params['Nome'] = name

        if client_id:
            params['ClienteId'] = client_id

        r = req.get(url, headers=headers, params=params, verify=False)

        if r.status_code == 200:
            return r.json()['data'][0]['id']

        elif r.status_code == 401:
            self.token = self.get_token()
            API_Spring._token[self.ambient] = self.token
            return self.get_account_type_id(name, client_id)

    def new_request(self, method, **kwargs) -> dict:
        if not kwargs.get('headers'):
            kwargs['headers'] = {}

        kwargs['headers']['Authorization'] = self.token
        kwargs['headers']['Referer'] = self.referer

        r = req.request(method, **kwargs, verify=False)

        if r.status_code == 200:
            return r.json()

        elif r.status_code == 401:
            self.token = self.get_token()
            API_Spring._token[self.ambient] = self.token
            return self.new_request(method, **kwargs)
        else:
            raise API_Spring_Error(f'Erro [{r.status_code}]: {r.text}')

    @cache
    def get_token(self) -> str:
        """
        Retrieves the bearer token for the specified email and password.

        Args:
            self (API_Spring): The API_Spring instance.

        Returns:
            str: The bearer token.

        Raises:
            LoginError: If there was an error during the login process.
        """
        credentials = {
            'email': self.email,
            'password': self.password
        }

        headers = {}
        headers['Referer'] = self.referer

        r = req.post(self.end_token, json=credentials, headers=headers, verify=False)

        if r.status_code == 200:
            return "Bearer " + r.json()['token']
        else:
            raise LoginError(f'Erro [{r.status_code}]: {r.text}')

    def get_accounts(self, client: BaseControleDownload) -> dict:
        url = self.end_get_invoices
        headers = {}
        headers['Authorization'] = self.token
        headers['Referer'] = self.referer

        params = {}
        params['ClienteId'] = client.cliente_id

        r = req.get(url, headers=headers, params=params, verify=False)

        if r.status_code == 401:
            self.token = self.get_token()
            API_Spring._token[self.ambient] = self.token
            return self.get_accounts(client)

        return r.json()

    def up_invoice(self, payload: dict, files: list[tuple], with_digital: bool = False) -> None:
        """
        Uploads an invoice to the API using the provided payload and files.

        Args:
            payload (dict): The payload containing the invoice data.
            files (list[tuple]): List of files to be uploaded in the form [(name, content, mime_type)].
            with_digital (bool): Determines the endpoint to be used.

        Raises:
            req.exceptions.ContentDecodingError: If a file is too large to be sent.
            req.exceptions.RequestException: If there is an error during the upload process.
        """
        url = self.end_up_invoice_with_digital if with_digital else self.end_up_invoice

        headers = {'Authorization': self.token}
        headers['Referer'] = self.referer

        # Prepara os arquivos para o envio em um único form-data
        form_files = [
            ('files', (file[0], file[1], file[2]))
            for file in files
        ]

        # Faz a requisição POST com o payload e os arquivos
        response = req.post(url, headers=headers, data=payload, files=form_files, verify=False)

        if response.status_code == 200:
            print('Arquivos enviados com sucesso.')
        elif response.status_code == 413:
            raise req.exceptions.ContentDecodingError('Um ou mais arquivos são muito grandes para serem enviados.')
        elif response.status_code == 401:
            # Atualiza o token e tenta novamente
            self.token = self.get_token()
            API_Spring._token[self.ambient] = self.token
            self.up_invoice(payload, files, with_digital)
        else:
            raise req.exceptions.RequestException(f'Erro [{response.status_code}]: {response.text}')

    def send_error_log(self, title: str, message: str, stacktrace: str,
                       origin: str, status: Literal['warning', 'error', 'info', 'success'] = 'error',
                       login_id: int = 1, cliente_adm_id: int | None = None) -> None:
        url = self.end_send_error_log
        headers = {}
        headers['Authorization'] = self.token
        headers['Referer'] = self.referer

        payload = {
            'titulo': title,
            'mensagem': message,
            'infoCode': stacktrace,
            'origem': origin,
            'status': status,
            'loginId': login_id,
            'clienteAdmId': cliente_adm_id
        }

        r = req.post(url, headers=headers, json=payload, verify=False)

        if r.status_code == 200:
            print('Log enviado com sucesso!')
        elif r.status_code == 401:
            self.token = self.get_token()
            API_Spring._token[self.ambient] = self.token
            self.send_error_log(title, message, stacktrace, origin, status, login_id, cliente_adm_id)
        else:
            print('Payload:', payload)
            raise UploadError(f'Erro [{r.status_code}]: {r.text}')


def filter_controle_download(api: API_Spring, list_controles_download: dict,
                             fornecedores_ids: list[int], ambient: Literal['prod', 'hml', 'qas', 'local']) -> list[BaseControleDownload]:
    filtered_accounts: list[str] = []
    filtered_controle_download: list[BaseControleDownload] = []

    assert len(list_controles_download) > 0, 'Nenhum login encontrado.'
    for controle_download in list_controles_download:

        if controle_download['senha'] == '' or controle_download['senha'] is None:
            continue

        obj_controle_download = BaseControleDownload(controle_download)
        obj_controle_download.ambient = ambient

        accounts = []
        accounts = api.get_accounts(obj_controle_download)['data']

        for account in accounts:
            obj_account = BaseInvoice(account)

            if obj_account.numero_conta in filtered_accounts:
                continue

            if obj_account.fornecedor_id not in fornecedores_ids:
                continue

            if obj_account.controle_download_id != obj_controle_download.id:
                continue

            obj_controle_download.contas.append(obj_account)
            filtered_accounts.append(obj_account.numero_conta)

        unidades = [x.unidade_id for x in obj_controle_download.contas]
        unidades = list(set(unidades))

        for unidade_id in unidades:
            if not unidade_id:
                continue
                # raise API_Spring_Error('Unidade não encontrada.')

            unidade: dict = api.get_unidade_by_id(unidade_id)
            if unidade == ['Cliente nào encontrado']:
                continue

            obj_unidade = BaseUnit(unidade)
            obj_controle_download.unidades.append(obj_unidade)

        obj_controle_download.unidades = list(set(obj_controle_download.unidades))
        obj_controle_download.cnpjs = list(set([x.cnpj for x in obj_controle_download.unidades]))

        filtered_controle_download.append(obj_controle_download)

    return filtered_controle_download


def get_logins(name: str, ambient: Literal['prod', 'hml', 'qas', 'local'] = 'prod') -> list[BaseControleDownload]:
    api = API_Spring(ambient)
    fornecedores_ids = api.get_fornecedores_by_name(name)
    list_fornecedores_ids = list(set([x for x, _ in fornecedores_ids]))
    controle_download_list = []

    for fornecedor_id, cliente_id in fornecedores_ids:
        all_controle_download = api.get_controle_download(fornecedor_id=fornecedor_id, cliente_id=cliente_id)['data']
        controle_download_list.extend(all_controle_download)

    controle_download = filter_controle_download(api, controle_download_list, list_fornecedores_ids, ambient=ambient)
    return controle_download


def send_log(ambient: Literal['prod', 'hml', 'qas', 'local'], title: str, message: str, stacktrace: str,
             origin: str, cliente_adm_id: int | None, status: Literal['warning', 'error', 'info', 'success'] = 'error',
             login_id: int = 1):
    api = API_Spring(ambient)
    api.send_error_log(
        title=title,
        message=message,
        stacktrace=stacktrace,
        origin=origin,
        status=status,
        login_id=login_id,
        cliente_adm_id=cliente_adm_id
    )
