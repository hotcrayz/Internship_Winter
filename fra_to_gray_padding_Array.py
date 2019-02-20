import pandas as pd
import numpy as np
import csv
import re

from numpy import genfromtxt
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

DATA_DIR = "./Fra_Gray_Padding_BBS14/"
OUTPUT_DIR = "./Fra_Gray_Padding_Array_Output/"
OUTPUT_IMG_DIR = "./Fra_Gray_Padding_Img/"
SENSOR_NAME_BASE = "MT_01200049-"
Y_Limits = [(-70, 70), (-20, 20), (-2, 2), (-200, 200)]   # Accelerometer, Gyro, Magnetism, Roll/Pitch/Yaw
Plot_Titles = ["Accelerometer", "Gyro", "Magnetic", "Roll,Pitch,Yaw"]
Maxs = {
    'Acc_X': 70, 'Acc_Y': 70, 'Acc_Z': 70, 'Gyr_X': 20, 'Gyr_Y': 20, 'Gyr_Z': 20, 'Mag_X': 2, 'Mag_Y': 2, 'Mag_Z': 2,
    'Roll': 200, 'Pitch': 200, 'Yaw': 200
}
Mins = {
    'Acc_X': -70, 'Acc_Y': -70, 'Acc_Z': -70, 'Gyr_X': -20, 'Gyr_Y': -20, 'Gyr_Z': -20, 'Mag_X': -2, 'Mag_Y': -2,
    'Mag_Z': -2, 'Roll': -200, 'Pitch': -200, 'Yaw': -200
}

check = 0

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


def   GetStatistics(Data_Dir, check):
   max_col = 0
   min_values = np.zeros(len(View_Cols))
   max_values = np.zeros(len(View_Cols))

   dfs = []
   

   for bbs in range(13,BBS):   
      for subj in range(SUBJECT):   
         for trial in range (TRIAL):   
            for sensor in SensorNames.keys():   
         
               file_name = Data_Dir + "subject"+str(subj+1) + "_" +"trial"+ str(trial+1) + "_" + "bbs" + str(bbs+1) + ".csv"
                  
               df = genfromtxt(file_name, delimiter=',')
                                          
            if(TO_SAVE == True):
               
               
               ##### Make CSV file from each Censor data #####
               
               
               df = np.delete(df, np.s_[:1], 1)
            
               npad = ((0, 0), (0, MAX_COL - df.shape[1]))
               df_padding = np.pad(df, npad, 'constant', constant_values=(0))      
               df_arr = df_padding.flatten()         
               df_arr = pd.DataFrame(df_arr)
               df_arr = df_arr.T
               
            
               if(check==0):
                  df_arr2 = df_arr
               df_arr2=df_arr2.append(df_arr)
               print(df_arr2.shape)   
               print(check)
               if(SAVE_CSV == True):
                  if(check==149):
                     df_arr2=df_arr2.T
                     #np.savetxt(OUTPUT_DIR + "subject"+str(subj+1) + "_" +"trial"+ str(trial+1) + "_" + "bbs" + str(bbs+1) + ".txt", df_arr2, delimiter=',',fmt="%.1f")
                     print("checkcheck3333")
                     print(df_arr2)
                     df_arr2.to_csv("output.txt",sep=',')
                     print("checkcheck, print output!!")
                     print(df_arr2.shape)
                     df_arr2=df_arr2.T
                  
               check = check + 1
               dfs = []

if __name__ == "__main__":
   GetStatistics(DATA_DIR, check)