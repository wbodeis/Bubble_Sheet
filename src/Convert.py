
import os, glob
from pdf2image import convert_from_path

# https://github.com/oschwartz10612/poppler-windows

class Convert():
    def __init__(self) -> None:
        self.image_directory: str = 'results/'
        self.input_directory: str = 'input/'
        self.pdf_names: list[str]

        # Initializing functions.
        self._check_for_directory()
        self._get_pdf_names()
        self._check_directories()

#-----------------------------------------------------------------------------------------------------------------------
    def _get_pdf_names(self):
        try:
            self.pdf_names = [f for f in os.listdir(self.input_directory) if f.endswith('.pdf')]
        except:
            raise ImportError('No PDF files were found.')
    
    def _check_directories(self):
        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)
        
        if not os.path.exists(self.PDF_directory):
            os.makedirs(self.PDF_directory)

    def _convert_pdf(self):
        for i in range(len(self.pdf_names)):
            image = convert_from_path(self.input_directory + self.pdf_names[i],
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