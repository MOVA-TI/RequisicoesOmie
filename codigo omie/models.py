from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, Float, Boolean, Time, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Omie(Base):
    __tablename__ = 'omie'

    id = Column(Integer, primary_key=True)
    cDesCliente = Column(String)
    dDataLancamento = Column(String)
    nSaldo = Column(Float)
    nValorDocumento = Column(Float)
    cDescricao = Column(String)
    nCodBanco = Column(String)
    nNumConta = Column(String)
    nCodAgencia = Column(String)
    cCodCategoria = Column(String)
    cDataInclusao = Column(String)
    cDesCategoria = Column(String)
    cHoraInclusao = Column(String)
    cNatureza = Column(String)
    cNumero = Column(String)
    cObservacoes = Column(String)
    cOrigem = Column(String)
    cSituacao = Column(String)
    cTipoDocumento = Column(String)
    dDataConciliacao = Column(String)
    nCodLancRelac = Column(Float)
    nCodLancamento = Column(Float)
    cParcela = Column(String)
    cRazCliente = Column(String)
    nCodCliente = Column(Float)
    cDocCliente = Column(String)
    cDocumentoFiscal = Column(String)
    cBloqueado = Column(String)