import pymupdf

class Digital_Scannar:
    def __init__(self,pdf_to_scan):
        self.pdf = pdf_to_scan

    def extract_text(self):
        doc = pymupdf.open(f"{self.pdf}")
        data = {"pages":[]}
        for num,page in enumerate(doc):
            texto = page.get_text('text')
            data['pages'].append({'page':num+1,'content': texto})
            
        return data