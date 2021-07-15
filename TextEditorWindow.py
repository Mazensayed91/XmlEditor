from XmlEditor import Ui_TextEditor
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt5.QtGui import QColor
from main import XML
import logging, threading, functools
import time

class EditorWindow(QtWidgets.QMainWindow, Ui_TextEditor):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.xml = XML()
        self.open = 0
        self.textEdit.setFontPointSize(12)
        
        self.check()

        self.actionOpen.triggered.connect(self.openFile)
        self.actionClose.triggered.connect(self.closeFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionCompressed_file.triggered.connect(self.compressedFile)
        self.actionJSON_file.triggered.connect(self.jsonFile)
        self.actionXML_file.triggered.connect(self.xmlFile)
        self.actionError_Fixation.triggered.connect(self.Error_Fixation)
        self.actionPrettifying.triggered.connect(self.prettify)
        self.actionMinifying.triggered.connect(self.minify)
        self.actionCopy.triggered.connect(self.copy)
        self.actionCut.triggered.connect(self.cut)
        self.actionPaste.triggered.connect(self.paste)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionFont.triggered.connect(self.font)
        self.actionBackground_Color.triggered.connect(self.backColor)
        self.actionText_Color.triggered.connect(self.color)

        self.show()
    
    def check(self):
        data = self.textEdit.toPlainText()
        self.xml.text = data
        begin = self.xml.check_format()
        # if type(begin) == int:
        #     cursor = self.textEdit.textCursor()
        #     cursor.movePosition(begin-1)
        #     cursor.movePosition(begin, QtGui.QTextCursor.KeepAnchor)
        #     self.textEdit.setTextBackgroundColor(QColor("red"))
        self.timer = threading.Timer(2, self.check)
        self.timer.start()


    def closeEvent(self, event):
        self.timer.cancel()

    def newFile(self):
        self.open = 0
        self.textEdit.clear()

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', filter="*.xml *.bin")
        if filename[0]:
            if filename[0][-4:] == '.xml':
                self.xml.open(filename[0])
                self.textEdit.setText(self.xml.text)
                self.textEdit.setFontPointSize(12)
                self.open = 1
            elif filename[0][-4:] == '.bin':
                self.xml.decompress(filename[0])
                self.xml.fix_errors()
                self.xml.prettify()
                self.textEdit.setText(self.xml.text)
                self.textEdit.setFontPointSize(12)


    def closeFile(self):
        self.open = 0
        self.textEdit.clear()

    def saveFile(self):
        if self.open:
            data = self.textEdit.toPlainText()
            self.xml.text = data
            self.xml.save()
        else:
            self.xmlFile()

    def compressedFile(self):
        data = self.textEdit.toPlainText()
        self.xml.text = data
        x = self.xml.check_format()
        if (x == True) and (type(x) == bool):
            filename = QFileDialog.getSaveFileName(self, 'Save file', filter="*xml *jon *bin")
            if filename[0]:
                self.xml.save_as(filename[0], 'Compressed')
                QMessageBox.about(self, 'Save File', "File compressed successfully")
        else:
            QMessageBox.warning(self, 'Save File', "File contains errors can not be compressed")


    def jsonFile(self):
        data = self.textEdit.toPlainText()
        self.xml.text = data
        x = self.xml.check_format()
        if (x == True) and (type(x) == bool):
            filename = QFileDialog.getSaveFileName(self, 'Save file', filter="*xml *jon *bin")
            if filename[0]:

                self.xml.save_as(filename[0], 'JSON')
                QMessageBox.about(self, 'Save File', "File converted to Json successfully")
        else:
            QMessageBox.warning(self, 'Save File', "File contains errors can not be converted to Json")
            

    def xmlFile(self):
        data = self.textEdit.toPlainText()
        self.xml.text = data
        filename = QFileDialog.getSaveFileName(self, 'Save file', filter="*xml *jon *bin")
        if filename[0]:
            self.xml.save_as(filename[0], 'XML')
            self.open = 1

    def copy(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedText = textSelected

    def paste(self):
        self.textEdit.append(self.copiedText)

    def cut(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedText = textSelected
        self.textEdit.cut()

    def Error_Fixation(self):
        data = self.textEdit.toPlainText()
        self.xml.text = data
        self.xml.fix_errors()
        self.textEdit.setText(self.xml.text)
        self.textEdit.setFontPointSize(12)
           
            
    def prettify(self):
        data = self.textEdit.toPlainText()
        self.xml.text = data
        self.xml.prettify()
        self.textEdit.setText(self.xml.text)
        self.textEdit.setFontPointSize(12)
            
    def minify(self):
        data = self.textEdit.toPlainText()
        self.xml.text = data
        self.xml.minimize()
        self.textEdit.setText(self.xml.text)
        self.textEdit.setFontPointSize(12)

    def font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def color(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def backColor(self):
        color = QColorDialog.getColor()
        print(color)
        self.textEdit.setTextBackgroundColor(color)