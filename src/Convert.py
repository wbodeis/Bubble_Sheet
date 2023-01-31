from pdf2image import convert_from_path
import os
# https://github.com/oschwartz10612/poppler-windows

class Convert():
    def __init__(self) -> None:
        self.image_directory: str = 'images/'
        self.PDF_directory: str = 'PDFs/'
        self.pdf_names: list[str]

        # Initializing functions.
        self._get_pdf_names()

    def _get_pdf_names(self):
        try:
            self.pdf_names = (os.listdir('PDFs/'))
        except Exception as ex:
            print(ex)

    def _convert_pdf(self):

        image = convert_from_path('PDFs/' + self.pdf_names[0],
                                   poppler_path = 'poppler-23.01.0//Library//bin',
                                   dpi = 700, 
                                   first_page = 1, 
                                   last_page = 1)
        # file_name = 'test.png'
        # directory = 'images//'
        # location = directory + file_name
        # images[0].save('images//test.png', 'PNG')
        image[0].save(self.image_directory, 'PNG')

        # for i, image in enumerate(images):
        #     image.save('images/', format = 'PNG')

    
"""
if __name__ == "__main__":
    Convert
"""
x = Convert()
# x._convert_pdf()
# x._get_pdf_names()
x._convert_pdf()
# print(os.listdir('images/')[0])