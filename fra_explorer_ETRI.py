import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


Skip_Rows = 5
DEBUG = False
SHOW_GRID = True
DROP_NA = True


DATA_DIR = "./Fra_ETRI_Input/"
SENSOR_NAME_BASE = "MT_01200049-"
Y_Limits = [(-70, 70), (-20, 20), (-2, 2), (-200, 200)]	# Accelerometer, Gyro, Magnetism, Roll/Pitch/Yaw
Plot_Titles = ["Accelerometer", "Gyro", "Magnetic", "Roll,Pitch,Yaw"]
View_Cols = [['Acc_X', 'Acc_Y', 'Acc_Z'], ['Gyr_X', 'Gyr_Y', 'Gyr_Z'], ['Mag_X', 'Mag_Y', 'Mag_Z'], ['Roll', 'Pitch', 'Yaw']]
View_ColsAll = ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyr_X', 'Gyr_Y', 'Gyr_Z', 'Mag_X', 'Mag_Y', 'Mag_Z', 'Roll', 'Pitch', 'Yaw']
# Use dictionary type
#BBS_Names = { "bbs1"  : 1, "bbs2"  : 2, "bbs3"  : 3, "bbs4"  : 4, "bbs5"  : 5, "bbs6"  : 6, "bbs7"  : 7,
#		"bbs8"  : 8, "bbs9"  : 9, "bbs10" : 10, "bbs11" : 11, "bbs12" : 12, "bbs13" : 13, "bbs14" : 14 }
BBS_Names = { "bbs11" : 11 }

SensorNames = {
		"Head"  : "00B405F2", 
		"fARM_L": "00B40560", 
		"fArm_R": "00B405D3", 
		"Pelvs" : "00B405F7", 
		"Foot_L": "00B405C0", 
		"Foot_R": "00B405BF" 
	}
# Used to sort Sensor Names
SensorNumbering = { 1 : "Head", 2 : "fARM_L", 3 : "fArm_R", 4 : "Pelvs",
		5: "Foot_L", 6: "Foot_R" }


class MyWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setupUI()

	def setupUI(self):
		# Initialize variables
		self.subject = "subject1"
		self.trial = "trial1"
		self.bbs = str(BBS_Names["bbs11"])
		self.sensor = SensorNames["Pelvs"]

		self.setGeometry(100, 100, 1400, 1000)
		self.setWindowTitle("Fall Risk Assessment Data Viewer v1.0")

		self.comboBoxSubject = QComboBox(self)
		for i in range(1,6):
			self.comboBoxSubject.addItem("subject" + str(i))
		self.comboBoxSubject.activated[str].connect(self.subject_choice)

		self.comboBoxTrial = QComboBox(self)
		for i in range(1,2):
			self.comboBoxTrial.addItem("trial" + str(i))
		self.comboBoxTrial.activated[str].connect(self.trial_choice)

		self.comboBoxBBS = QComboBox(self)
		for bbs in sorted(BBS_Names, key=lambda k : BBS_Names[k]):	# sort with values, not keys
			self.comboBoxBBS.addItem(bbs)
		self.comboBoxBBS.activated[str].connect(self.bbs_choice)

		self.comboBoxSensor = QComboBox(self)
		for sn in SensorNumbering.keys():
			self.comboBoxSensor.addItem(SensorNumbering[sn])
		self.comboBoxSensor.activated[str].connect(self.sensor_choice)

		self.btn_view = QPushButton("View Data")
		self.btn_view.clicked.connect(self.viewData)

		self.btn_quit = QPushButton("Quit")
		self.btn_quit.clicked.connect(self.quitAction)


		# Canvas to plot
		self.fig = plt.Figure()
		self.canvas = FigureCanvas(self.fig)
		self.axes = []
		for i in range(4):
			ax = self.fig.add_subplot(2, 2, i+1)
			self.axes.append(ax)

		self.tableView = QTableView()
		#self.tableView.setRowCount(10)
		#self.tableView.setColumnCount(10)
		self.tableView.setGeometry(QRect(10, 60, 731, 241))


		# Left Layout
		leftLayout = QVBoxLayout()
		leftLayout.addWidget(self.canvas, stretch=2)
		leftLayout.addWidget(self.tableView)

		# Right Layout
		rightLayout = QVBoxLayout()
		rightLayout.addWidget(self.comboBoxSubject)
		rightLayout.addWidget(self.comboBoxTrial)
		rightLayout.addWidget(self.comboBoxBBS)
		rightLayout.addWidget(self.comboBoxSensor)
		rightLayout.addWidget(self.btn_view)
		rightLayout.addStretch(1)
		rightLayout.addWidget(self.btn_quit)

		layout = QHBoxLayout()
		layout.addLayout(leftLayout)
		layout.addLayout(rightLayout)
		layout.setStretchFactor(leftLayout, 1)
		layout.setStretchFactor(rightLayout, 0)

		self.setLayout(layout)

	def subject_choice(self, text):
		if (DEBUG == True):
			print(text, "selected")
		self.subject = text

	def trial_choice(self, text):
		if (DEBUG == True):
			print(text, "selected")
		self.trial = text

	def bbs_choice(self, text):
		if (DEBUG == True):
			print(text, "selected")
		self.bbs = str(BBS_Names[text])

	def sensor_choice(self, text):
		if (DEBUG == True):
			print(text, "selected")
		self.sensor = SensorNames[text]

	def viewData(self):
		f_name = DATA_DIR + self.subject + "/" + self.trial +"/" + "bbs" + self.bbs +"/" + \
			SENSOR_NAME_BASE + "%03d"%(int(self.bbs)-1) + "-000_" + self.sensor + ".txt"
		if (DEBUG == True):
			print(f_name)
		df = pd.read_csv(f_name, skiprows=Skip_Rows)

		# Drop NA columns
		if DROP_NA == True:
			df.dropna(axis = 'columns', how='all', inplace=True)

		# Build Table
		desc = df[View_ColsAll].describe(percentiles=[])

		# Drop some rows
		desc.drop(labels=['count', '50%'], inplace=True)

		model = PandasTableModel(desc.round(1))
		self.tableView.setModel(model)

		for i in range(4):
			self.axes[i].clear()
			self.axes[i].plot(df.index, df[View_Cols[i]])
			self.axes[i].legend(View_Cols[i], loc='upper right')
			self.axes[i].set_ylim(Y_Limits[i])
			self.axes[i].set_title(Plot_Titles[i])

			if (SHOW_GRID == True):
				self.axes[i].grid()

		self.fig.suptitle(f_name)
		self.canvas.draw()

	def quitAction(self):
		qApp.quit()


class PandasTableModel(QAbstractTableModel):
	"""
	Class to populate a table view with a pandas dataframe
	"""
	def __init__(self, data, parent=None):
		QAbstractTableModel.__init__(self, parent)
		self._data = data

	def rowCount(self, parent=None):
		return len(self._data.values)

	def columnCount(self, parent=None):
		return self._data.columns.size

	def data(self, index, role=Qt.DisplayRole):
		if index.isValid():
			if role == Qt.TextAlignmentRole:
				return Qt.AlignCenter
			elif role == Qt.DisplayRole or role == Qt.EditRole:
				return str(self._data.values[index.row()][index.column()])
		return None

	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return self._data.columns[col]
		elif orientation == Qt.Vertical and role == Qt.DisplayRole:
			return self._data.index.tolist()[col]
		return None


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MyWindow()
	window.show()
	app.exec_()
