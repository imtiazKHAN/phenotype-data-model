import wx
import xlrd
import re
import os
import ntpath
from collections import defaultdict
from draganddrop import FileListDialog, MyFileDropTarget


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Drop Target",size=(500,300))
        p = wx.Panel(self)

	dia = FileListDialog(self)
	if dia.ShowModal()== wx.ID_OK:
	    filename =  dia.dropped_file	
	    self.save_file_name = os.path.splitext(os.path.basename(filename))[0]
	    self.save_file_path = os.path.abspath(os.path.join(os.path.dirname(filename), '..', 'PhenotypeDB')) 
	    dia.Destroy()
	    self.Destroy()
	    
	self.phenotypic_portfolio = defaultdict(list)
	#worksheets = workbook.sheet_names()

	# Converting FluorTRAK data
	f = open(filename, 'r')
	lines = [line.strip() for line in f]
	
	for line in lines:
	    object_data = line.split('\t')
	    cellularName_frameNum = object_data[0].split('_')
		    	    
	    if len(cellularName_frameNum) == 1:
		self.phenotypic_portfolio[cellularName_frameNum[0]].append( 
		    ("Event: %s" %str(object_data[7]),
		    "Birth Frame Number: %s" %str(object_data[8]),
		    "End Frame Number: %s" %str(object_data[9]),
		    "IMT in Frame Number: %s" %str(object_data[10]),
		    "INTRA mitotic intensity: %s" %str(object_data[12]),
		    "Cell cycle max intensity: %s" %str(object_data[16])))
	    else:				    
		self.phenotypic_portfolio[cellularName_frameNum[0]].append( 
		    ("Frame Number: %s" %str(cellularName_frameNum[1]),
		    "ROI: %s" %str(1),
		    "X Coordinate: %s" %str(object_data[2]),
		    "Y Coordinate: %s" %str(object_data[3]),
		    "Average Intensity: %s" %str(object_data[5])))
		self.phenotypic_portfolio[cellularName_frameNum[0]].append( 
		    ("Frame Number: %s" %str(cellularName_frameNum[1]),
		    "ROI: %s" %str(2),
		    "X Coordinate: %s" %str(object_data[12]),
		    "Y Coordinate: %s" %str(object_data[13]),
		    "Average Intensity: %s" %str(object_data[15])))
		self.phenotypic_portfolio[cellularName_frameNum[0]].append( 
		    ("Frame Number: %s" %str(cellularName_frameNum[1]),
		    "ROI: %s" %str(3),
		    "X Coordinate: %s" %str(object_data[22]),
		    "Y Coordinate: %s" %str(object_data[23]),
		    "Average Intensity: %s" %str(object_data[25])))	
			

	# Converting Balance Beam data convertion
	#workbook = xlrd.open_workbook(filename)
	#worksheet = workbook.sheet_by_name('Balance Beam Data Summary')	
	#num_rows = worksheet.nrows 
	#num_cells = worksheet.ncols
		
	#for curr_row in range(3,num_rows):
	    #mouseNum = str(worksheet.cell(curr_row,0).value).split('-')[1]
	    #self.phenotypic_portfolio[mouseNum].append(
	        #("Genotype: %s" %str(worksheet.cell(curr_row,1).value),
	        #"Sex: %s" %str(worksheet.cell(curr_row,2).value)))
	    #for sp in xrange(4,num_cells,14):
		#self.phenotypic_portfolio[mouseNum].append(
		    #("Age: %s" %str(worksheet.cell(0,sp).value),
		     #"Trial Num: %s" %str(1), 
		     #"Date: %s" %str(worksheet.cell(curr_row,sp).value),
		     #"Turning: %s" %str(worksheet.cell(curr_row,sp+1).value),
		     #"Time Across Beam: %s" %str(worksheet.cell(curr_row,sp+2).value),
		     #"FR: %s" %str(worksheet.cell(curr_row,sp+3).value),
		     #"BR: %s" %str(worksheet.cell(curr_row,sp+4).value),
		     #"FL: %s" %str(worksheet.cell(curr_row,sp+5).value),
		     #"BL: %s" %str(worksheet.cell(curr_row,sp+6).value)))
		#self.phenotypic_portfolio[mouseNum].append(
		    #("Age: %s" %str(worksheet.cell(0,sp).value),
		     #"Trial Num: %s" %str(2),
		     #"Date: %s" %str(worksheet.cell(curr_row,4).value),
		     #"Turning: %s" %str(worksheet.cell(curr_row,sp+7).value),
		     #"Time Across Beam: %s" %str(worksheet.cell(curr_row,sp+8).value),
		     #"FR: %s" %str(worksheet.cell(curr_row,sp+9).value),
		     #"BR: %s" %str(worksheet.cell(curr_row,sp+10).value),
		     #"FL: %s" %str(worksheet.cell(curr_row,sp+11).value),
		     #"BL: %s" %str(worksheet.cell(curr_row,sp+12).value)))	
		     
		
	# Converting Startle test data	     
	#worksheet = workbook.sheet_by_name('3m Startle Test')	
	#num_rows = worksheet.nrows 
	#num_cells = worksheet.ncols
			
	#for curr_row in range(2,num_rows):
	    #mouseNum = str(worksheet.cell(curr_row,3).value)
	    #self.phenotypic_portfolio[mouseNum].append(
	            #("Trial Num: %s" %str(worksheet.cell(curr_row,6).value),
	             #"Trial Type: %s" %str(worksheet.cell(curr_row,7).value),
	             #"Date: %s" %str(worksheet.cell(curr_row,0).value),
	             #"Time: %s" %str(worksheet.cell(curr_row,1).value),
	             #"Chan: %s" %str(worksheet.cell(curr_row,8).value),
	             #"Seq: %s" %str(worksheet.cell(curr_row,9).value),
	             #"Start: %s" %str(worksheet.cell(curr_row,10).value),
	             #"V Max: %s" %str(worksheet.cell(curr_row,11).value),
	             #"T Max: %s" %str(worksheet.cell(curr_row,12).value),
	             #"AVG: %s" %str(worksheet.cell(curr_row,13).value)))
		
	self.save_to_file()
	    
	    
	    
				    		
    def save_to_file(self):
	if self.save_file_path:
	    try:
		f = open(self.save_file_path+"/TRANSFORMED_%s.txt"%self.save_file_name, 'w')
		for tag, value in sorted(self.phenotypic_portfolio.items()):
		    print tag, value
		    f.write('%s = %s\n'%(tag, value))
		f.close()	
	    except IOError:
		import wx
		dial = wx.MessageDialog(None, 'No permission to create file in current directory\nPlease save file in separate directory.', 'Error', wx.OK | wx.ICON_ERROR)
		if dial.ShowModal() == wx.ID_OK:
		    self.save_as_file_dialogue()
				
	    
app = wx.PySimpleApp()
frm = MyFrame()
frm.Show()
app.MainLoop()