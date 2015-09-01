from draganddrop import FileListDialog, MyFileDropTarget
from experimentsettings import *
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import datetime
import matplotlib
import matplotlib.animation as animation
import numpy as np

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Drop Target",size=(500,300))
        p = wx.Panel(self)

	dia = FileListDialog(self)
	if dia.ShowModal()== wx.ID_OK:
	    filenames =  dia.dropped_file	
	    dia.Destroy()
	    self.Destroy()
	    
	    print filenames
	    
	    #f = open(filename, 'r')
	    #self.lines = [line.strip() for line in f]
	    ##self.sort_timewise()
	    #self.sort_objectwise()
		
		
    def sort_timewise(self):
	timepoints = {}
	ploting_data = []
	meta = ExperimentSettings.getInstance()
	
	for line in self.lines:
	    obj, measurements = line.split('=', 1)
	    obj = obj.strip()
	    measurements = eval(measurements)
	    
	    ROI1=[]
	    ROI2=[]
	    ROI3=[]	    
	     
	    tps = sorted(list(set([measurements[i][0].split(':')[1] for i in range(1,len(measurements))])), key = meta.stringSplitByNumbers)
	    for tp in tps:
		for i, measurment in enumerate(measurements):
		    if i>0 and measurment[0].split(':')[1] == tp:
			if int(measurment[1].split(':')[1]) == 1:  # tp point and ROI number matches
			    ROI1.append(measurment[4].split(':')[1])
			elif int(measurment[1].split(':')[1]) == 2:  
			    ROI2.append(measurment[4].split(':')[1])
			elif int(measurment[1].split(':')[1]) == 3:  
			    ROI3.append(measurment[4].split(':')[1])

	    ploting_data.append(tps)
	    ploting_data.append(ROI1)
	    ploting_data.append(ROI2)
	    ploting_data.append(ROI3)
	 
	f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
	
	f.suptitle('GFP Intensity', fontsize=20)
	ax1.set_ylabel('Nucleus')
	ax2.set_ylabel('Cytoplasm')
	ax3.set_ylabel('Cytoplasm')
	ax3.set_xlabel('Frame Number')
	
	for i in xrange(0,len(ploting_data),4):
	    ax1.plot(ploting_data[i],ploting_data[i+1], color='#568C37')
	    ax2.plot(ploting_data[i],ploting_data[i+2], color='#8EF553')
	    ax3.plot(ploting_data[i],ploting_data[i+3], color='#8EF553')
	    
	plt.show()    
	
    def sort_objectwise(self):
	ploting_data = []
	obj_list = []
	meta = ExperimentSettings.getInstance()
	
	for line in self.lines: # per line represents an object/cell/animal and its associated measurements
	    obj, measurements = line.split('=', 1)
	    obj = obj.strip()
	    measurements = eval(measurements)
	 
	    ROI1=[]
	    ROI2=[]
	    ROI3=[]	    
	     
	    tps = sorted(list(set([measurements[i][0].split(':')[1] for i in range(1,len(measurements))])), key = meta.stringSplitByNumbers)
	    del tps[-1] # last element is the event name this is excluded *** the algorithm needs to be more generic and robust ****
	    for tp in tps:
		for i, measurment in enumerate(measurements):
		    if measurment[0].split(':')[1] == tp: # match time point 
			if int(measurment[1].split(':')[1]) == 1:  # match ROI number
			    ROI1.append(measurment[4].split(':')[1])
			elif int(measurment[1].split(':')[1]) == 2:  
			    ROI2.append(measurment[4].split(':')[1])
			elif int(measurment[1].split(':')[1]) == 3:  
			    ROI3.append(measurment[4].split(':')[1])
		    else:
			obj_list.append(obj)
			    
	    # convert frame numbers to relative time (starting time for each object from 0 )
	    rtps = [i*15 for i, tp in enumerate(tps)]  # 15 mins for each frame interval 
	    ploting_data.append(rtps)
	    ploting_data.append(ROI1)
	    ploting_data.append(ROI2)
	    ploting_data.append(ROI3)
	    
	f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
	
	f.suptitle('GFP Intensity', fontsize=20)
	ax1.set_ylabel('Nucleus')
	ax2.set_ylabel('Cytoplasm')
	ax3.set_ylabel('Cytoplasm')
	ax3.set_xlabel('Time (min)')

	for i in xrange(0,len(ploting_data),4):
	    ax1.plot(ploting_data[i],ploting_data[i+1], color='#568C37')
	    ax2.plot(ploting_data[i],ploting_data[i+2], color='#8EF553')
	    ax3.plot(ploting_data[i],ploting_data[i+3], color='#8EF553')
	    
	#def update_line(num, data, line):
	    #line.set_data(data[...,:num])
	    #return line,	
	
	#fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
	
	#fig.suptitle('GFP Intensity', fontsize=20)
	#ax1.set_ylabel('Nucleus')
	#ax2.set_ylabel('Cytoplasm')
	#ax3.set_ylabel('Cytoplasm')
	#ax3.set_xlabel('Time (min)')	

	#for i in xrange(0,len(ploting_data),4):
	    #nuc_data = np.array([ploting_data[i],ploting_data[i+1]])
	    #cyto1_data = np.array([ploting_data[i],ploting_data[i+2]])
	    #cyto2_data = np.array([ploting_data[i],ploting_data[i+3]])
	
	
	    #line1 = Line2D([], [], color='black')
	    #line2 = Line2D([], [], color='red')
	    #line3 = Line2D([], [], color='green')
	    
	    #ax1.add_line(line1)
	    #ax2.add_line(line2)
	    #ax3.add_line(line3)
	    
	    #plt.xlim(0, 1200)
	    #plt.ylim(0, 600)
		    
	    
	    #nuc_ani = animation.FuncAnimation(fig, update_line, 1200, fargs=(nuc_data, line1), interval=5, blit=True)
	    #cyto1_ani = animation.FuncAnimation(fig, update_line, 1200, fargs=(cyto1_data, line2), interval=5, blit=True)
	    #cyto2_ani = animation.FuncAnimation(fig, update_line, 1200, fargs=(cyto2_data, line3), interval=5, blit=True)
	    
	
	
	    
	
	
	plt.show()  
   
	
  
app = wx.PySimpleApp()
frm = MyFrame()
frm.Show()
app.MainLoop()