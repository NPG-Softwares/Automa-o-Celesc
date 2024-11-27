from typing import Literal


class BaseControleDownload:
    def __init__(self, data: dict) -> None:
        self.id = data.get("id")
        self.status = data.get("status")
        self.cliente_id = data.get("clienteId")
        self.fornecedor_classe_id = data.get("fornecedorClasseId")
        self.unidade_id = data.get("unidadeId")
        self.fornecedor_id = data.get("fornecedorId")
        self.cnpj_login = data.get("cnpjLogin")
        self.cpf_gestor = data.get("cpfGestor")
        self.email_gestor = data.get("emailGestor")
        self.senha = data.get("senha").strip()
        self.login = data.get("login").strip()
        self.fatura_enviada_por_email = data.get("faturaEnviadaPorEmail")
        self.email_recebimento_fatura = data.get("emailRecebimentoFatura")
        self.dia_verificacao = data.get("diaVerificacao")
        self.nome_configuracao = data.get("nomeConfiguracao")
        self.observacao = data.get("observacao")
        self.ambient: Literal['prod', 'hml', 'qas', 'local']
        self.cnpjs: list[str] = []
        self.contas: list[BaseInvoice] = []  # Empty list for potential future use
        self.unidades: list[BaseUnit] = []  # Empty list for potential future use
        self.tipo_conta_id: str | int | None

    def __repr__(self) -> str:
        return f"BaseClient(ControleDownloadId={self.id}, ClienteId={self.cliente_id})"


class BaseInvoice:
    def __init__(self, data: dict) -> None:
        self.id = data.get("id")
        self.status = data.get("status")
        self.numero_conta = data.get("numeroConta")
        self.tipo_conta_id = data.get("tipoContaId")
        self.fornecedor_classe_id = data.get("fornecedorClasseId")
        self.fornecedor_id = data.get("fornecedorId")
        self.conta_id = data.get("id")
        self.cliente_id = data.get("clienteId")
        self.controle_download_id = data.get("controleDownloadId")
        self.unidade_id = data.get("unidadeId")
        self.login_id = data.get("loginId")
        self.cnpj: str | None

    def __repr__(self) -> str:
        return f"BaseInvoice(conta={self.numero_conta}, contaId={self.conta_id}, status={self.status})"


class BaseUnit:
    def __init__(self, data: dict) -> None:
        self.id = data.get("id")
        self.status = data.get("status")
        self.active = data.get("active")
        self.cliente_adm_id = data.get("clienteAdmId")
        self.login_id = data.get("loginId")
        self.cliente_id = data.get("clienteId")
        self.nome_fantasia = data.get("nomeFantasia")
        self.razao_social = data.get("razaoSocial")
        self.cnpj = data.get("cnpj")
        self.principal = data.get("principal")
        self.logradouro = data.get("logradouro")
        self.logradouro_numero = data.get("logradouroNumero")
        self.logradouro_complemento = data.get("logradouroComplemento")
        self.logradouro_cep = data.get("logradouroCep")
        self.logradouro_bairro = data.get("logradouroBairro")
        self.logradouro_municipio = data.get("logradouroMunicipio")
        self.logradouro_uf = data.get("logradouroUf")
        self.observacao = data.get("observacao")
        self.contas_relacionadas = []


class FaturaInfo:
    def __init__(self):
        self.ArquivoAzureDigital: str
        self.ArquivoAzurePdf: str
        self.AnoReferencia: str
        self.CicloInicio: str
        self.CicloFim: str
        self.ClienteId: int
        self.CodigoBarra: str
        self.ContaId: int
        self.DownloadArquivo: str
        self.Emissao: str
        self.FornecedorClasseId: int
        self.FornecedorId: int
        self.LoginId: int
        self.MesReferencia: str
        self.MedicaoString: str
        self.NomeArquivoDigital: str
        self.NomeArquivoPdf: str
        self.NumeroConta: str
        self.Observacao: str
        self.Status: str
        self.TipoContaId: int
        self.UnidadeId: int
        self.ValorDocumentoDigital: float
        self.ValorDocumentoPDF: float
        self.Vencimento: str

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def get_dict(self) -> dict:
        return self.__dict__
