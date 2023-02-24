import os
import time
from dataclasses    import dataclass
from docxtpl        import DocxTemplate

from typing         import Dict


@dataclass
class DocHandle():
    f_name : str


class Docgen():
    def __init__(self, docs : Dict):
        self.docs_info = [
            { 'tag' : doc['tag'], 'name' : doc['doc_name'] } for
                doc in docs.values()
        ]

    def MakeDocument(self, tags):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        tmp_dir  = os.path.join(file_dir, 'tmp')
        f_name   = os.path.join(tmp_dir, 
                                time.strftime("%Y%m%d%H%M%S")) + ".docx"
        self.__MakeDocumentJinja(f_name, tags)
        return DocHandle(f_name=f_name)

    def __MakeDocumentJinja(self, f_name, tags):
        try:
            doc = self.__GetDoc(tags)
            doc.render(tags)
        except Exception as e:
            print(e)
        doc.save(f_name)

    def __GetDoc(self, tags):
        file_dir        = os.path.dirname(os.path.realpath(__file__))
        templates_dir   = os.path.join(file_dir, 'templates')

        for doc in self.docs_info:
            if doc['tag'] in tags: 
                return DocxTemplate(
                    os.path.join(templates_dir, doc['name']))
        return None

