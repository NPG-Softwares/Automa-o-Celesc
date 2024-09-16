import base64
from time import sleep
from datetime import datetime as dt

from functions import LoginError, BaseClient
from functions import (get_access_info, get_bt_invoice,
                       get_all_accounts, format_all_accounts,
                       get_all_contracts, format_all_contracts,
                       get_all_invoices, format_all_invoices,
                       read_pdf, create_invoice_object,
                       get_logins, upload_invoice)

from Objects.Obj_Logger import Logger


class Temp_Log:
    readed_accounts: list = []
    readed_contracts: list = []
    readed_invoices: list = []


def decode_file(coded_text: str | None):
    if not coded_text:
        return None

    return base64.b64decode(coded_text)


def init_process(login: BaseClient, platform: str):
    now = dt.now()
    init = dt(now.year, now.month, 1)

    log = Logger('logger.gz', './data')
    readed_files = log.to_list()

    portal_accounts = [x.numero_conta for x in login.contas]

    access = get_access_info(login.login, login.senha)

    accounts = get_all_accounts(access.token, access.userId)
    accounts = format_all_accounts(accounts)

    for account in accounts:
        if account in Temp_Log.readed_accounts:
            continue

        print(account.partnerName)
        contracts = get_all_contracts(access.token, account.partnerNumber, account.category)
        contracts = format_all_contracts(contracts)

        for contract in contracts:
            if contract in Temp_Log.readed_contracts:
                continue

            print('\t', contract.partner, contract.installation, contract.status)
            invoices = get_all_invoices(access.token, contract.partner, contract.installation)
            invoices = format_all_invoices(invoices)

            for invoice in invoices:
                if invoice in Temp_Log.readed_invoices:
                    continue

                if invoice.installation not in portal_accounts:
                    continue

                due = dt.strptime(invoice.dueDate, '%Y-%m-%d')
                if due >= init:
                    print('\t\t', invoice.code, invoice.dueDate)
                    if not invoice.code:
                        raise Exception(f'Fatura sem Código: {invoice.code} | {invoice.dueDate} | {invoice.installation}')

                    if invoice.code in readed_files:
                        print('\t\t\tFatura ja enviada. Continuando...')
                        continue

                    bt_invoice = get_bt_invoice(access.token, contract.contractAccount,
                                                invoice.partner.rjust(10, '0'),
                                                access.accessId, invoice.code)

                    fileb64 = bt_invoice['data']['duplicateBill']['invoiceBase64']
                    decoded_file = decode_file(fileb64)

                    pdf_info = read_pdf(decoded_file)

                    obj_invoice, files = create_invoice_object(
                        login, account, contract,
                        invoice, pdf_info, decoded_file
                    )

                    upload_invoice(obj_invoice, files, platform)

                    sleep(2)

                    log.append(invoice.code)
                Temp_Log.readed_invoices.append(invoice)
            Temp_Log.readed_contracts.append(contract)
        Temp_Log.readed_accounts.append(account)


def main():
    """
    Tenta executar init_process() 5 vezes, esperando 15 segundos entre
    cada tentativa em caso de erro. Se todas as tentativas falharem,
    levanta a exce o da  ltima tentativa.
    """
    platform = 'hml'  # prod | hml
    logins: list[BaseClient] = get_logins(platform)

    tries = 3
    for login in logins:
        for tr in range(tries):
            try:
                print(f'[INFO] - {dt.now()} - Iniciando processo...')
                print(f'Tentativa {tr + 1} de {tries}...')
                init_process(login, platform)
                break

            except LoginError as e:
                print(f'Erro ao acessar o login {login} ({login.login} - {login.senha}). CNPJ: {login.cnpj_login}')
                print(f'[ERROR] - {dt.now()} - {e}')
                break

            except Exception as e:
                if tr == tries - 1:
                    raise e

                sleep(15)


if __name__ == '__main__':
    main()
