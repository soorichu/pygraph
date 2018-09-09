#!-- coding: utf-8 --
import sys
import re
from PyQt5 import QtWidgets, QtCore
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.style as stl
import matplotlib.ticker as tck

from polytofunction import polytofunction

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setupUI()
		self.count = 0
		

	def setupUI(self):
		self.setGeometry(200, 300, 410, 500)
		self.inputText = QtWidgets.QLineEdit("", self)
		self.inputText.setGeometry(QtCore.QRect(30, 30, 300, 30))

		self.statusBar = QtWidgets.QStatusBar(self)
		self.setStatusBar(self.statusBar)
#		self.inputText.textChanged.connect(self.inputTextChanged)		
		
#		self.showAxisCheckBox = QtWidgets.QCheckBox("축 보이기", self)
#		self.showAxisCheckBox.setGeometry(QtCore.QRect(40, 70, 150, 30))
#		self.showAxisCheckBox.stateChanged.connect(self.showAxisCheckBoxChanged)

		self.showGridCheckBox = QtWidgets.QCheckBox("격자 보이기", self)
		self.showGridCheckBox.setGeometry(QtCore.QRect(40, 70, 150, 30))
		self.showGridCheckBox.stateChanged.connect(self.showGridCheckBoxChanged)

		self.piAxisCheckBox = QtWidgets.QCheckBox("x축 단위 π", self)
		self.piAxisCheckBox.setGeometry(QtCore.QRect(200, 70, 150, 30))


		self.graphLabel = QtWidgets.QLabel("", self)
		self.graphLabel.setGeometry(QtCore.QRect(30, 120, 390, 400))
		self.graphLabel.setAlignment(QtCore.Qt.AlignTop)

		self.okButton = QtWidgets.QPushButton("OK", self)
		self.okButton.setGeometry(QtCore.QRect(340, 30, 40, 30))		
		self.okButton.clicked.connect(self.okButtonClicked)

		self.object_labels = []
		self.function_samples = ['f', 'g', 'h']
		self.valuable_samples = ['a', 'b', 'c', 'd', 'e']
		self.function_count = 0
		self.valuable_count = 0
		self.label_text = ""

		self.fig = plt.figure(figsize=(9, 9))
		self.ax = self.fig.add_subplot(1,1,1)
		self.piAxisCheckBox.stateChanged.connect(self.piXAxis)

	def functionLabelArray(self, text):
		pass
		
	def graph2dInit(self):
		plt.xlim(-5, 5)
		plt.ylim(-5, 5)
		axisShow(self.ax)
		self.count += 1


	def showGridCheckBoxChanged(self):
		if self.count > 0:
			if self.showGridCheckBox.isChecked()==True:
				gridShow(self.ax)
			else: gridHide(self.ax)

	def showAxisCheckBoxChanged(self):
		if self.count > 0:
			if self.showAxisCheckBox.isChecked()==True:
				axisShow(self.ax)
				plt.show()
			else: 
				axisHide(self.ax)
				plt.show()

	def okButtonClicked(self):
		if self.count == 0:
			self.graph2dInit()
		graph_text = self.inputText.text()
		graph = graphJudge(graph_text)
		if graph == 'x':
			self.label_text += makeLabelText(self.function_count, 
				self.function_samples, len(self.function_samples)) 
			self.label_text += ("(x) = "+ graph_text + "\n")
			self.graphLabel.setText(self.label_text)
			self.function_count += 1
			drawGraphX(graph_text, self.ax)
		elif graph == 'xy':
			self.label_text += graph_text+"\n"
			self.graphLabel.setText(self.label_text)
			graph_text = polytofunction(graph_text)[:-1]
			drawGraphXY(graph_text, self.ax)

	def piXAxis(self):
		if self.piAxisCheckBox.isChecked:
#			self.ax.xaxis.set_major_formatter(tck.FormatStrFormatter(r'%g$\pi$'))
#			self.ax.xaxis.set_major_locator(tck.MultipleLocator(base=1.0))
#			plt.style.use("ggplot")
			xtics = arange(-30*pi, 30*pi, pi)
			xticlabel = []
			for xt in arange(-30, 30, 1):
				xticlabel.append('$'+str(xt)+r'\pi$')

			plt.xticks(xtics, xticlabel)

		else:
			self.ax.xaxis.set_major_formatter(tck.FormatStrFormatter(r'%g'))
			self.ax.xaxis.set_major_locator(tck.MultipleLocator(base=pi))
			plt.style.use("ggplot")			
				
def makeLabelText(count, samples, lens):
	if count < lens:
		return samples[count]
	else:
		return samples[count%lens] + str(int(count/lens))

#	def inputTextChanged(self):
#		if self.count > 0:
#			graph_text = self.inputText.text()
#			drawGraph(graph_text, self.ax)

def axisShow(ax):
	ax.spines['left'].set_position(('data', 0))
	ax.spines['right'].set_color('none')
	ax.spines['bottom'].set_position(('data', 0))
	ax.spines['top'].set_color('none')
	ax.spines['left'].set_smart_bounds(True)
	ax.spines['bottom'].set_smart_bounds(True)
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')

def axisHide(ax):
	pass


def gridShow(ax):
	ax.grid()

def gridHide(ax):
	ax.grid(False)


def drawGraphX(graph_text, ax):
	x = arange(-100, 100, 0.01)
#	if graphPiJudge: x = arange(-pi*100, pi*100, 0.01*pi)
#	else: x = arange(-100, 100, 0.01)
#	if len(self.ax.lines) > 0:
#		self.ax.lines.pop(0)
	try: y = eval(graph_text.replace("^", "**"))
	except: print('error')

#	if graphPiJudge:
#		plt.plot(x/pi, y)
#		plt.ylim(-5*pi, 5*pi)
#		piXAxis(plt, ax)
#	else:
#		plt.plot(x, y)
	plt.plot(x, y)

	plt.show()


def drawGraphXY(graph_text, ax):
	x = arange(-100, 100, 0.01)
#	if graphPiJudge: x = arange(-pi*100, pi*100, 0.01*pi)
#	else: x = arange(-100, 100, 0.01)
	try:
		y = eval(graph_text.replace("^", "**"))
		ym = eval("(-1)*("+(graph_text.replace("^", "**"))+")")
	except: print('error')

#	if graphPiJudge:
#		plt.plot(x/pi, y)
#		plt.plot(x/pi, ym)
#		plt.ylim(-5*pi, 5*pi)
#		piXAxis(plt, ax)
#	else:
#		plt.plot(x, y)
#		plt.plot(x, ym)
	plt.plot(x, y)
	plt.plot(x, ym)

	plt.show()


def graphPiJudge(graph_text):
	repi = re.compile('.*[pi]+.*')
	resin = re.compile('.*[sin]+.*')
	recos = re.compile('.*[cos]+.*')
	retan = re.compile('.*[tan]+.*')

	if repi.match(graph_text) or resin.match(graph_text) or recos.match(graph_text) or retan.match(graph_text):
		return True
	else:
		return False

def graphJudge(graph_text):
	#define graphing regural extension 
	rex = re.compile('.*[x]+.*')
	rey = re.compile('.*[y]+.*')
	rez = re.compile('.*[z]+.*')
	ren = re.compile('.*[0-9]+.*')
	reu = re.compile('^[a-zA-Z]+[0-9]*.*')

	if graph_text == "":
		return ""
	
	elif rez.match(graph_text): #valuable xyz
		return "xyz"

	elif rey.match(graph_text): #valuable xy
		return "xy"

	elif rex.match(graph_text): #valuable x
		return "x"

	elif ren.match(graph_text): #number
		return "n"

	elif reu.match(graph_text): #user valuable
		return "u"

	else: return ""


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	mainwindow = MainWindow()
	mainwindow.show()
	app.exec_()