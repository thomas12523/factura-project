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
    
    def extract_info_metrogas(self):
        info = {'Fecha de Vto': [None, False],
                'Monto Total a Pagar': [None, False]}
        
        for page in self.pdf['pages']:
            monto_pagar_pattern = re.search(r'TOTAL A PAGAR\s*\$ ([\d,.]+)', page['content'])
            monto_pagar = monto_pagar_pattern.group(1) if monto_pagar_pattern else "No encontrado"

            fecha_Vto_pattern = re.search(r'FECHA DE VENCIMIENTO:\s*([\d/]+)', page['content'])
            fecha_Vto = fecha_Vto_pattern.group(1) if fecha_Vto_pattern else "No encontrada"
            
            if fecha_Vto != "No encontrado" and not info['Fecha de Vto'][1]:
                info['Fecha de Vto'][1] = True
                info['Fecha de Vto'][0] = fecha_Vto

            if monto_pagar != "No encontrado" and not info['Monto Total a Pagar'][1]:
                info['Monto Total a Pagar'][1] = True
                info['Monto Total a Pagar'][0] = monto_pagar
        
        return info

    def extract_info_edenor(self):
        info = {'Fecha de Vto': [None, False],
                'Monto Total a Pagar': [None, False]}

        for page in self.pdf['pages']:
            text = page['content']

            monto_pagar_pattern = re.search(r"[-+]?\$?\s?(-?\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d+))",text, re.IGNORECASE)
            monto_pagar = monto_pagar_pattern.group(1) if monto_pagar_pattern else "No encontrado"

            fecha_Vto_pattern = re.search(r'(FECHA DE VENCIMIENTO|VENCIMIENTO).*?(\d{1,2}/\d{1,2}/\d{2,4})', text, re.IGNORECASE)
            fecha_Vto = fecha_Vto_pattern.group(1) if fecha_Vto_pattern else "No encontrada"

            if fecha_Vto != "No encontrada" and not info['Fecha de Vto'][1]:
                info['Fecha de Vto'][1] = True
                info['Fecha de Vto'][0] = fecha_Vto

            if monto_pagar != "No encontrado" and not info['Monto Total a Pagar'][1]:
                info['Monto Total a Pagar'][1] = True
                info['Monto Total a Pagar'][0] = monto_pagar

        return info

    def extract_info_edesur(self):
        info = {'Fecha de Vto': [None, False],
                'Monto Total a Pagar': [None, False]}
        
        for page in self.pdf['pages']:
            
            fecha_Vto_pattern = re.search(r'Vencimiento:\s*(\d{2}/\d{2}/\d{4})', page['content'])
            if fecha_Vto_pattern:
                fecha_Vto = fecha_Vto_pattern.group(1)
            else:
                fecha_Vto = "No encontrada"
                
            monto_pagar_pattern = re.search(r'TOTAL:\s*\$\s*([\d,.]+)', page['content'])
            monto_pagar = monto_pagar_pattern.group(1) if monto_pagar_pattern else "No encontrado"
            
            if fecha_Vto != "No encontrado" and not info['Fecha de Vto'][1]:
                info['Fecha de Vto'][1] = True
                info['Fecha de Vto'][0] = fecha_Vto

            if monto_pagar != "No encontrado" and not info['Monto Total a Pagar'][1]:
                info['Monto Total a Pagar'][1] = True
                info['Monto Total a Pagar'][0] = monto_pagar
        
        return info    
