import os


class OMR_Scantron():
    def __init__(self) -> None:
        self.directories: list[str] = ['input/', 'images/', 'results/']
        self.pdf_names: list[str]

        # Initializing functions.
        self._check_directories()
        self._get_pdf_names()
        
#-----------------------------------------------------------------------------------------------------------------------
    def _get_pdf_names(self):
        try:
            self.pdf_names = [f for f in os.listdir(self.directories[0]) if f.endswith('.pdf')]
        except:
            raise ImportError('No PDF files were found.')

        
#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self):
        for direct in self.directories:
            if not os.path.exists(direct):
                os.makedirs(direct)


if __name__ == "__main__":
    try:
        con = OMR_Scantron()
    except Exception as ex:
        print(ex)