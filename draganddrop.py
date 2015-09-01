import wx
import sys

########################################################################        
########       Popup Dialog showing all instances of settings       ####
########################################################################            
class FileListDialog(wx.Dialog):
    def __init__(self, parent):
	wx.Dialog.__init__(self, parent, -1, size=(550,200), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
	self.SetTitle("Attach files")
	self.dropped_file = ''

        self.label = wx.StaticText(self, -1, "Drag and drop file in the box bellow")
        self.text_box = wx.TextCtrl(self, -1, "",style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        self.drop_target = MyFileDropTarget(self.text_box)
        self.text_box.SetDropTarget(self.drop_target)        
	
        self.ok_btn = wx.Button(self, wx.ID_OK)
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL)
        
        # Sizers
	container = wx.BoxSizer(wx.VERTICAL)
	container.Add(self.label, 0, wx.ALL, 5)
	container.Add(self.text_box, 1, wx.EXPAND|wx.ALL, 5)	
	bottom = wx.BoxSizer(wx.HORIZONTAL)
	bottom.Add((0, 0), 1, wx.EXPAND)
	bottom.Add(self.ok_btn)
	bottom.AddSpacer((5,-1))
	bottom.Add(self.cancel_btn)
	container.Add(bottom, 0, wx.ALL|wx.EXPAND, 5)        
        self.SetSizer(container)
        self.Show()
        
    def clearList(self, event):
        self.drop_target.showFiles()

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        
    def OnDropFiles(self, x, y, filenames):
	#if len(filenames)>1:
	    #error_dia = wx.MessageDialog(None, 'Only 1 data file can be reformatted', 'Error', wx.OK | wx.ICON_ERROR)
	    #if error_dia.ShowModal() == wx.ID_OK:	 
		#return	
	for f in filenames:
	    self.window.AppendText("%s\n" %filenames)
	self.window.GetParent().dropped_file = filenames
