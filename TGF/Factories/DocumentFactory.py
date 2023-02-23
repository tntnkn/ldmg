from aiogram.types import InputFile


class DocumentFactory():
    docgen = None

    @staticmethod
    def INIT(docgen):
        DocumentFactory.docgen = docgen

    @staticmethod
    def Make(tags):
        f_name = DocumentFactory.docgen.MakeDocument(tags).f_name
        return InputFile(f_name, filename="Иск.docx")        

