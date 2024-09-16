class Access:
    def __init__(self, username: str, password: str):
        self.username: str = username
        self.password: str = password
        self.token: str = None
        self.userId: str = None
        self.partner: str = None
        self.accessId: str = None
        self.channel: str = None


class Account:
    def __init__(self):
        self.category: str
        self.subcategory: str
        self.status: str
        self.partnerName: str
        self.partnerNumber: str
        self.partnerDocument: str


class Contract:
    def __init__(self):
        self.partner: str
        self.installation: str
        self.category: str
        self.office: str
        self.contract: str
        self.contractAccount: str
        self.home: str
        self.name: str
        self.street: str
        self.houseNum: str
        self.postCode: str
        self.city1: str
        self.city2: str
        self.region: str
        self.country: str
        self.alertCode: str
        self.alert: str
        self.status: str
        self.tarifType: str
        self.favorite: str
        self.denomination: str
        self.messageHome: str
        self.messageCard: str
        self.messageType: str
        self.complement: str
        self.referencePoint: str
        self.generation: str


class Invoice:
    def __init__(self):
        self.protocol: str
        self.installation: str
        self.code: str
        self.dueDate: str
        self.totalAmount: str
        self.currency: str
        self.usage: str
        self.previousUsage: str
        self.consumption: str
        self.compensation: str
        self.compensationDate: str
        self.compensationBloqued: str
        self.launchBloqued: str
        self.hasActiveInstallment: str
        self.channel: str
        self.serviceCode: str
        self.accessId: str
        self.serviceId: str
        self.partner: str
        self.billingPeriod: str
        self.totalDays: str
        self.flag: str
        self.readType: str
        self.availability: str
        self.demandaContr: str
        self.demandaNp: str
        self.demandaFp: str
        self.consumoFatNp: str
        self.consumoFatFp: str
        self.mediaConsFatNp: str
        self.mediaConsFatFp: str
        self.consumoRegNp: str
        self.consumoRegFp: str
        self.mediaConsRegNp: str
        self.mediaConsRegFp: str
        self.mediaValor: str
        self.flagId: str
        self.status: str
        self.readTypeId: str
        self.avalabilityId: str
        self.codigoDeBarras: str
        self.qrCode: str
        self.positionRead: str
        self.averageConsumption: str
        self.intermediateConsumptionBilled: str
        self.intermediateConsumptionReg: str
        self.intermediateAverageConsBilled: str
        self.intermediateAverageConsReg: str
        self.reservedConsumption: str
        self.averageReservedConsumption: str
        self.intermediateGeneratedConsumption: str
        self.generatedConsumptionNP: str
        self.generatedConsumption: str
        self.reservedGeneratedConsumption: str
        self.generatedConsumptionFP: str
        self.averageGeneratedCons: str
        self.averageGeneratedConsNP: str
        self.averageGeneratedConsFP: str
        self.averageIntermediateGeneratedCons: str
        self.averageReservedGeneratedCons: str
