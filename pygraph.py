# -*- coding: utf-8 -*-
#
# This is really really Simple Python Graphing Program
# It is arranged 3 tabs
#
# first tab can draw 2d graphing such as y = x^2 and x = cos(t), y = sin(t)
# second tab can draw 3d graphing such as z = sin(sqrt(x^2 + y^2)) and x = cos(u), y = cos(v), z = sin(u + v)
# third tab can crawl rss feed datas and make word cloud map. it is so beautiful
#
# https://github.com/soorichu
# This is follwed MIT License.
# If you contact me, please send email : soorichu@gmail.com or Homepage : http://soori.co
# Thanks!
#

#for system
import sys
from os import path, walk
import re
import time
#for math
from numpy import *
#for graph
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
#UI : pyqt5
from PyQt5 import QtCore, QtGui, QtWidgets, sip
#for wordcloud
import feedparser
from wordcloud import WordCloud, STOPWORDS

from polytofunction import polytofunction


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        #define mesh ranges for 3d graph
        mesh_ranges = ["사각형 메쉬", "와이어 프레임", "칸토어", "산포도", "곡선"]

        #define color maps for 3d graph
        color_maps = ["Spectral", "CMRmap", "Blues", "Greens", "Reds", "Oranges", "Purples", "Grays", 
                    "Accent", "BrBG", "BuGn", "BuPu", "Dark2", "GnBu", "OrRd", 
                     "PRGn", "Paired", "Pastel1", "Pastel2", "PiYG", "PuBu", "PuBuGn", "PuOr", "PuRd", 
                    "RdBu", "RdGy", "RdPu", "RdYlBu", "RdYlGn",  "Set1", "Set2", "Set3", 
                    "Wistia", "YlGn", "YlGnBu", "YlOrBr", "YlOrRd"]

        self.graph2d = 0

        Dialog.setObjectName("PyGraph")
        Dialog.setWindowTitle("PyGraph")
        Dialog.resize(571, 550)

        #define fontfamily for beautiful font
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)

        #define tabwidget
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 551, 521))
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")

        #define tab
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "2차원")

        #define 2d graph tab 
#        self.label_3 = QtWidgets.QLabel(self.tab)
#        self.label_3.setGeometry(QtCore.QRect(20, 20, 500, 21))
#        self.label_3.setFont(font)
#        self.label_3.setObjectName("label_3")
#        self.label_3.setText("미지수가 x인 식 입력")

        #RadioButton for 2D Graph
        self.radioButton_1 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_1.setGeometry(QtCore.QRect(20, 20, 80, 31))
        self.radioButton_1.setText("y=f(x)")
        self.radioButton_1.setChecked(True)

        self.radioButton_2 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_2.setGeometry(QtCore.QRect(160, 20, 200, 31))
        self.radioButton_2.setText("매개변수 t 방정식")
        self.radioButton_2.setChecked(False)

        self.radioButton_3 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_3.setGeometry(QtCore.QRect(350, 20, 150, 31))
        self.radioButton_3.setText("도형의 방정식")
        self.radioButton_3.setChecked(False)


#        self.checkBox_1 = QtWidgets.QCheckBox(self.tab)
#        self.checkBox_1.setGeometry(QtCore.QRect(300, 64, 96, 31))
#        self.checkBox_1.setObjectName("checkBox_1")
#        self.checkBox_1.setText("x 생략")
#        self.checkBox_1.setChecked(True)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 60, 361, 41))
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.hide()

        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 60, 31, 31))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("x = ")
        self.label_4.hide()

        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(50, 95, 361, 41))
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(20, 95, 31, 31))
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("y = ")

        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 60, 91, 111))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Graph")

        self.checkBox_2 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_2.setGeometry(QtCore.QRect(30, 200, 150, 40))
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setText("x축 단위 π")

#        self.checkBox_3 = QtWidgets.QCheckBox(self.tab)
#        self.checkBox_3.setGeometry(QtCore.QRect(250, 200, 150, 40))
#        self.checkBox_3.setFont(font)
#        self.checkBox_3.setObjectName("checkBox_3")
#        self.checkBox_3.setText("격자 보이기")
#        self.checkBox_3.setChecked(True)


        self.label_1 = QtWidgets.QLabel(self.tab)
        self.label_1.setGeometry(QtCore.QRect(20, 270, 500, 150))
        self.label_1.setText("#팁\n1. 한 좌표평면에 여러 개의 그래프를 그릴 수 있음.\n2. 숫자와 문자의 곱은 반드시 * 표시해야 함.\n3. 매개변수 방정식을 이용할 경우 'x 생략' 체크를 해제하고 \n   매개변수는 t로 이용.\n4. 기호사용 예 : x^2-2*x+1, sqrt(x), abs(x), sin(x), cos(x), log(x)")
        

        #define 3d graph tab_2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "3차원")

        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(440, 70, 91, 181))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText( "Graph")

        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 500, 21))
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("미지수가 x, y인 함수식")

        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(20, 140, 31, 31))
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("y = ")

        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(60, 70, 191, 41))
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setEnabled(False)

        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(60, 140, 191, 41))
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setEnabled(False)

        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(20, 70, 31, 31))
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_8.setText("x = ")

        self.lineEdit_11 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_11.setGeometry(QtCore.QRect(60, 210, 361, 41))
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")

        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(20, 210, 31, 31))
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_17.setText("z = ")

        self.comboBox = QtWidgets.QComboBox(self.tab_2)
        self.comboBox.setGeometry(QtCore.QRect(230, 280, 181, 31))
        self.comboBox.setObjectName("comboBox")

        self.comboBox_2 = QtWidgets.QComboBox(self.tab_2)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 330, 181, 31))
        self.comboBox_2.setObjectName("comboBox_2")

        #input combobox items
        for item in mesh_ranges:
            self.comboBox.addItem(item)    

        for item in color_maps:
            self.comboBox_2.addItem(item)

        self.label_18 = QtWidgets.QLabel(self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(60, 270, 141, 41))
        self.label_18.setObjectName("label_18")
        self.label_18.setText("그래프 종류")

        self.label_19 = QtWidgets.QLabel(self.tab_2)
        self.label_19.setGeometry(QtCore.QRect(60, 330, 131, 21))
        self.label_19.setObjectName("label_19")
        self.label_19.setText("그래프 칼라맵")

        self.checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox.setGeometry(QtCore.QRect(230, 400, 181, 19))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText("칼라맵 보기")

        self.checkBox_5 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_5.setGeometry(QtCore.QRect(300, 110, 96, 31))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.setText("x, y 생략")
        self.checkBox_5.setChecked(True)

        #define tab_3
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "Word Cloud")

        self.label_20 = QtWidgets.QLabel(self.tab_3)
        self.label_20.setGeometry(QtCore.QRect(20, 20, 470, 41))
        self.label_20.setText("크롤링할 RSS 주소(http://)")

        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(30, 80, 470, 35))
        self.lineEdit_6.setText("http://www.ktimes.com/www/rss/rss.xml")

        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_7.setGeometry(QtCore.QRect(30, 130, 470, 35))
        self.lineEdit_7.setText("https://news.google.com/?output=rss")

        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_8.setGeometry(QtCore.QRect(30, 180, 470, 35))
        self.lineEdit_8.setText("http://rss.cnn.com/rss/cnn_tech.rss")

        #cloud font
        self.label_22 = QtWidgets.QLabel(self.tab_3)
        self.label_22.setGeometry(QtCore.QRect(20, 240, 150, 41))
        self.label_22.setText("워드 클라우드 글꼴")

        self.comboBox_3 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_3.setGeometry(QtCore.QRect(200, 240, 300, 35))
        self.comboBox_3.setObjectName("comboBox_3")
        self.font_path = 'font\\'
        for root, dirs, files in walk(self.font_path):
        #    print(root, dirs, files)
            for fname in files:
                self.comboBox_3.addItem(fname)

        self.label_21 = QtWidgets.QLabel(self.tab_3)
        self.label_21.setGeometry(QtCore.QRect(20, 290, 470, 41))
        self.label_21.setText("데이터를 저장할 파일명(.txt/.csv)")

        self.lineEdit_10 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_10.setGeometry(QtCore.QRect(30, 330, 470, 35))

        #now localtime for saving name
        now = time.localtime()
        s = "%04d%02d%02d_%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        self.lineEdit_10.setText("clouddata"+s+".txt")

        #define buttonbox
        self.buttonBox = QtWidgets.QDialogButtonBox(self.tab_3)
        self.buttonBox.setGeometry(QtCore.QRect(20, 400, 480, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        #tab3 buttonbox function
        self.buttonBox.accepted.connect(self.crawling)
        self.buttonBox.rejected.connect(Dialog.reject)

        #Function 2dim
        self.pushButton_2.clicked.connect(self.graphing2d)
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

        #Function 3dim
        self.pushButton_3.clicked.connect(self.graphing3d)

        #radioButton clicked
        self.radioButton_1.clicked.connect(self.radioButtonChanged)
        self.radioButton_2.clicked.connect(self.radioButtonChanged)
        self.radioButton_3.clicked.connect(self.radioButtonChanged)

        #tab2 x, y check
        self.checkBox_5.stateChanged.connect(self.checkBox_5Changed)

        self.checkBox_2.stateChanged.connect(self.checkBox_2Changed)
#        self.checkBox_3.stateChanged.connect(self.checkBox_3Changed)
     

    def checkBox_3Changed(self):
        if self.checkBox_3.isChecked:
            plt.grid(True)
        else:
            plt.grid(False)


    def checkBox_2Changed(self):
        if self.checkBox_2.isChecked:
            xtics = arange(-30*pi, 30*pi, pi)
            xticlabel = []
            for xt in arange(-30, 30, 1):
                if xt == -1: xticlabel.append(r'$-\pi$')
                elif xt == 1: xticlabel.append(r'$\pi$')
                else: xticlabel.append('$'+str(xt)+r'\pi$')
            plt.xticks(xtics, xticlabel)
        else:
            xtics = arange(-100, 100, 1)
            xticlabel = []
            for xt in range(-100, 100, 1):
                xticlabel.append(xt)
            plt.xtics(xtics, xticlabel) 


    def radioButtonChanged(self):
        if self.radioButton_1.isChecked() == True:
            self.lineEdit_2.hide()
            self.label_4.hide()
            self.label_5.show()
            self.label_5.setGeometry(QtCore.QRect(20, 95, 31, 31))
            self.lineEdit_3.setGeometry(QtCore.QRect(50, 95, 361, 41))
            self.graph2d = 0

        elif self.radioButton_2.isChecked() == True:
            self.lineEdit_2.show()
            self.label_4.show()
            self.label_5.show()
            self.label_5.setGeometry(QtCore.QRect(20, 130, 31, 31))
            self.lineEdit_3.setGeometry(QtCore.QRect(50, 130, 361, 41))
            self.graph2d = 1
#            self.label_3.setText("미지수가 x인 함수식")
        elif self.radioButton_3.isChecked() == True:
            self.lineEdit_2.hide()
            self.label_4.hide()
            self.label_5.hide()
#            self.label_5.setGeometry(QtCore.QRect(20, 95, 31, 31))
            self.lineEdit_3.setGeometry(QtCore.QRect(20, 95, 400, 41))
            self.graph2d = 2
#            self.label_3.setText("미지수가 t인 매개변수 방정식")


    def checkBox_5Changed(self):
        if self.checkBox_5.isChecked() == True:
            self.lineEdit_5.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.label_6.setText("미지수가 x, y인 함수식")
        #    print(True)
        else:
            self.lineEdit_5.setEnabled(True)
            self.lineEdit_4.setEnabled(True)
            self.label_6.setText("미지수가 u, v인 매개변수 방정식")


    # Graph 2D
    def graphing2d(self):
        t = arange(-100, 100, 0.01)
        x = arange(-100, 100, 0.01)
        graph_text_x = ""
        if self.graph2d == 1:
            graph_text_x = self.lineEdit_2.text()

            try:
                x = eval(graph_text_x.replace("^", "**"))
            except:
                print("error")

            graph_text_x = "$x = "+graph_text_x.replace("*", "")+"$, "

        graph_text = self.lineEdit_3.text()
        temgraph = ""

        if self.graph2d == 2:
            try: temgraph = polytofunction(graph_text)
            except: print('error')
            if temgraph[-1]=='m':
                try:            
                    y = eval(temgraph[:-1].replace("^", "**"))
                except:
                    print('error')
        else:
            try:
                y = eval(graph_text.replace("^", "**"))
            except:
                print("error")

        if self.graph2d != 2:
            graph_text = graph_text_x + "$y = "+graph_text.replace("*", "")+"$"
        else: 
            graph_text = "$"+graph_text+"$"

        try:
            self.ax.plot(x, y)
        except:
            print("error")

        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')

        plt.xlim(-10, 10)
        plt.ylim(-10, 10)

        #axis pretty
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position(('data',0))
        ax.spines['left'].set_position(('data',0))
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        try:
            plt.plot(x, y, linewidth="3", linestyle="-", label=graph_text)
            plt.plot()
        except:
            print("error")

        if self.graph2d == 2:
            try:            
                y = eval(('-('+temgraph[:-1]+')').replace("^", "**"))
                plt.plot(x, y, linewidth="3", linestyle="-")
                plt.plot()
            except:
                print('error')
                
        plt.legend(loc='upper left', frameon=False)
        plt.grid(True)
        plt.show()


    # Graph 3D
    def graphing3d(self):
        plt.close(self.fig)

        self.fig3 = plt.figure(figsize=(8, 8))
        self.ax3 = self.fig3.add_subplot(111, projection='3d') 

        u = arange(-10, 10, 0.25)
        v = arange(-10, 10, 0.25)
        u, v = meshgrid(u, v)

        if self.checkBox_5.isChecked() == False:
            x = eval(self.lineEdit_4.text().replace("^", "**"))
            y = eval(self.lineEdit_5.text().replace("^", "**"))
        else:
            x = arange(-10, 10, 0.25)
            y = arange(-10, 10, 0.25)
            x, y = meshgrid(x, y)

        graph_text = self.lineEdit_11.text()

        try:
            z = eval(graph_text.replace("^", "**"))
        except:
            print('error')

        graph_text = graph_text.replace("*", "")
        Mesh = self.comboBox.currentText() 

        try:
            surf = self.ax3.plot_surface(x, y, z, cmap=self.comboBox_2.currentText())
        except:
            print('error')

        try:
            if Mesh == "사각형 메쉬":
                surf = self.ax3.plot_surface(x, y, z, cmap=self.comboBox_2.currentText(), antialiased=True)
            elif Mesh == "와이어 프레임":
                surf == self.ax3.plot_wireframe(x, y, z, cmap=self.comboBox_2.currentText(), antialiased=True)
            elif Mesh == "칸토어":
                surf = self.ax3.contour(x, y, z, cmap=self.comboBox_2.currentText(), antialiased=True)
            elif Mesh == "산포도":
                surf = self.ax3.scatter(x, y, z, cmap=self.comboBox_2.currentText())
            elif Mesh == "곡선":
                surf = self.ax3.plot(x, y, z, cmap=self.comboBox_2.currentText())
        except:
            print('error')

        if self.checkBox.isChecked() == True:
            self.fig3.colorbar(surf, shrink=0.5, aspect=10)

        plt.show()


    # Crawling for Word Cloud
    def crawling(self):
        plt.close(self.fig)
        self.feedlist = [self.lineEdit_6.text(), self.lineEdit_7.text(), self.lineEdit_8.text()]
        self.cloud_folder = "cloud_data\\"
        self.savedata = self.cloud_folder + self.lineEdit_10.text()
        self.d = path.dirname(__file__)
        self.mystopwords = ['test', 'quot', 'nbsp']
   #     print(self.savedata)
    #    print(self.feedlist)
        self.combineWordsFromFeed(self.savedata)


    def extractPlainText(self, ht):
        plaintxt = ''
        s = 0
        for char in ht:
            if char == '<': s=1
            elif char == '>':
                s = 0
                plaintxt += ' '
            elif s == 0:
                plaintxt += str(char)
        return plaintxt


    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if len(s)>3]


    def combineWordsFromFeed(self, filename):
        with open(filename, 'w') as wfile:
            for feed in self.feedlist:
        #        print("Parsing : "+ feed)
                fp = feedparser.parse(feed)
                for e in fp.entries:
                    txt = str(str(e.title).encode('utf8')) + self.extractPlainText(str(e.description).encode('utf8'))

                    words = self.separatewords(txt)

                    for word in words:
                        if word.isdigit() == False and word not in self.mystopwords:
                            wfile.write(word)
                            wfile.write(" ")
                    wfile.write('\n')
        wfile.close()
        self.show_wordcloud()
#        sys.exit(app.exec_())


    def show_wordcloud(self):
        text = open(path.join(self.d, self.savedata)).read()
        wordcloud = WordCloud(font_path = self.font_path + self.comboBox_3.currentText(),
            stopwords =  STOPWORDS,#set(map(str.strip, open('stopwords').readlines())),
            background_color = "#222222",
            width=1000,
            height=800).generate(text)
        plt.figure(figsize=(13, 13))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

