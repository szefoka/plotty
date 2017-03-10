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
import copy as cp

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
	def __init__(self, datas, legends):
		self.cdfs = []
		for data in zip(datas, legends):
			cdf = CDF(data[0], data[1])
			cdf.CalcCDF()
			self.cdfs.append(cdf)
	
	def DrawCDF (self):
		plot_num = 111
		plt.figure(1)
		i = 0
		for item in self.cdfs:
			plt.subplot(plot_num)
			plt.semilogx(item.bin_edges, item.cdf, label=item.data.legend)
			plt.xticks(fontsize=8)
			plt.grid(True)
			pylab.legend(loc="upper right", fancybox=True, shadow=True, fontsize=8)
			i+=1
			plt.savefig("cdf.jpg", dpi=800)


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
	def __init__ (self, datas, legends):
		self.percentiles = []
		for data in zip(datas, legends):
			perc = Percentile(data[0], data[1])
			perc.calcPercentiles()
			self.percentiles.append(perc)
	
	def DrawPercentiles (self):
		plot_num = 111
		plt.figure(2)
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
		plt.savefig("percentiles.jpg", dpi=800)
	
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
		self.rows = 0;
		self.inputlist = []
		self._window = QDialog()
		self._window.setWindowTitle("Plotty")
		windowLayout = QVBoxLayout()
		self.layout = QGridLayout()
		
		self.CDF = QCheckBox(self._window)
		self.Hist = QCheckBox(self._window)
		self.Perc = QCheckBox(self._window)
		
		self.createLayout()
		windowLayout.addWidget(self._window.horizontalGroupBox)
		self._window.setLayout(windowLayout)
			
	@pyqtSlot()	
	def createLayout (self):
		self._window.horizontalGroupBox = QGroupBox("")
		
		#add widgets		
		addBtn = QPushButton('New')
		createBtn = QPushButton('Create')
		cdfLabel = QLabel("CDF")
		histLabel = QLabel("Hist")
		percLabel = QLabel("Perc")		
		self.layout.addWidget(addBtn,0,0) 
		self.layout.addWidget(createBtn,0,1) 
		self.layout.addWidget(createBtn,0,1) 
		self.layout.addWidget(cdfLabel,0,2)
		self.layout.addWidget(self.CDF,0,3)
		self.layout.addWidget(histLabel,0,4)
		self.layout.addWidget(self.Hist,0,5)
		self.layout.addWidget(percLabel,0,6)
		self.layout.addWidget(self.Perc,0,7)

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
			self.legends.append(cp.deepcopy(str(item.text.text())))
			self.datas.append(cp.deepcopy(data))
			data[:]=[]
			
		if self.CDF.isChecked():
			cdfPlot = CDFPloft(self.datas, self.legends)
			cdfPlot.DrawCDF()
			
		if self.Perc.isChecked():
			percPlot = PercentilePlot(self.datas, self.legends)
			percPlot.DrawPercentiles()
	

a = QApplication(sys.argv)
mywin = Window()
mywin.show()
sys.exit(a.exec_())
