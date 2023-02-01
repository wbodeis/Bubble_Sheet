from pdf2image import convert_from_path
import os
# https://github.com/oschwartz10612/poppler-windows

class Convert():
    def __init__(self) -> None:
        self.image_directory: str = 'images/'
        self.PDF_directory: str = 'pdf/'
        self.pdf_names: list[str]

        # Initializing functions.
        self._get_pdf_names()
        self._check_directories()

    def _get_pdf_names(self):
        try:
            self.pdf_names = (os.listdir('pdf/'))
        except:
            raise ImportError('No PDF files were found.')
    
    def _check_directories(self):
        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)
        
        if not os.path.exists(self.PDF_directory):
            os.makedirs(self.PDF_directory)

    def _convert_pdf(self):

        for pdf in self.pdf_names:
            count = 0
            image = convert_from_path('pdf/' + self.pdf_names[count],
                                    poppler_path = 'poppler/Library/bin',
                                    dpi = 700, 
                                    first_page = 1, 
                                    last_page = 1)
            # file_name = 'test.png'
            # directory = 'images//'
            location = self.image_directory + str(count + 1) + '.png'
            # image[0].save('images//test.png', 'PNG')
            image[0].save(location, 'PNG')

            # for i, image in enumerate(images):
            #     image.save('images/', format = 'PNG')
            count += 1

    

if __name__ == "__main__":
    try:
        con = Convert()
        con._convert_pdf()
    except Exception as ex:
        print(ex)
"""
x = Convert()
# x._convert_pdf()
# x._get_pdf_names()
x._convert_pdf()
# print(os.listdir('images/')[0])
"""