import pandas as pd
import numpy as np
import csv

from numpy import genfromtxt
from PIL import Image

MAX_COL = 1964
SENSOR_TOTAL = 132
RGB = 255

SUBJECT = 50
TRIAL = 3
BBS = 14

Skip_Rows = 5
DEBUG = False
#DEBUG = True
DROP_NA = True
GET_MAX_COLS = True
GET_MIN_MAX_VALUES = True
TO_SAVE = True
SAVE_CSV = True
SAVE_IMG = False

DATA_DIR = "/Data/SungNam_Elderly/"
OUTPUT_DIR = "./Fra_Gray_Padding_Output/"
OUTPUT_IMG_DIR = "./Fra_Gray_Padding_Img_Output/"
SENSOR_NAME_BASE = "MT_01200049-"
Y_Limits = [(-70, 70), (-20, 20), (-2, 2), (-200, 200)]	# Accelerometer, Gyro, Magnetism, Roll/Pitch/Yaw
Plot_Titles = ["Accelerometer", "Gyro", "Magnetic", "Roll,Pitch,Yaw"]
Maxs = {
    'Acc_X': 70, 'Acc_Y': 70, 'Acc_Z': 70, 'Gyr_X': 20, 'Gyr_Y': 20, 'Gyr_Z': 20, 'Mag_X': 2, 'Mag_Y': 2, 'Mag_Z': 2,
    'Roll': 200, 'Pitch': 200, 'Yaw': 200
}
Mins = {
    'Acc_X': -70, 'Acc_Y': -70, 'Acc_Z': -70, 'Gyr_X': -20, 'Gyr_Y': -20, 'Gyr_Z': -20, 'Mag_X': -2, 'Mag_Y': -2,
    'Mag_Z': -2, 'Roll': -200, 'Pitch': -200, 'Yaw': -200
}

#View_Cols = [['Acc_X', 'Acc_Y', 'Acc_Z'], ['Gyr_X', 'Gyr_Y', 'Gyr_Z'], ['Mag_X', 'Mag_Y', 'Mag_Z'], ['Roll', 'Pitch', 'Yaw']]
View_Cols = ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyr_X', 'Gyr_Y', 'Gyr_Z', 'Mag_X', 'Mag_Y', 'Mag_Z', 'Roll', 'Pitch', 'Yaw']
# Use dictionary type
BBS_Names = { "bbs1"  : 1, "bbs2"  : 2, "bbs3"  : 3, "bbs4"  : 4, "bbs5"  : 5, "bbs6"  : 6, "bbs7"  : 7,
		"bbs8"  : 8, "bbs9"  : 9, "bbs10" : 10, "bbs11" : 11, "bbs12" : 12, "bbs13" : 13, "bbs14" : 14 }
SensorNames = {
		"Head"  : "00B405F2", 
		"Stern" : "00B405E1", 
		"fARM_L": "00B40560", 
		"fArm_R": "00B405D3", 
		"Pelvs" : "00B405F7", 
		"uLeg_L": "00B405EF", 
		"uLeg_R": "00B40581", 
		"lLeg_L": "00B405A4", 
		"lLeg_R": "00B405FB",
		"Foot_L": "00B405C0", 
		"Foot_R": "00B405BF" 
	}
# Used to sort Sensor Names
SensorNumbering = { 1 : "Head", 2 : "Stern", 3 : "fARM_L", 4 : "fArm_R", 5 : "Pelvs",
		6 : "uLeg_L", 7 : "uLeg_R", 8 : "lLeg_L", 9 : "lLeg_R", 10: "Foot_L", 11: "Foot_R" }

def	GetStatistics(Data_Dir):
	max_col = 0
	min_values = np.zeros(len(View_Cols))
	max_values = np.zeros(len(View_Cols))

	dfs = []
	COUNT = 0

	for bbs in range(13,BBS):	
		for subj in range(SUBJECT):	
			for trial in range (TRIAL):	
				for sensor in SensorNames.keys():	
					f_name = Data_Dir + "subject" + str(subj+1) + "/" + "trial" + str(trial+1) +"/" + "bbs" + str(bbs+1) +"/" + \
						SENSOR_NAME_BASE + "%03d"%(bbs) + "-000_" + SensorNames[sensor] + ".txt"
					
					file_name = "subject"+str(subj+1) + "_" +"trial"+ str(trial+1) + "_" + "bbs" + str(bbs+1)
						
					df = pd.read_csv(f_name, skiprows=Skip_Rows)
					
					df.dropna(axis='columns', how='all', inplace=True)
					df.drop(columns=['PacketCounter'], inplace=True)
					
					#print("checkcheckcheckcheckcheckcheck11111")
					#print(file_name)
					#print(df.shape)
					
					for col in View_Cols:
						df[col] = (df[col] - Mins[col]) * RGB / (Maxs[col] - Mins[col] + 1)
					dfs.append(df)
				
				fdf = pd.concat(dfs, axis=1, sort=False)  
					
				desc = fdf[View_Cols].describe(percentiles=[])
				img = fdf.astype(float).transpose().values
						
				if(TO_SAVE == True):
					
					
					##### Make CSV file from each Censor data #####
					csv_file = pd.DataFrame(img)	
					
					df = csv_file.values
					df = np.delete(df, np.s_[:1], 1)

					npad = ((0, 0), (0, MAX_COL - df.shape[1]))
					df_padding = np.pad(df, npad, 'constant', constant_values=(0))
					
					
					##### Make JPG file from each Censor file #####
					#img_data = genfromtxt(OUTPUT_DIR + str(file_name) + ".csv", delimiter=',')
					#img_data = np.array(img_data)
					#img_data = Image.fromarray(img_data)
					#img_data = img_data.convert('RGB')
					
					# Save CSV file
					if(SAVE_CSV == True):
						print(str(file_name))
						np.savetxt(OUTPUT_DIR + str(file_name) + ".csv", df_padding, delimiter=',',fmt="%.1f")
					
					if(SAVE_IMG == True):
					    print(str(file_name))
					    img_data.save(OUTPUT_IMG_DIR + str(file_name)+".jpg")
						
					COUNT = COUNT + 1
					dfs = []

if __name__ == "__main__":
	GetStatistics(DATA_DIR)
