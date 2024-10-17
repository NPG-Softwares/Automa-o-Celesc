from functools import cache
import re
import json
from time import sleep
from typing import Literal
import requests as req
from retry import retry
from datetime import datetime as dt

from Objects.Obj_ApiSpringBase import BaseControleDownload
from Objects.Obj_PDF_Reader import PDFReader
from Objects.Obj_ApiSpring import API_Spring
from Objects.Obj_ApiSpring import get_logins as _get_logins
from Objects.Obj_UploadFatura import FaturaInfo
from Objects.Obj_ApiBase import APIs, Obj_BaseAPIError
from Objects.Obj_Geral import Access, Account, Contract, Invoice


class LoginError(Exception):
    pass


def login(username: str, password: str) -> dict:
    _login = APIs.Login(username, password)

    payload = json.dumps(_login.data)
    response = req.post(_login.url, data=payload)

    if response.status_code == 200:
        authenticate: dict = response.json()['data']['authenticate']
        if authenticate.get('error') or authenticate.get('errors'):
            raise LoginError(response.status_code, authenticate.get('message'))

        return authenticate
    else:
        raise Obj_BaseAPIError(response.status_code, response.text)


@retry(exceptions=Obj_BaseAPIError, tries=3, delay=10)
def get_access_info(username: str, password: str) -> Access:
    access = Access(username, password)
    access_login = login(access.username, access.password)
    access.token = 'Bearer ' + access_login['login']['accessToken']
    access.userId = access_login['sapAccess']['userId']
    access.partner = access_login['sapAccess']['partner']
    access.accessId = access_login['sapAccess']['accessId']
    access.channel = access_login['sapAccess']['channel']

    return access


@retry(exceptions=Obj_BaseAPIError, tries=3, delay=10)
def get_all_accounts(token: str, userId: str) -> dict:
    _get_all_accounts = APIs.Get_All_Accounts(userId)

    headers = {}
    headers['Authorization'] = token
    headers['Content-Type'] = 'application/json'
    payload = _get_all_accounts.mount_data()
    response = req.post(_get_all_accounts.url, json=payload, headers=headers)

    if response.status_code == 200:
        response_json: dict = response.json()
        if response_json.get('errors'):
            raise Obj_BaseAPIError(response.status_code, response_json.get('errors')[0]['message'])

        if response_json['data']['findOneUserProfile']['categories'] is None:
            return get_all_accounts(token, userId)

        return response_json
    else:
        raise Obj_BaseAPIError(response.status_code, response.text)


def format_all_accounts(accounts: dict) -> list[Account]:
    formated_accounts = []
    accounts = accounts['data']['findOneUserProfile']['categories']
    for account in accounts:
        ac = Account()
        ac.category = account['categoryId']
        ac.subcategory = account['subcategory']
        ac.status = account['status']
        ac.partnerName = account['partnerName']
        ac.partnerNumber = account['partnerNumber']
        ac.partnerDocument = account['partnerDocument']
        formated_accounts.append(ac)

    return formated_accounts


@retry(exceptions=Obj_BaseAPIError, tries=3, delay=10)
def get_all_contracts(token: str, partnerNumber: str, profileType: str) -> dict:
    _get_all_contracts = APIs.Get_All_Contracts(partnerNumber, profileType)

    headers = {}
    headers['Authorization'] = token
    headers['Content-Type'] = 'application/json'

    payload = _get_all_contracts.mount_data()

    response = req.post(_get_all_contracts.url, json=payload, headers=headers)

    if response.status_code == 200:
        response_json: dict = response.json()
        if response_json.get('errors'):
            raise Obj_BaseAPIError(response.status_code, response_json.get('errors')[0]['message'])

        if response_json['data']['allContracts']['contracts'] is None:
            sleep(3)
            return get_all_contracts(token, partnerNumber, profileType)
        return response_json
    else:
        raise Obj_BaseAPIError(response.status_code, response.text)


def format_all_contracts(contracts: dict) -> list[Contract]:
    formated_contracts = []
    list_contracts = contracts['data']['allContracts']['contracts']
    if list_contracts == None:  # noqa
        pass

    for contract in list_contracts:
        ct = Contract()
        ct.partner = contract['partner']
        ct.installation = contract['installation']
        ct.category = contract['category']
        ct.office = contract['office']
        ct.contract = contract['contract']
        ct.contractAccount = contract['contractAccount']
        ct.home = contract['home']
        ct.name = contract['name']
        ct.street = contract['street']
        ct.houseNum = contract['houseNum']
        ct.postCode = contract['postCode']
        ct.city1 = contract['city1']
        ct.city2 = contract['city2']
        ct.region = contract['region']
        ct.country = contract['country']
        ct.alertCode = contract['alertCode']
        ct.alert = contract['alert']
        ct.status = contract['status']
        ct.tarifType = contract['tarifType']
        ct.favorite = contract['favorite']
        ct.denomination = contract['denomination']
        ct.messageHome = contract['messageHome']
        ct.messageCard = contract['messageCard']
        ct.messageType = contract['messageType']
        ct.complement = contract['complement']
        ct.referencePoint = contract['referencePoint']
        ct.generation = contract['generation']
        formated_contracts.append(ct)

    return formated_contracts


@retry(exceptions=Obj_BaseAPIError, tries=3, delay=10)
def get_all_invoices(token: str, partner: str, installation: str) -> dict:
    _get_all_invoices = APIs.Get_All_Invoices(partner, installation)

    headers = {}
    headers['Authorization'] = token
    headers['Content-Type'] = 'application/json'

    payload = _get_all_invoices.mount_data()

    response = req.post(_get_all_invoices.url, json=payload, headers=headers)

    if response.status_code == 200:
        response_json: dict = response.json()
        if response_json.get('errors'):
            raise Obj_BaseAPIError(response.status_code, response_json.get('errors')[0]['message'])

        return response_json
    else:
        raise Obj_BaseAPIError(response.status_code, response.text)


def format_all_invoices(invoices: dict) -> list[Invoice]:
    formated_invoices = []
    list_invoices = invoices['data']['getAllBills']['bills']
    for invoice in list_invoices:
        if invoice['status'] == 'INATIVO':
            continue

        iv = Invoice()
        iv.protocol = invoice['protocol']
        iv.installation = invoice['installation']
        iv.code = invoice['code']
        iv.dueDate = invoice['dueDate']
        iv.totalAmount = invoice['totalAmount']
        iv.currency = invoice['currency']
        iv.usage = invoice['usage']
        iv.previousUsage = invoice['previousUsage']
        iv.consumption = invoice['consumption']
        iv.compensation = invoice['compensation']
        iv.compensationDate = invoice['compensationDate']
        iv.launchBloqued = invoice['launchBloqued']
        iv.hasActiveInstallment = invoice['hasActiveInstallment']
        iv.channel = invoice['channel']
        iv.serviceCode = invoice['serviceCode']
        iv.accessId = invoice['accessId']
        iv.serviceId = invoice['serviceId']
        iv.partner = invoice['partner']
        iv.billingPeriod = invoice['billingPeriod']
        iv.totalDays = invoice['totalDays']
        iv.flag = invoice['flag']
        iv.readType = invoice['readType']
        iv.availability = invoice['availability']
        iv.demandaContr = invoice['demandaContr']
        iv.demandaNp = invoice['demandaNp']
        iv.demandaFp = invoice['demandaFp']
        iv.consumoFatNp = invoice['consumoFatNp']
        iv.consumoFatFp = invoice['consumoFatFp']
        iv.mediaConsFatNp = invoice['mediaConsFatNp']
        iv.mediaConsFatFp = invoice['mediaConsFatFp']
        iv.consumoRegNp = invoice['consumoRegNp']
        iv.consumoRegFp = invoice['consumoRegFp']
        iv.mediaConsRegNp = invoice['mediaConsRegNp']
        iv.mediaConsRegFp = invoice['mediaConsRegFp']
        iv.mediaValor = invoice['mediaValor']
        iv.flagId = invoice['flagId']
        iv.status = invoice['status']
        iv.readTypeId = invoice['readTypeId']
        iv.avalabilityId = invoice['avalabilityId']
        iv.codigoDeBarras = invoice['codigoDeBarras']
        iv.qrCode = invoice['qrCode']
        iv.positionRead = invoice['positionRead']
        iv.averageConsumption = invoice['averageConsumption']
        iv.intermediateConsumptionBilled = invoice['intermediateConsumptionBilled']
        iv.intermediateConsumptionReg = invoice['intermediateConsumptionReg']
        iv.intermediateAverageConsBilled = invoice['intermediateAverageConsBilled']
        iv.intermediateAverageConsReg = invoice['intermediateAverageConsReg']
        iv.reservedConsumption = invoice['reservedConsumption']
        iv.averageReservedConsumption = invoice['averageReservedConsumption']
        iv.intermediateGeneratedConsumption = invoice['intermediateGeneratedConsumption']
        iv.generatedConsumptionNP = invoice['generatedConsumptionNP']
        iv.generatedConsumption = invoice['generatedConsumption']
        iv.reservedGeneratedConsumption = invoice['reservedGeneratedConsumption']
        iv.generatedConsumptionFP = invoice['generatedConsumptionFP']
        iv.averageGeneratedCons = invoice['averageGeneratedCons']
        iv.averageGeneratedConsNP = invoice['averageGeneratedConsNP']
        iv.averageGeneratedConsFP = invoice['averageGeneratedConsFP']
        iv.averageIntermediateGeneratedCons = invoice['averageIntermediateGeneratedCons']
        iv.averageReservedGeneratedCons = invoice['averageReservedGeneratedCons']

        formated_invoices.append(iv)

    return formated_invoices


@retry(exceptions=Obj_BaseAPIError, tries=3, delay=10)
def get_bt_invoice(token: str, contractAccount: str, partner: str,
                   acessId: str, invoiceId: str, tr=0):
    _get_bt_invoice = APIs.Get_Invoice(contractAccount, partner,
                                       acessId, invoiceId)

    headers = {}
    headers['Authorization'] = token
    headers['Content-Type'] = 'application/json'

    payload = _get_bt_invoice.mount_data()

    response = req.post(_get_bt_invoice.url, json=payload, headers=headers)

    if response.status_code == 200:
        response_json: dict = response.json()
        if response_json.get('errors'):
            raise Obj_BaseAPIError(response.status_code, response_json.get('errors')[0]['message'])

        if response_json['data']['duplicateBill']['invoiceBase64'] is None:
            if tr == 3:
                raise Exception('Erro ao buscar fatura')
            return get_bt_invoice(token, contractAccount, partner, acessId, invoiceId, tr + 1)

        return response_json
    else:
        raise Obj_BaseAPIError(response.status_code, response.text)


def read_pdf(byte_file: bytes):
    obj_pdf = PDFReader(byte_file)
    pdf = obj_pdf.read_pdf()
    infos = {}

    pages = obj_pdf.get_pages()
    for page in pages:
        text = obj_pdf.get_text(pdf, page)

        emissao = re.findall(r'\d\d/\d\d/\d\d\d\d\nDATA EMISSAO', text)[0][:10]
        infos['emissao'] = emissao
        ciclo: str = re.findall(r'\d\d/\d\d/\d\d\d\d\n\d\d/\d\d/\d\d\d\d', text)[0]
        ciclo: str = ciclo.split('\n')

        infos['inicioCiclo'] = ciclo[0]
        infos['fimCiclo'] = ciclo[1]

        return infos


def get_logins(ambient: Literal['prod', 'hml'] = 'prod') -> list[BaseControleDownload]:
    logins = _get_logins(name='CELESC', ambient=ambient)

    return logins


@cache
def get_account_type_id(login: BaseControleDownload) -> int:
    api = API_Spring(ambient=login.ambient)
    id = api.get_account_type_id(name='ENERGIA')
    return id


def create_invoice_object(login: BaseControleDownload, account: Account,
                          contract: Contract, invoice: Invoice,
                          pdf_infos: dict, byte_file: bytes) -> tuple[FaturaInfo, list]:
    def format_date(date: str, input_format: str = '%Y-%m-%d',
                    output_format: str = '%Y-%m-%dT%H:%M:%S') -> str:
        return dt.strptime(date, input_format).strftime(output_format)

    now = dt.now().strftime('%Y-%m-%dT%H:%M:%S')

    obj_account = None
    for acc in login.contas:
        if acc.numero_conta == invoice.installation:
            obj_account = acc
            break

    inv = FaturaInfo()
    inv.AnoReferencia = invoice.billingPeriod[:4]
    inv.CodigoBarra = invoice.codigoDeBarras
    inv.CicloInicio = format_date(pdf_infos['inicioCiclo'], '%d/%m/%Y')
    inv.CicloFim = format_date(pdf_infos['fimCiclo'], '%d/%m/%Y')
    inv.ClienteId = login.cliente_id
    inv.DownloadArquivo = now
    inv.Emissao = format_date(pdf_infos['emissao'], '%d/%m/%Y')
    inv.FornecedorClasseId = login.fornecedor_classe_id
    inv.FornecedorId = login.fornecedor_id
    inv.LoginId = 1
    inv.MesReferencia = invoice.billingPeriod[5:7]
    inv.MedicaoString = invoice.usage
    inv.NumeroConta = invoice.installation
    inv.Status = "PENDENTE"
    inv.ValorDocumentoPDF = invoice.totalAmount
    inv.Vencimento = format_date(invoice.dueDate)

    if obj_account:
        if obj_account.status != 'ATIVO':
            return None, None

        inv.ContaId = obj_account.conta_id
        inv.TipoContaId = obj_account.tipo_conta_id
        inv.UnidadeId = obj_account.unidade_id
    else:
        inv.TipoContaId = get_account_type_id(login)
        inv.UnidadeId = login.unidade_id

    fat_name = f'CELESC_{format_date(invoice.dueDate, output_format="%d%m%y")}_{inv.NumeroConta}.pdf'
    inv.ArquivoAzurePdf = fat_name
    inv.NomeArquivoPdf = fat_name

    files = [(fat_name, byte_file, 'application/pdf')]

    return inv, files


def upload_invoice(invoice: FaturaInfo, files: list, platform) -> None:
    payload = invoice.__dict__
    API_Spring(platform).up_invoice(payload, files)
