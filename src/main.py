import os


        
#-----------------------------------------------------------------------------------------------------------------------
def _check_directories(self):
    if not os.path.exists(self.image_directory):
        os.makedirs(self.image_directory)
    
    if not os.path.exists(self.PDF_directory):
        os.makedirs(self.PDF_directory)

_check_directories()