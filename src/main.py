import os


class OMR_Scantron():
    def __init__(self) -> None:
        self.image_directory: str = 'images/'
        self.PDF_directory: str = 'input/'
        self.results_directory: str = 'results/'
        self.pdf_names: list[str]

        # Initializing functions.
        self._check_directories()
        self._get_pdf_names()
        
#-----------------------------------------------------------------------------------------------------------------------
    def _get_pdf_names(self):
        try:
            self.pdf_names = [f for f in os.listdir(self.PDF_directory) if f.endswith('.pdf')]
        except:
            raise ImportError('No PDF files were found.')

        
#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self):
        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)
        
        if not os.path.exists(self.PDF_directory):
            os.makedirs(self.PDF_directory)

_check_directories()