# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 18:23:26 2014
@author: Manuel
"""

# modules which need to be installed
#pygs

#from myForceFocus import *



from myKeyboardSim import *
#import win32clipboard
from gotransscrapper import getGoogleTranslationFromText, initSelenium
import pyperclip
from globalHotkeys import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os


__file__ = os.path.basename(sys.argv[0])

class AppForm(QMainWindow):
     
    def __init__(self, parent=None):

        # target language handler and dict for translate   
        self.tlang = None   
        self.langDict = {u'Deutsch': 'de',
                u'Englisch': 'en',
                u'Spanisch': 'es',
                u'Franzoesisch': 'fr',
                u'Thailaendisch': 'th'
                }
        
        # set global hotkey handler
        self.shortcut_show = QxtGlobalShortcut()
        self.shortcut_close = QxtGlobalShortcut()
        
        # gui logic
        QMainWindow.__init__(self, parent, Qt.WindowStaysOnTopHint)  
        self.create_main_frame()
        # position window (x,y) and extent (w,h)       
        self.setGeometry(1070, 600, 200, 150)

        
    def create_main_frame(self):
        
        page = QWidget()  

        #define elements
        self.edit1 = QLineEdit()
        self.selectLab = QLabel('select target language',page)
        tList = ['Spanisch','Englisch', 'Deutsch', 'Franzoesisch', 'Thailaendisch']
        self.tselect = QComboBox(page)
        self.tselect.addItems(tList)       
        self.buttonGo = QPushButton('GO', page)
        self.buttonEx = QPushButton('Exit', page)
        self.msgBoxCloseButton = QPushButton('OK')
        
        # combobox logic for triggering state
        self.changeIndex()
        self.tselect.activated['QString'].connect(self.setHandle)
        self.tselect.currentIndexChanged['QString'].connect(self.setHandle)
        self.changeIndex()       
         
        #register elements in layout
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.edit1)
        vbox1.addWidget(self.selectLab)
        vbox1.addWidget(self.tselect)
        vbox1.addWidget(self.buttonGo)
        vbox1.addWidget(self.buttonEx)
         
        #set Layout       
        page.setLayout(vbox1)
        self.setCentralWidget(page)
         
        # set keyboard-shortcut
        self.connect(self.buttonGo, SIGNAL("clicked()"), self.transGo)
        self.connect(self.buttonEx, SIGNAL("clicked()"), self.close)
        self.buttonGo.setShortcut("RETURN")
        self.buttonEx.setShortcut("ESC")
        self.edit1.setFocus()
        
        SHORTCUT_SHOW = "CTRL+y"  # Ctrl maps to Command on Mac OS X
        self.shortcut_show.setShortcut(QKeySequence(SHORTCUT_SHOW))
        self.shortcut_show.activated.connect(self.transGo)
	SHORTCUT_CLOSE = "CTRL+<"
        self.shortcut_close.setShortcut(QKeySequence(SHORTCUT_CLOSE))
        self.shortcut_close.activated.connect(self.closePopUp)
     
    
    def closePopUp(self):
	self.msgBox.close()
	# toggle window mini full
	if self.windowState() == Qt.WindowMinimized:
	  # Window is minimised. Restore it.
	  self.setWindowState(Qt.WindowNoState)
	else:
	  self.showMinimized()
	
    def popupMesgBox(self,text):
	if hasattr(self, 'msgBox'):
	  self.msgBox.close()
        # rebuild with closed deleted button
	self.msgBoxCloseButton = QPushButton('OK')
        self.msgBox = QMessageBox()
        self.msgBox.setText(text)
        self.msgBox.addButton(self.msgBoxCloseButton, QMessageBox.YesRole)
        ret = self.msgBox.exec_()
      
    # combobox logic check state even if unchanged
    def changeIndex(self):
        index = self.tselect.currentIndex()
        if index < self.tselect.count() - 1:
            self.tselect.setCurrentIndex(index + 1)
        else:
            self.tselect.setCurrentIndex(0)
     
    # combobox logic
    def setHandle(self,lang):
        self.tlang = self.langDict[str(lang)]
	# init selenium browser
        initSelenium(self)
         
    def transGo(self):
        if not self.edit1.text():
	    # check if window is minimized
	    if self.windowState() == Qt.WindowMinimized:
		# Window is minimised. Restore it.
		self.setWindowState(Qt.WindowNoState)

            self.pushDataToClipB()
            text = self.getDataFClipB()
            transS = self.myTranslate(text)
            self.edit1.clear()
        else:
            text = self.edit1.text()
            transS = self.myTranslate(text)
            self.edit1.clear()
	    #self.gainFocusForPU()
         
        #popup window
        self.popupMesgBox(transS)
        
    def gainFocusForPU(self):
        w = WindowMgr()
        w.find_window_wildcard(".*translation*")
        w.set_foreground()

    def pushDataToClipB(self):
	# push selected data to clipbord
        pyperclip.copy(os.popen('xsel').read())
	
    def getDataFClipB(self):
        # get clipboard data
        # win32clipboard.OpenClipboard()
        # data = win32clipboard.GetClipboardData()
        # win32clipboard.CloseClipboard()
        return pyperclip.paste()
     
    def myTranslate(self,word):
        return getGoogleTranslationFromText(self, unicode(word))
        #return gs.translate(word, tlan)
     
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit?"
        reply = QMessageBox.question(self, 'Message',
                         quit_msg, QMessageBox.Yes, QMessageBox.No)
     
        if reply == QMessageBox.Yes:
            #exitHotkeyMode()
            event.accept()
        else:
            #testHotkeyMode()
            event.ignore()
     
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()