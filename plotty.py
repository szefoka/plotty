import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pylab
from pylab import xticks
import sys
import os
import math

class Data:
	def __init__ (self, vals, legend):
		self.vals = vals
		self.legend = legend
		

class CDF:
	def __init__ (self, vals, legend):
		self.data = Data(vals, legend)
		self.bin_edges = []
		self.counts = []
		self.cdf = []
	
	def CalcCDF (self):
		num_bins = int(len(self.data.vals)/10)
		self.counts, self.bin_edges = np.histogram(self.data.vals, bins=num_bins, normed=False)
		self.cdf = np.cumsum(self.counts)
		tmp = self.cdf.tolist()

		newList = []
		for item in self.cdf.tolist():
			newList.append(float(item)/len(self.data.vals))

		self.cdf = newList
		self.cdf.insert(0,0)
		
class CDFPloft:
	def __init__(self, datas, legends, filename, title, xlabel, ylabel):
		self.fn = filename
		self.title = title
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.cdfs = []
		for data in zip(datas, legends):
			cdf = CDF(data[0], data[1])
			cdf.CalcCDF()
			self.cdfs.append(cdf)
	
	def DrawCDF (self):
		plt.gcf().clear()
		plot_num = 111
		plt.figure(1)
		plt.title(self.title)
		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)
		i = 0
		for item in self.cdfs:
			plt.subplot(plot_num)
			plt.semilogx(item.bin_edges, item.cdf, label=item.data.legend)
			plt.xticks(fontsize=8)
			plt.grid(True)
			pylab.legend(loc="upper right", fancybox=True, shadow=True, fontsize=8)
			i+=1
			plt.savefig(self.fn + "_cdf.jpg", dpi=800)


class Percentile:
	def __init__ (self, vals, legend):
		self.data = Data(vals, legend)
		self.percentiles = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 99.9, 99.99, 99.999]
		self.results = []
		
	def calcPercentiles (self):
		tmp_vals = self.data.vals
		tmp_vals.sort()
		my_vals = np.array(tmp_vals)
		for p in self.percentiles:
			self.results.append(np.percentile(my_vals, p))
		self.results.append(max(tmp_vals))

class PercentilePlot:
	def __init__ (self, datas, legends, filename, title, xlabel, ylabel):
		self.percentiles = []
		for data in zip(datas, legends):
			perc = Percentile(data[0], data[1])
			perc.calcPercentiles()
			self.percentiles.append(perc)
			self.fn = filename
			self.title = title
			self.xlabel = xlabel
			self.ylabel = ylabel
	
	def DrawPercentiles (self):
		plt.gcf().clear()
		plot_num = 111
		plt.figure(2)
		plt.title(self.title)
		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)
		for item in self.percentiles:
			plt.subplot(plot_num)
			item.percentiles.append(1)
			plt.plot(range(0, len(item.results)), item.results, label=item.data.legend)
			xticks = []
			for tick in item.percentiles:
				xticks.append(str(tick))
			xticks[-1]="max"
			plt.xticks(range(0, len(xticks)), xticks ,fontsize=8)
		pylab.legend(loc="upper left", fancybox=True, shadow=True, fontsize=7)
		plt.grid(True)
		plt.savefig(self.fn + "_percentiles.jpg", dpi=800)
	
#class Histogram:
	



class InputRow:
	def __init__(self, window):
		self.window = window
		self.fn = QLineEdit()
		self.fn.setFixedWidth(200)
		self.fn.setText(QFileDialog.getOpenFileName(window, 'Open File', '/'))
		self.text = QLineEdit()
		self.text.setFixedWidth(200)
		self.fnLabel = QLabel("Filename:")
		self.descLabel = QLabel("Description:")
		self.modButton = QPushButton('Choose')
		self.modButton.clicked.connect(self.fnModify)
		
	def fnModify (self):
		self.fn.setText(QFileDialog.getOpenFileName(self.window, 'Open File', '/'))
		
		

class Window:
	def __init__ (self):
		self.datas = []
		self.legends = []
		self.rows = 3;
		self.inputlist = []
		self._window = QDialog()
		self._window.setWindowTitle("Plotty")
		windowLayout = QVBoxLayout()
		self.layout = QGridLayout()
		
		self.CDF = QCheckBox(self._window)
		self.Hist = QCheckBox(self._window)
		self.Perc = QCheckBox(self._window)
		self.fileName = QLineEdit(self._window)
		self.fileName.setFixedWidth(200)
		
		self.titleText = QLineEdit(self._window)
		self.titleText.setFixedWidth(200)
		self.CDFXLabelText = QLineEdit(self._window)
		self.CDFXLabelText.setFixedWidth(200)
		self.CDFYLabelText = QLineEdit(self._window)
		self.CDFYLabelText.setFixedWidth(200)
		
		self.HistXLabelText = QLineEdit(self._window)
		self.HistXLabelText.setFixedWidth(200)
		self.HistYLabelText = QLineEdit(self._window)
		self.HistYLabelText.setFixedWidth(200)
		
		self.PercXLabelText = QLineEdit(self._window)
		self.PercXLabelText.setFixedWidth(200)
		self.PercYLabelText = QLineEdit(self._window)
		self.PercYLabelText.setFixedWidth(200)
		
		self.createLayout()
		windowLayout.addWidget(self._window.horizontalGroupBox)
		self._window.setLayout(windowLayout)
			
	@pyqtSlot()	
	def createLayout (self):
		self._window.horizontalGroupBox = QGroupBox("")
		
		#add widgets		
		addBtn = QPushButton('New')
		createBtn = QPushButton('Create')
		
		#first row
		self.layout.addWidget(addBtn,0,0) 
		self.layout.addWidget(createBtn,0,1) 
		#self.layout.addWidget(createBtn,0,1) 
		self.layout.addWidget(QLabel("Filename: "), 0, 2)
		self.layout.addWidget(self.fileName, 0, 3)
		self.layout.addWidget(QLabel("Title: "), 0, 4)
		self.layout.addWidget(self.titleText, 0, 5)
		
		#second row for CDF
		self.layout.addWidget(QLabel("CDF"),1,0)
		self.layout.addWidget(self.CDF,1,1)
		self.layout.addWidget(QLabel("X label: "), 1, 2)
		self.layout.addWidget(self.CDFXLabelText, 1, 3)
		self.layout.addWidget(QLabel("Y label: "), 1, 4)
		self.layout.addWidget(self.CDFYLabelText, 1, 5)
		
		#third row for Histogram
		self.layout.addWidget(QLabel("Hist"),2,0)
		self.layout.addWidget(self.Hist,2,1)
		self.layout.addWidget(QLabel("X label: "), 2, 2)
		self.layout.addWidget(self.HistXLabelText, 2, 3)
		self.layout.addWidget(QLabel("Y label: "), 2, 4)
		self.layout.addWidget(self.HistYLabelText, 2, 5)
		
		#fourth row for Percentiles
		self.layout.addWidget(QLabel("Perc"),3,0)
		self.layout.addWidget(self.Perc,3,1)
		self.layout.addWidget(QLabel("X label: "), 3, 2)
		self.layout.addWidget(self.PercXLabelText, 3, 3)
		self.layout.addWidget(QLabel("Y label: "), 3, 4)
		self.layout.addWidget(self.PercYLabelText, 3, 5)
		
		#button events
		addBtn.clicked.connect(self.addNewRow)
		createBtn.clicked.connect(self.createPlot)
		

		self._window.horizontalGroupBox.setLayout(self.layout)
				
		
	def show (self):
		self._window.show()
		
	@pyqtSlot()
	def addNewRow (self):
		self.rows += 1
		row = InputRow(self._window)
		self.inputlist.append(row)
		self.layout.addWidget(row.fnLabel, self.rows, 0)
		self.layout.addWidget(row.fn, self.rows, 1)
		self.layout.addWidget(row.descLabel, self.rows, 2)
		self.layout.addWidget(row.text, self.rows, 3)
		self.layout.addWidget(row.modButton, self.rows, 4)
	
	@pyqtSlot()
	def createPlot (self):
		self.datas[:] = []
		self.legends[:] = []
		self.legends[:] = []
		for item in self.inputlist:
			raw_data = []
			data = []
			with open (str(item.fn.text())) as f:
				raw_data = f.readlines()
			for val in raw_data:
				try:
					data.append(float(val))
				except:
					pass
			self.legends.append((str(item.text.text())))
			self.datas.append((data))
			
		if self.CDF.isChecked():
			cdfPlot = CDFPloft(self.datas, 
							   self.legends,
							   str(self.fileName.text()),
							   str(self.titleText.text()),
							   str(self.CDFXLabelText.text()),
							   str(self.CDFYLabelText.text()))
			cdfPlot.DrawCDF()
			
		if self.Perc.isChecked():
			percPlot = PercentilePlot(self.datas,
									  self.legends,
									  str(self.fileName.text()),
									  str(self.titleText.text()),
									  str(self.PercXLabelText.text()),
									  str(self.PercYLabelText.text()))
			percPlot.DrawPercentiles()
	

a = QApplication(sys.argv)
mywin = Window()
mywin.show()
sys.exit(a.exec_())
