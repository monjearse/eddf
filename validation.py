import os
from typing import Tuple, List, Dict, Any

import xmlschema
from lxml import etree


class NFeValidator:
    """
    Empacota o xmlschema para validar NFe 4.00
    """

    def __init__(self, xsd_path: str = "./schemas/nfe_v4.00.xsd"):
        if not os.path.exists(xsd_path):
            raise FileNotFoundError(
                f"Schema NFe não encontrado em: {xsd_path}"
            )
        self.schema = xmlschema.XMLSchema(xsd_path)

    def validar(self, xml_bytes: bytes) -> Tuple[bool, List[str]]:
        """
        Retorna (eh_valido, lista_de_erros)
        """
        erros: List[str] = []
        try:
            # valida incrementalmente para pegar detalhes
            for err in self.schema.iter_errors(xml_bytes):
                erros.append(str(err))
        except Exception as e:
            erros.append(f"Erro ao validar XML: {e}")

        return (len(erros) == 0, erros)

    def extrair_contexto_basico(self, xml_bytes: bytes) -> Dict[str, Any]:
        """
        Extrai alguns campos simples (ide/emit/dest) só para dar contexto ao LLM.
        """
        contexto: Dict[str, Any] = {}

        try:
            root = etree.fromstring(xml_bytes)
            ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

            ide = root.find(".//nfe:ide", ns)
            emit = root.find(".//nfe:emit", ns)
            dest = root.find(".//nfe:dest", ns)

            if ide is not None:
                contexto["ide.cNF"] = (ide.findtext("nfe:cNF", default="", namespaces=ns) or "").strip()
                contexto["ide.nNF"] = (ide.findtext("nfe:nNF", default="", namespaces=ns) or "").strip()
                contexto["ide.dhEmi"] = (ide.findtext("nfe:dhEmi", default="", namespaces=ns) or "").strip()
                contexto["ide.natOp"] = (ide.findtext("nfe:natOp", default="", namespaces=ns) or "").strip()

            if emit is not None:
                contexto["emit.CNPJ"] = (emit.findtext("nfe:CNPJ", default="", namespaces=ns) or "").strip()
                contexto["emit.xNome"] = (emit.findtext("nfe:xNome", default="", namespaces=ns) or "").strip()

            if dest is not None:
                contexto["dest.CNPJ"] = (dest.findtext("nfe:CNPJ", default="", namespaces=ns) or "").strip()
                contexto["dest.xNome"] = (dest.findtext("nfe:xNome", default="", namespaces=ns) or "").strip()
        except Exception:
            # se der erro aqui, apenas devolvemos contexto vazio
            pass

        return contexto
