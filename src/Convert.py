
import os, glob
from pdf2image import convert_from_path

# https://github.com/oschwartz10612/poppler-windows

class Convert():
    def __init__(self) -> None:
        self.image_directory: str = 'images/'
        self.PDF_directory: str = 'input/'
        self.results_directory: str = 'results/'
        self.pdf_names: list[str]

        # Initializing functions.
        self._get_pdf_names()
        
#-----------------------------------------------------------------------------------------------------------------------
    def _get_pdf_names(self):
        try:
            self.pdf_names = [f for f in os.listdir(self.PDF_directory) if f.endswith('.pdf')]
        except:
            raise ImportError('No PDF files were found.')
    
#-----------------------------------------------------------------------------------------------------------------------
    def _convert_pdf(self):
        for i in range(len(self.pdf_names)):
            image = convert_from_path(self.PDF_directory + self.pdf_names[i],
                                      poppler_path = 'poppler/Library/bin',
                                      dpi = 700,  
                                      last_page = 1,
                                      thread_count = 10)
            location = self.image_directory + str(i + 1) + '.png'
            image[0].save(location, 'PNG')

#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        con = Convert()
        con._convert_pdf()
    except Exception as ex:
        print(ex)