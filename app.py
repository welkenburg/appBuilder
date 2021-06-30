from tkBuilder import *
import tkinter as tk
import xml.dom.minidom
import cssutils

APP_PATH 	= 'avancementEnhanced.xml'
STYLE_PATH	= 'dark.css'

class Chemical():
	def __init__(self, value=0, coef=1):
		self.value = value
		self.coef	= coef

	
	def molAt(self, x, consume):
		if consume:
			return self.value - x * self.coef
		return x * self.coef

class myApp(Builder):
	def __init__(self, appPath, style=None):
		super().__init__(appPath)
		self.functions['onScale'] = self.scale
		self.build()	
		
	def setLabel(self, name, value):
		self.widgets.get(name).config(text = value)
	
	def getLabels(self, *names):
		return tuple([self.widgets.get(n).get() for n in names])

	def scale(self, n):
		# chemicals
		self.chemicals = {
			'A': Chemical(*map(int,self.getLabels('n_quantity_A','quantity_A'))),
			'B': Chemical(*map(int,self.getLabels('n_quantity_B','quantity_B'))),
			'C': Chemical(0,*map(int,self.getLabels('quantity_C'))),
			'D': Chemical(0,*map(int,self.getLabels('quantity_D')))
		}

		# reaction maths
		A_Xf 	= self.chemicals['A'].value/self.chemicals['A'].coef
		B_Xf	= self.chemicals['B'].value/self.chemicals['B'].coef
		limit 	= min(A_Xf,B_Xf)
		x 		= int(n) / 100 * limit
		maxX 	= max([limit * c.coef for c in self.chemicals.values()])

		# values
		A_Xn = self.chemicals['A'].molAt(x, consume=True)
		B_Xn = self.chemicals['B'].molAt(x, consume=True)
		C_Xn = self.chemicals['C'].molAt(x, consume=False)
		D_Xn = self.chemicals['D'].molAt(x, consume=False)

		# labels
		self.setLabel('xn_quantity_A','{:.2f}'.format(A_Xn))
		self.setLabel('xn_quantity_B','{:.2f}'.format(B_Xn))
		self.setLabel('xn_quantity_C','{:.2f}'.format(C_Xn))
		self.setLabel('xn_quantity_D','{:.2f}'.format(D_Xn))

		# graphs
		self.widgets.get('graph_A').setValue(A_Xn / maxX)
		self.widgets.get('graph_B').setValue(B_Xn / maxX)
		self.widgets.get('graph_C').setValue(C_Xn / maxX)
		self.widgets.get('graph_D').setValue(D_Xn / maxX)

appTree = xml.dom.minidom.parse(APP_PATH)
#appStyle = cssutils.parse(STYLE_PATH)

app = myApp(APP_PATH, STYLE_PATH)
app.mainloop()