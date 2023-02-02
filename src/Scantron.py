import PIL.ImageGrab
import pandas as pd
from PIL import Image
from pdf2image import convert_from_path
from openpyxl import Workbook
from os.path import exists
import glob, os, time

def getAnswer(startPoint, numberOfAnswers, pixelsApart=54):
  bestScore = 999999
  selectedAnswer = None
  for i in range(numberOfAnswers):
    counterTemp = 0
    for x in range(-5,5):
      for y in range(-5,5):
        counterTemp=counterTemp+pix[startPoint[0]+x,startPoint[1]+y][0]+pix[startPoint[0]+x,startPoint[1]+y][1]+pix[startPoint[0]+x,startPoint[1]+y][2]
    if(counterTemp<bestScore):
      bestScore = counterTemp
      selectedAnswer = i
    counterTemp = 0
    startPoint[1]=startPoint[1]+pixelsApart
  return selectedAnswer


#start = time.time()
for file in glob.glob(os.getcwd()+"\\content\\*.pdf"):
  if(not exists(file.replace(".pdf",'') +'.jpg')):
    images = convert_from_path(file)
    images[0].save(file.replace(".pdf",'') +'.jpg', 'JPEG')
    im = Image.open(file.replace(".pdf",'') +'.jpg')
    pix = im.load()
    imageSize = im.size
    x= imageSize[0]
    y = imageSize[1]
    y1 = int(419*(y/2174))
    y2 = int(1126*(y/2174)) 
    x1 = int(623*(x/1680)) 
    x2 = int(739*(x/1680))
    x3 = int(970*(x/1680))
    x4 = int(1200*(x/1680))
    x5 = int(1430*(x/1680))
    TNX3 = int(356*(x/1680))
    TNX4 = int(419*(x/1680))
    ClimbY = int(1774*(y/2174)) 

    Taxi = [int(1430*(x/1680)) ,int(203*(y/2174))]
    TN1 = [int(230*(x/1680)),y1]
    TN2 = [int(293*(x/1680)),y1]
    TN3 = [TNX3,y1]
    TN4 = [TNX4,y1]
    TaxiValue = getAnswer(Taxi, 2)
    TaxiString = ""
    if(TaxiValue == 0):
      TaxiString = "Yes"
    else:
      TaxiString = "No"
    TeamNumber = getAnswer(TN1, 10)*1000+getAnswer(TN2, 10)*100+getAnswer(TN3, 10)*10+getAnswer(TN4, 10)*1
    M1 = [x1,y1]
    M2 = [x2,y1]
    MatchNumber = getAnswer(M1, 10)*10+getAnswer(M2, 10)

    AL = [x3,y1]
    AH = [x4,y1]
    AM = [x5,y1]

    TL1 = [x1,y2]
    TL2 = [x2,y2]
    TH1 = [x3,y2]
    TH2 = [int((x4+x3)/2),y2]
    TM1 = [int((x5+x4)/2),y2]
    TM2 = [x5,y2]

    CTime = getAnswer([int((TNX3+TNX4)/2),ClimbY],5)
    CAtt = getAnswer([x1,ClimbY],5)
    CSuc = getAnswer([int((x2+x3)/2), ClimbY],5)

    CommentValue = getAnswer([x3,ClimbY], 2)

    df2 = pd.read_excel(os.getcwd()+"\\Book1.xlsx", index_col=0)
    df2.loc[len(df2.index)] = [
      MatchNumber,
      TeamNumber,
      TaxiString,
      getAnswer(AL,10),
      getAnswer(AH, 10),
      getAnswer(AM, 10),
      getAnswer(TL1, 10)*10+getAnswer(TL2, 10),
      getAnswer(TH1, 10)*10+getAnswer(TH2, 10),
      getAnswer(TM1, 10)*10+getAnswer(TM2, 10),
      getAnswer([int((TNX3+TNX4)/2),y2-54],6),
      CTime,
      CAtt,
      CSuc,
      CommentValue,
      str(os.getcwd()+"\\"+file)
      ]
    print(df2)

    with pd.ExcelWriter(os.getcwd()+"\\Book1.xlsx",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
    ) as writer:
        df2.to_excel(writer, sheet_name="Sheet1", startcol=0)
df2 = pd.read_excel(os.getcwd()+"\\Book1.xlsx", index_col=0)
print(df2)



#print ("Time elapsed:", time.time() - start)
#https://stackoverflow.com/questions/54242194/python-find-the-closest-color-to-a-color-from-giving-list-of-colors