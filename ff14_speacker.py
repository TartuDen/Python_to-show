import pyautogui as pg 
import time
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import pyttsx3





pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

check1=set()

for k in range(10000):
	x_s_p=False
	y_s_p=False
	
	def conf(pth):
		for i in range(10,7,-1):
			i=i/10
			x=pg.locateCenterOnScreen(pth, confidence=i)
			if x:
				print("conf. = ",i)
				return(x)


	start_point=conf("G:/PROJECTS/FF14/img/start1.png")
	if start_point:
		# pg.moveTo(start_point)
		# pg.moveTo(start)
		x_s_p=start_point[0]
		y_s_p=start_point[1]
	else:
		time.sleep(1)
		start_point=conf("G:/PROJECTS/FF14/img/start1.png")


	#time.sleep(2)

	#Point(x=1301, y=885)
	#Point(x=721, y=808)

	im=pg.screenshot('new_test1.png',region=(x_s_p-580,y_s_p-77, 580, 85))

	txt1=(pytesseract.image_to_string(Image.open("G:/PROJECTS/For Dani/new_test1.png")))
	if txt1 not in check1:
		check1.add(txt1)

		temp1=str()
		for i in txt1:
			if i=="|":
				temp1=temp1 +'I'
			elif i=="—":
				temp1=temp1+' . '
			elif i=='\n':
				temp1=temp1+' '
			else:
				temp1=temp1 + i

		print(temp1)



		engine = pyttsx3.init()
		# for voice in engine.getProperty('voices'):
		#     print(voice)

		engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
		engine.setProperty('rate', 190)
		engine.say(temp1)
		engine.runAndWait()

		pg.click()
