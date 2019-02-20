# Uses python3.x
# Requires Keras

all:
	@echo " "	
	@echo "fg_pd_sv: Saving the FRA Data to Gray Image with padding (132*2000)"
	@echo "fg_img_cl_fs: FRA Image Data Clustering With Feature Selection"
	@echo "fe_ET: FRA_ETRI Data Explorer"
	@echo " "	

fg_pd_sv:
	python3 fra_to_gray_padding_save_CSV_OR_JPG.py

fg_img_cl_fs:
	python3 fra_imgcluster_feature_extract.py

fe_ET:
	python3 fra_explorer_ETRI.py

