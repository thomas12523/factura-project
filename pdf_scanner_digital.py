import pymupdf
import re

class Digital_Scanner:
    def __init__(self, pdf_to_scan):
        doc = pymupdf.open(f"{pdf_to_scan}")
        data = {"pages": []}
        for num, page in enumerate(doc):
            texto = page.get_text('text')
            data['pages'].append({'page': num + 1, 'content': texto})
        self.pdf = data

    def extract_info_movistar(self):
        info = {'Fecha de Vto': [None, False],
                'Monto Total a Pagar': [None, False]}

        for page in self.pdf['pages']:
            fecha_Vto_pattern = re.search(r"(?:Vto|Vencimiento)[:\s]*([\d]{2}/[\d]{2}/[\d]{4})", page['content'])
            monto_pagar_pattern = re.search(r"(?:Total a Pagar)[:\s]*\$?\s*([\d.,]+)", page['content'])

            fecha_Vto = fecha_Vto_pattern.group(1) if fecha_Vto_pattern else "No encontrado"
            monto_pagar = monto_pagar_pattern.group(1) if monto_pagar_pattern else "No encontrado"

            if fecha_Vto != "No encontrado" and not info['Fecha de Vto'][1]:
                info['Fecha de Vto'][1] = True
                info['Fecha de Vto'][0] = fecha_Vto

            if monto_pagar != "No encontrado" and not info['Monto Total a Pagar'][1]:
                info['Monto Total a Pagar'][1] = True
                info['Monto Total a Pagar'][0] = monto_pagar

        return info
