import glob, os


current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

# Directory where the data will reside, relative to 'darknet.exe'
path_data = '/labels'
path_data1 = 'NFPA_dataset/'
full_path = current_dir

for filename in os.listdir(full_path):
	if len(filename) <= 9: 
		print(filename)
		os.remove(filename)
		continue
	else:
        	continue  
