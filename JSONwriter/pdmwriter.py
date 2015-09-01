import json

# Create a dictionary (a key-value-pair structure in Python)
my_dict = {                   
  'Name':      'KAIRA',
  'Location':  u'Kilpisj\u00E4rvi',
  'Longitude': 20.76,
  'Latitude':  69.07
}  

# Open a file for writing
out_file = open("C:\\Users\\Imtiaz\\Dropbox\\Research_PDM\\Software\\JSONwriter\\test.json","w")

# Save the dictionary into this file
# (the 'indent=4' is optional, but makes it more readable)
json.dump(my_dict,out_file, indent=4)                                    

# Close the file
out_file.close()
 