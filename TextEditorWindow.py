from XmlEditor import Ui_TextEditor
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt5.QtGui import QColor, QTextBlockFormat
from PyQt5 import QtCore
from main import XML
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
import logging, threading, functools
import time
from colorWrongEditor import *


class EditorWindow(QtWidgets.QMainWindow, Ui_TextEditor, QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.line_to_be_colored = 1000

        self.highlight_format = QTextBlockFormat()
        self.highlight_format.setBackground(Qt.red)

        self.format_normal = QTextBlockFormat()
        self.format_normal.setBackground(Qt.white)

        self.xml = XML()
        self.open = 0
        self.textEdit.setFontPointSize(12)
        self.coloring_flag = 0
        
        self.check()

        self.actionOpen.triggered.connect(self.openFile)
        self.logView = QtWidgets.QTextEdit()
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

    def setLineFormat(self, lineNumber, format):
        """ Sets the highlighting of a given line number in the QTextEdit"""
        cursor = self.textEdit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setBlockFormat(self.format_normal)

        cursor = QTextCursor(self.textEdit.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(format)

    def color_2(self):
        data = self.textEdit.toPlainText()

        self.xml.text = data
        # print(data)
        self.textEdit.setText(data)
        cursor = self.textEdit.textCursor()
        # Setup the desired format for matches
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor("red")))
        # Setup the regex engine
        pattern = "Item"
        regex = QtCore.QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.textEdit.toPlainText(), pos)
        # print("Text", self.textEdit.toPlainText())
        while index != -1:
            # print("Iam Here")
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QtGui.QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.textEdit.toPlainText(), pos)

    def check(self):
        data = self.textEdit.toPlainText()

        self.xml.text = data
        begin, text = self.xml.check_format()

        # if not self.coloring_flag and len(self.textEdit.toPlainText()):
            # print(self.coloring_flag)
            # self.coloring_flag = True

            # self.textEdit.append("<span style=\" font-size:12pt; font-weight:400; color:#ff0000;\" > hello world </span>")

        # flag = True
        # if begin > 1:
        #     self.coloring_flag = True
        #
        # if self.coloring_flag:
        #     layout = QtWidgets.QGridLayout()
        #     layout.addWidget(self.logView, 3, 3)
        #     self.setLayout(layout)
        #     self.textEdit.setText('')
        #     self.textEdit.append('started appending s')  # append string
        #     QtWidgets.QApplication.processEvents()  # update gui for pyqt
        #     print("here")
        #     self.coloring_flag = False
        #     first_text = data[:begin]
        #     text_edit = "<span style=\" font-size:12pt; font-weight:600; color:#ff0000;\" >"
        #     text_edit += data[begin]
        #     text_edit += "</span>"
        #     remaining_text = data[begin+1:]
        #     total_text = first_text + text_edit + remaining_text
        #     # print(total_text)
        #     # self.textEdit.setText(total_text)
        #     self.textEdit.append(text_edit)
        #     print(self.textEdit.toPlainText())
            # self.prettify()

            # self.textEdit.setPlainText(total_text)
        # if type(begin) == int:
        #     cursor = self.textEdit.textCursor()
        #     cursor.movePosition(begin-1)
        #     cursor.movePosition(begin, QtGui.QTextCursor.KeepAnchor)
        #     self.textEdit.setTextBackgroundColor(QColor("red"))
        # editor = self.textEdit
        # editor.setStyleSheet("""QPlainTextEdit{
        # 	font-family:'Consolas';
        # 	color: #ccc;
        # 	background-color: #2b2b2b;}""")
        # highlight = PythonHighlighter(editor.document())
        # editor.show()
        # print("1")
        if text:
            print(text.split('\n'))
        if type(begin) == int:
            print(begin)
            begin -= 8
            print(begin)
            index = 0
            # fmt = QTextCharFormat()
            # fmt.setBackground(QColor(255, 0, 0, 50))
            # print(data.split('\n'))
            # print(data[begin: begin+5])ban
            # print(begin)
            for line_number, line in enumerate(text.split('\n')):
                for _ in line:
                    if begin == index:
                        print("HHHHH")
                        print(line_number)
                        self.line_to_be_colored = line_number
                    # print(index)
                    index += 1
                index += 1
            print('line', self.line_to_be_colored)
            self.setLineFormat(self.line_to_be_colored-1, self.highlight_format)
        else:
            self.setLineFormat(self.line_to_be_colored-1, self.format_normal)
            # fmt.setUnderlineStyle(QTextCharFormat::WaveUnderline);
            # self.textEdit.setCurrentCharFormat(fmt)
            # cursor = QTextCursor(self.textEdit.document())
            # # set the cursor position (defaults to 0 so this is redundant)
            # cursor.setPosition(10)
            # self.textEdit.setTextCursor(cursor)
            #
            # # insert text at the cursor
            # self.textEdit.insertPlainText('your text here')
        # if not self.coloring_flag:
        #     self.coloring_flag = True
        # self.color_2()
        # self.textEdit.show()
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
        x, _ = self.xml.check_format()
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
        x, _ = self.xml.check_format()
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