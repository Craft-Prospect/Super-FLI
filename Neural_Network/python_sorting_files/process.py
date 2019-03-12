import glob, os

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

# Directory where the data will reside, relative to 'darknet.exe'
path_data = '/labels'
path_data1 = 'labels/'
full_path = current_dir + path_data

# Percentage of images to be used for the test set
percentage_test = 10;

# Create and/or truncate train.txt and test.txt
file_train = open('train.txt', 'w')  
file_test = open('test.txt', 'w')
print("hello")
# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  
for pathAndFilename in glob.iglob(os.path.join(full_path, "*.png")):  
    print(pathAndFilename)
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    print("Do we get here: 1")
    if counter == index_test:
        counter = 1
        file_test.write(path_data1 + title + '.png' + "\n")
	file_test.write(path_data1 + title + '.txt' + "\n")
	print("Do we get here")
    else:
	print("Do we get here: 2")
        file_train.write(path_data1 + title + '.png' + "\n")
	file_test.write(path_data1 + title + '.txt' + "\n")
        counter = counter + 1
