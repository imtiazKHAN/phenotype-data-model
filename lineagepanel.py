import wx
import os
import re
import subprocess
import numpy as np
import icons
import timeline
import  wx.lib.dialogs
import math
import bisect
import csv
from operator import itemgetter
from wx.lib.combotreebox import ComboTreeBox
from PIL import Image
from time import time
from datalinkList import *
from notepad import NotePad
from draganddrop import FileListDialog, MyFileDropTarget

# x-spacing modes for timeline and lineage panels
SPACE_EVEN = 0
SPACE_TIME = 1
SPACE_TIME_COMPACT = 2

meta = exp.ExperimentSettings.getInstance()

class LineageFrame(wx.ScrolledWindow):
    def __init__(self, parent, id=-1, **kwargs):
        wx.ScrolledWindow.__init__(self, parent, id, **kwargs)
        
        sw = self
        timeline_panel = TimelinePanel(sw)
        self.timeline_panel = timeline_panel
        lineage_panel = LineagePanel(sw)
        self.lineage_panel = lineage_panel
        timeline_panel.set_style(padding=20)
        lineage_panel.set_style(padding=20, flask_gap = 40)
        #sw.SetSizer(wx.BoxSizer(wx.VERTICAL))
        #sw.Sizer.Add(timeline_panel, 0, wx.EXPAND|wx.LEFT, 40)
        #sw.Sizer.Add(lineage_panel, 1, wx.EXPAND)
        #sw.SetScrollbars(20, 20, self.Size[0]/20, self.Size[1]/20, 0, 0)
        
        #tb = self.CreateToolBar(wx.TB_HORZ_TEXT|wx.TB_FLAT)
        #tb.AddControl(wx.StaticText(tb, -1, 'zoom'))
        #self.zoom = tb.AddControl(wx.Slider(tb, -1, style=wx.SL_AUTOTICKS|wx.VERTICAL)).GetControl()
        #self.zoom.SetRange(1, 30)
        #self.zoom.SetValue(8)       
        #tb.Realize()
	self.zoom = wx.Slider(sw, -1, size=(-1, 70), style=wx.SL_AUTOTICKS|wx.VERTICAL|wx.SL_INVERSE|wx.SL_LEFT)
        self.zoom.SetRange(1, 30)
	self.zoom.SetValue(8)
	self.Bind(wx.EVT_SLIDER, self.on_zoom, self.zoom)
	
	zoom_sizer = wx.BoxSizer(wx.VERTICAL)
	zoom_sizer.Add(wx.StaticText(sw, -1, 'Zoom'), 0)
	zoom_sizer.Add(self.zoom, 0)
	time_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
	time_panel_sizer.Add(zoom_sizer, 0, wx.RIGHT, 5)
	time_panel_sizer.Add(timeline_panel, 1, wx.EXPAND)
	
	
        sw.SetSizer(wx.BoxSizer(wx.VERTICAL))
	sw.Sizer.Add(time_panel_sizer, 0, wx.EXPAND)
        sw.Sizer.Add(lineage_panel, 1, wx.EXPAND)
        sw.SetScrollbars(20, 20, self.Size[0]/20, self.Size[1]/20, 0, 0)	
	
	
        #from f import TreeCtrlComboPopup
        #cc = wx.combo.ComboCtrl(sw)
        #self.tcp = TreeCtrlComboPopup()
        #cc.SetPopupControl(self.tcp)
        #sw.Sizer.Add(cc)
        #meta.add_subscriber(self.on_metadata_changed, '')
        
        #self.Bind(wx.EVT_SLIDER, self.on_zoom, self.zoom)
        #self.Bind(wx.EVT_CHECKBOX, self.on_change_spacing, x_spacing)
        #self.Bind(wx.EVT_BUTTON, self.generate_random_data, generate)
        
    def on_metadata_changed(self, tag):
        self.tcp.Clear()
        alltags = meta.get_field_tags()
        t0 = set([tag.split('|')[0] for tag in alltags])
        for t in t0:
            item1 = self.tcp.AddItem(t)
            t1 = set([tag.split('|')[1] for tag in meta.get_field_tags(t)])
            for tt in t1:
                item2 = self.tcp.AddItem(tt, item1)
                t2 = set([tag.split('|')[2] for tag in meta.get_field_tags('%s|%s'%(t,tt))])
                for ttt in t2:
                    item3 = self.tcp.AddItem(ttt, item2)

    def on_zoom(self, evt):
        #self.lineage_panel.set_style(node_radius=self.zoom.GetValue(),
                                     #xgap=self.lineage_panel.NODE_R*2+1,
                                     #ygap=self.lineage_panel.NODE_R*2+1)
	self.lineage_panel.set_style(icon_size=self.zoom.GetValue(),
	                             xgap=self.lineage_panel.ICON_SIZE*2+1,
	                             ygap=self.lineage_panel.ICON_SIZE*2+1)	
        self.timeline_panel.set_style(icon_size=self.zoom.GetValue()*2,
                                      xgap=self.timeline_panel.ICON_SIZE+2)
        
    def on_change_spacing(self, evt):
        if evt.Checked():
            self.lineage_panel.set_x_spacing(SPACE_TIME)
            self.timeline_panel.set_x_spacing(SPACE_TIME)
        else:
            self.lineage_panel.set_x_spacing(SPACE_EVEN)
            self.timeline_panel.set_x_spacing(SPACE_EVEN)
    
    #def generate_random_data(self, evt=None):
        #exp.PlateDesign.add_plate('test', PLATE_TYPE)
        #allwells = exp.PlateDesign.get_well_ids(exp.PlateDesign.get_plate_format('test'))
        #event_types = ['AddProcess|Stain|Wells|0|',
                       #'AddProcess|Wash|Wells|0|',
                       #'AddProcess|Dry|Wells|0|',
                       #'AddProcess|Spin|Wells|0|',
                       #'Perturbation|Chemical|Wells|0|',
                       #'Perturbation|Bio|Wells|0|',
                       #'DataAcquis|TLM|Wells|0|',
                       #'DataAcquis|FCS|Wells|0|',
                       #'DataAcquis|HCS|Wells|0|',
	               #'DataAcquis|RHE|Wells|0|',
                       #'Transfer|Seed|Wells|0|',
                       #'Transfer|Harvest|Wells|0|']
        ## GENERATE RANDOM EVENTS ON RANDOM WELLS
        #for t in list(np.random.random_integers(0, MAX_TIMEPOINT, N_TIMEPOINTS)):
            #for j in range(np.random.randint(1, N_FURCATIONS)):
                #np.random.shuffle(allwells)
                #well_ids = [('test', well) for well in allwells[:np.random.randint(1, len(allwells)+1)]]
                ##timeline.add_event(t, 'event%d'%(t), well_ids)
                #etype = event_types[np.random.randint(0,len(event_types))]
                #meta.set_field('%s%s'%(etype, t), well_ids)
		
    def set_hover_timepoint(self, hover_timepoint):
	self.timeline_panel.hover_timepoint = hover_timepoint
	self.lineage_panel.set_timepoint(hover_timepoint)


class TimelinePanel(wx.Panel):
    '''An interactive timeline panel
    '''
    # Drawing parameters
    PAD = 0.0
    ICON_SIZE = 16.0
    MIN_X_GAP = ICON_SIZE + 2
    TIC_SIZE = 10
    FONT_SIZE = (5,10)
    NOTE_ICON_FACTOR = 0.0
    ATTACH_ICON_FACTOR = 0.0

    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)

        meta.add_subscriber(self.on_timeline_updated, exp.get_matchstring_for_subtag(2, 'Well'))
        self.timepoints = None
        self.events_by_timepoint = None
        self.cursor_pos = None
        self.hover_timepoint = None
        self.time_x = False
        
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_MOTION, self._on_mouse_motion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._on_mouse_exit)
        self.Bind(wx.EVT_LEFT_UP, self._on_click)
        
    def set_style(self, padding=None, xgap=None, icon_size=None):
        if padding is not None:
            self.PAD = padding
        if xgap is not None:
            self.MIN_X_GAP = xgap
        if icon_size is not None:
            self.ICON_SIZE = icon_size
        self._recalculate_min_size()
        self.Refresh(eraseBackground=False)
        
    def set_x_spacing(self, mode):
        if mode == SPACE_TIME:
            self.time_x = True
        elif mode == SPACE_EVEN:
            self.time_x = False
        self._recalculate_min_size()
        self.Refresh(eraseBackground=False)

    def on_timeline_updated(self, tag):
        timeline = meta.get_timeline()
        self.events_by_timepoint = timeline.get_events_by_timepoint()
        self.timepoints = timeline.get_unique_timepoints()
         #for time compact x-spacing
        if len(self.timepoints) > 1:
            self.min_time_gap = min([y-x for x,y in zip(self.timepoints[:-1], 
                                                        self.timepoints[1:])])
        else:
            self.min_time_gap = 1
        self._recalculate_min_size()
        self.Refresh(eraseBackground=False)
	self.Parent.FitInside()
	
    def on_note_icon_add(self):
	note_num = {}
	for tag in meta.global_settings: 
	    if tag.startswith('Notes') or tag.startswith('Attachments'):
		timepoint = exp.get_tag_attribute(tag)
		if not timepoint in note_num:
		    note_num[timepoint] = 1
		else:
		    note_num[timepoint] += 1	
	if note_num:
	    self.NOTE_ICON_FACTOR = (max(note_num.values())+1) * self.ICON_SIZE
	    self._recalculate_min_size()
	    self.Refresh(eraseBackground=False)
	    self.Parent.FitInside()
    
    def on_attach_icon_add(self):
	attach_num = {}
	for tag in meta.global_settings: 
	    if tag.startswith('Attachments'):
		timepoint = exp.get_tag_attribute(tag)
		if not timepoint in attach_num:
		    attach_num[timepoint] = 1
		else:
		    attach_num[timepoint] += 1	
	if attach_num:
	    self.NOTE_ICON_FACTOR = (max(attach_num.values())+1) * self.ICON_SIZE
	    self._recalculate_min_size()
	    self.Refresh(eraseBackground=False)
	    self.Parent.FitInside()    
	
    def _recalculate_min_size(self):
        if self.timepoints is not None and len(self.timepoints) > 0:
	    min_h = self.NOTE_ICON_FACTOR + self.PAD * 2 + self.FONT_SIZE[1] + self.TIC_SIZE * 2 + 1
            if self.time_x:
                self.SetMinSize((self.PAD * 2 + self.MIN_X_GAP * self.timepoints[-1], min_h))
            else:
                self.SetMinSize((len(self.timepoints) * self.MIN_X_GAP + self.PAD * 2, min_h))

    def _on_paint(self, evt=None):
        '''Handler for paint events.
        '''
        if not self.timepoints:
            evt.Skip()
            return

        PAD = self.PAD + self.ICON_SIZE / 2.0
        ICON_SIZE = self.ICON_SIZE
        MIN_X_GAP = self.MIN_X_GAP
        TIC_SIZE = self.TIC_SIZE
        FONT_SIZE = self.FONT_SIZE
        MAX_TIMEPOINT = self.timepoints[-1]
	WIGGEL_NUM = 100
        self.hover_timepoint = None
	self.curr_note_tag = None
	self.on_note_icon_add()
	#self.current_atag = None
	#self.on_attach_icon_add()

        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.BeginDrawing()

        w_win, h_win = (float(self.Size[0]), float(self.Size[1]))
        if self.time_x:
            if MAX_TIMEPOINT == 0:
                px_per_time = 1
            else:
                px_per_time = max((w_win - PAD * 2.0) / MAX_TIMEPOINT,
                                  MIN_X_GAP)
	else:
	    px_per_time = 1
        
        if len(self.timepoints) == 1:
            x_gap = 1
        else:
            x_gap = max(MIN_X_GAP, 
                        (w_win - PAD * 2) / (len(self.timepoints) - 1))

        # y pos of line
        y = h_win - PAD - FONT_SIZE[1] - TIC_SIZE - 1
	
	
	def icon_hover(mouse_pos, icon_pos, icon_size):
	    '''returns whether the mouse is hovering over an icon
	    '''
	    if mouse_pos is None:
		return False
	    MX,MY = mouse_pos
	    X,Y = icon_pos
	    return (X - icon_size/2.0 < MX < X + icon_size/2.0 and 
	            Y - icon_size/2.0 < MY < Y + icon_size/2.0)	

	# draw the timeline
	if self.time_x:	    
	    dc.DrawLine(PAD, y, 
	                px_per_time * MAX_TIMEPOINT + PAD, y)
	else:   
	    dxs = range(WIGGEL_NUM+1)
	    dxs = [float(dx)/WIGGEL_NUM for dx in dxs]

	    x = PAD
	    for i, timepoint in enumerate(self.timepoints):
		if i > 0:
		    n = math.sqrt(((self.timepoints[i]-self.timepoints[i-1])))  #instead of log can use square root
		    ys = [5*(math.sin((math.pi)*dx))*math.sin(2*math.pi*dx*n) for dx in dxs] # 10 is px height fow wiggles can change it
		    for p, dx in enumerate(dxs[:-1]):
			dc.DrawLine(x+x_gap*dxs[p], y+ys[p], x+x_gap*dxs[p+1], y+ys[p+1])
		    x += x_gap

	font = dc.Font
	font.SetPixelSize(FONT_SIZE)
	dc.SetFont(font)
	
	# draw the ticks
        for i, timepoint in enumerate(self.timepoints):
	    # if data acquisition is the only event in this timepoint skip it
	    #evt_categories = list(set([exp.get_tag_stump(ev.get_welltag(), 1) for ev in self.events_by_timepoint[timepoint]]))
	    #if all(evt_categories[0] == cat and cat == 'DataAcquis' for cat in evt_categories):
		#continue
	
            # x position of timepoint on the line
            if self.time_x:
                x = timepoint * px_per_time + PAD
            else:
                x = i * x_gap + PAD
                
            if (self.cursor_pos is not None and 
                x - ICON_SIZE/2 < self.cursor_pos[0] < x + ICON_SIZE/2):
                dc.SetPen(wx.Pen(wx.BLACK, 3))
                self.hover_timepoint = timepoint
            else:
                dc.SetPen(wx.Pen(wx.BLACK, 1))
            # Draw tic marks
            dc.DrawLine(x, y - TIC_SIZE, 
                        x, y + TIC_SIZE)    
	    
	    # Draw the note/attachment icon above the tick
	    note_tags = [ tag for tag in meta.global_settings
	                  if (tag.startswith('Notes') or tag.startswith('Attachments')) and exp.get_tag_attribute(tag) == str(timepoint)] 
	    for i, note_tag in enumerate(note_tags):
		if exp.get_tag_type(note_tag) == 'Notes':
		    bmp = icons.note.Scale(ICON_SIZE, ICON_SIZE, quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() 
		if exp.get_tag_type(note_tag) == 'Attachments':
		    bmp = icons.clip.Scale(ICON_SIZE, ICON_SIZE, quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap() 
		dc.DrawBitmap(bmp, x - ICON_SIZE / 2.0, 
	                        y - ((i+1)*ICON_SIZE) - TIC_SIZE - 1)	
		
		if icon_hover(self.cursor_pos, (x - ICON_SIZE / 2.0, 
	                        y - ((i+1)*ICON_SIZE) - TIC_SIZE - 1), ICON_SIZE):
		    self.curr_note_tag = note_tag

            # draw the timepoint beneath the line
            time_string = exp.format_time_string(timepoint)
            wtext = FONT_SIZE[0] * len(time_string)
	    htext = FONT_SIZE[1]
            dc.DrawText(time_string, x - wtext/2.0, y + TIC_SIZE + 1)
	    dc.DrawLine(x, y + TIC_SIZE + 1 + htext,  x, h_win)  # extension of tick towards the lineage panel
	    		   
        dc.EndDrawing()

    def _on_mouse_motion(self, evt):
        self.cursor_pos = evt.X, evt.Y
        self.Refresh(eraseBackground=False)

    def _on_mouse_exit(self, evt):
        self.cursor_pos = None
        self.Refresh(eraseBackground=False)
        
    def _on_click(self, evt):
        if self.hover_timepoint is not None:
            try:
                bench = wx.GetApp().get_bench()
            except: return
            bench.set_timepoint(self.hover_timepoint)
            bench.update_well_selections()
	
	if self.curr_note_tag is not None:
	    note_type = exp.get_tag_event(self.curr_note_tag)	    
	    timepoint = exp.get_tag_attribute(self.curr_note_tag)
	    self.page_counter = exp.get_tag_instance(self.curr_note_tag)	
	    if exp.get_tag_type(self.curr_note_tag) == 'Notes':
		note_dia = NotePad(self, note_type, timepoint, self.page_counter)
		if note_dia.ShowModal() == wx.ID_OK:
		    # Notes|<type>|<timepoint>|<instance> = value
		    meta.set_field('Notes|%s|%s|%s' %(note_dia.noteType, timepoint, str(self.page_counter)), note_dia.noteDescrip.GetValue())  
	    elif exp.get_tag_type(self.curr_note_tag) == 'Attachments':
		attfileTAG = 'Attachments|Files|%s|%s' %(timepoint, str(self.page_counter))
		dia = FileListDialog(self, attfileTAG, meta.get_field(attfileTAG, []), None)
		if dia.ShowModal()== wx.ID_OK:
		    f_list = dia.file_list
		    if f_list:
			meta.set_field(attfileTAG, f_list) 	    
		

class LineagePanel(wx.Panel):
    '''A Panel that displays a lineage tree.
    '''
    # Drawing parameters
    PAD = 30
    NODE_R = 8
    SM_NODE_R = 3
    ICON_SIZE = 16.0
    #MIN_X_GAP = NODE_R*2 + 2
    #MIN_Y_GAP = NODE_R*2 + 2
    MIN_X_GAP = ICON_SIZE + 2
    MIN_Y_GAP = ICON_SIZE + 2    
    FLASK_GAP = MIN_X_GAP
    #X_SPACING = 'EVEN'

    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.SetBackgroundColour('#FAF9F7')

        self.nodes_by_timepoint = {}
        self.time_x = False
        self.cursor_pos = None
        self.current_node = None
	self.timepoint_cursor = None
        
        meta.add_subscriber(self.on_timeline_updated, 
                            exp.get_matchstring_for_subtag(2, 'Well'))

        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_MOTION, self._on_mouse_motion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._on_mouse_exit)
        self.Bind(wx.EVT_LEFT_UP, self._on_mouse_click)
        
    def set_timepoint(self, timepoint):
	self.timepoint_cursor = timepoint
	self.Refresh(eraseBackground=False)
	
    def set_x_spacing(self, mode):
        if mode == SPACE_TIME:
            self.time_x = True
        elif mode == SPACE_EVEN:
            self.time_x = False
        self._recalculate_min_size()
        self.Refresh(eraseBackground=False)
        
    def set_style(self, padding=None, xgap=None, ygap=None, node_radius=None,
                  flask_gap=None, icon_size=None):
        if padding is not None:
            self.PAD = padding
        if xgap is not None:
            self.MIN_X_GAP = xgap
        if ygap is not None:
            self.MIN_Y_GAP = ygap
        if node_radius is not None:
            self.NODE_R = node_radius
        if flask_gap is not None:
            self.FLASK_GAP = flask_gap
	if icon_size is not None:
	    self.ICON_SIZE = icon_size	
        self._recalculate_min_size()
        self.Refresh(eraseBackground=False)
     
    def on_timeline_updated(self, tag):
        '''called to add events to the timeline and update the lineage
        '''
        timeline = meta.get_timeline()
        t0 = time()
        self.nodes_by_timepoint = timeline.get_nodes_by_timepoint()
      
        #print 'built tree in %s seconds'%(time() - t0)
        # get the unique timpoints from the timeline
        self.timepoints = meta.get_timeline().get_unique_timepoints()
        
        # For time-compact x-spacing
        #if len(self.timepoints) > 1:
            #self.min_time_gap = min([y-x for x,y in zip(self.timepoints[:-1], 
                                                        #self.timepoints[1:])])
        #else:
            #self.min_time_gap = 1
        self.timepoints.reverse()
        self.timepoints.append(-1)

        self._recalculate_min_size()
        self.Refresh(eraseBackground=False)
        
    def _recalculate_min_size(self):
        timepoints = meta.get_timeline().get_unique_timepoints()
        if len(timepoints) > 0:
            n_leaves = len(self.nodes_by_timepoint.get(timepoints[-1], []))
            if self.time_x:
                self.SetMinSize((self.PAD * 2 + self.MIN_X_GAP * timepoints[-1] + self.FLASK_GAP,
                                 n_leaves * self.MIN_Y_GAP + self.PAD * 2))
            else:
                self.SetMinSize((len(self.nodes_by_timepoint) * self.MIN_X_GAP + self.PAD * 2,
                                 n_leaves * self.MIN_Y_GAP + self.PAD * 2))


    def _on_paint(self, evt=None):
        '''Handler for paint events.
        '''
        if self.nodes_by_timepoint == {}:
            evt.Skip()
            return	

        t0 = time()
        #PAD = self.PAD + self.NODE_R
	PAD = self.PAD + self.ICON_SIZE
        NODE_R = self.NODE_R
	SM_NODE_R = self.SM_NODE_R 
        MIN_X_GAP = self.MIN_X_GAP
        MIN_Y_GAP = self.MIN_Y_GAP
        FLASK_GAP = self.FLASK_GAP
        MAX_TIMEPOINT = self.timepoints[0]
        timepoints = self.timepoints
        nodes_by_tp = self.nodes_by_timepoint
        self.current_node = None           # Node with the mouse over it
        w_win, h_win = (float(self.Size[0]), float(self.Size[1]))
	
        if self.time_x:
            if timepoints[0] == 0:
                px_per_time = 1
            else:
                px_per_time = max((w_win - PAD * 2 - FLASK_GAP) / MAX_TIMEPOINT,
                                  MIN_X_GAP)
	else:
	    px_per_time = 1
                
        if len(nodes_by_tp) == 2:
            x_gap = 1
        else:
            # calculate the number of pixels to separate each generation timepoint
            x_gap = max(MIN_X_GAP, 
                         (w_win - PAD * 2 - FLASK_GAP) / (len(nodes_by_tp) - 2))
            
        if len(nodes_by_tp[timepoints[0]]) == 1:
            y_gap = MIN_Y_GAP
        else:
            # calcuate the minimum number of pixels to separate nodes on the y axis
            y_gap = max(MIN_Y_GAP, 
                        (h_win - PAD * 2) / (len(nodes_by_tp[MAX_TIMEPOINT]) - 1))
                        
        nodeY = {}  # Store y coords of children so we can calculate where to draw the parents
        Y = PAD
        X = w_win - PAD
        
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.BeginDrawing()
        #dc.SetPen(wx.Pen("BLACK",1))
        
        def hover(mouse_pos, node_pos, node_r):
            '''returns whether the mouse is hovering over a node
            mouse_pos - the mouse position
            node_pos - the node position
            node_r - the node radius
            '''
            if mouse_pos is None:
                return False
            MX,MY = mouse_pos
            X,Y = node_pos
            return (X - node_r < MX < X + node_r and 
                    Y - node_r < MY < Y + node_r)	
	

        # Iterate from leaf nodes up to the root, and draw R->L, Top->Bottom
        for i, t in enumerate(timepoints):
            if t == -1:  # for the root node which is not shown
                X = PAD
            elif self.time_x:
                X = PAD + FLASK_GAP + t * px_per_time
                x_gap = PAD + FLASK_GAP + timepoints[i-1] * px_per_time - X
            else:
                X = PAD + FLASK_GAP + (len(timepoints) - i - 2) * x_gap
		
	    # Draw longitudinal time lines
	    if t != -1:
		dc.SetPen(wx.Pen('#E1E2ED', 1, wx.DOT))
		dc.DrawLine(X, 0, X, h_win)	    
            
            # LEAF NODES
            if i == 0:
                for node in sorted(nodes_by_tp[t], key=self.order_nodes):
		    ancestor_tags = self.get_ancestral_tags(node)	
		    node_tags = node.get_tags()
		    stateRGB = meta.getStateRGB([tags for tags in reversed(ancestor_tags)]+node_tags)# reverse the ancestal line so that it become progeny + curr node			    
		    if node_tags:
			eventRGB = meta.getEventRGB(node_tags[0]) #get all event tags for the passed node and returns the colour associated with the last event** Need to change
		    else:
			eventRGB = (255, 255, 255, 100)
		   
                    empty_path = False # whether this path follows a harvesting
		    event_status = False # whether any event occured to this node		    
		    
                    if len(node.get_tags()) > 0:
                        # Event occurred
			dc.SetBrush(wx.Brush(eventRGB))
			dc.SetPen(wx.Pen(stateRGB, 3))
			event_status = True
			
                    else:
                        # No event
			if eventRGB == (255,255,255,100) and stateRGB == (255,255,255,100):
			    dc.SetBrush(wx.Brush(wx.WHITE))
			    dc.SetPen(wx.Pen(wx.WHITE))	
                        if 'Transfer|Harvest' in self.get_ancestral_tags(node):
                            empty_path = True

                    if hover(self.cursor_pos, (X,Y), self.NODE_R):
                        # MouseOver
			if event_status:
			    dc.SetPen(wx.Pen(stateRGB, 1))
			    self.current_node = node
                    else:
                        # No MouseOver
			if event_status:
			    dc.SetPen(wx.Pen(stateRGB, 3))
                    
                    if not empty_path and event_status:
			#dc.DrawCircle(X, Y, NODE_R)
			#evt_categories = list(set([exp.get_tag_stump(tag, 1) for tag in node.get_tags()]))
			#if all(evt_categories[0] == cat and cat == 'DataAcquis' for cat in evt_categories):
			if (node_tags[0].startswith('Transfer|Seed') and 
		           meta.get_field('Transfer|Seed|CellLineInstance|'+exp.get_tag_instance(node_tags[0])) is not None):
			    event = 'CellLine'
			else:
			    event = exp.get_tag_event(node_tags[0])
			#dc.DrawBitmap(meta.getEventIcon(16.0, event), X - 16.0 / 2.0, Y - 16.0 / 2.0)
			dc.DrawBitmap(meta.getEventIcon(self.ICON_SIZE, event), X - self.ICON_SIZE / 2.0, Y - self.ICON_SIZE / 2.0)
##                      dc.DrawText(str(node.get_tags()), X, Y+NODE_R)
                    nodeY[node.id] = Y
                    Y += y_gap
                    
            # INTERNAL NODES
            else:
                for node in sorted(nodes_by_tp[t], key=self.order_nodes):
		    ancestor_tags = self.get_ancestral_tags(node)
		    children_tags = self.get_children_tags(node, 2)
		    node_tags = node.get_tags()
		    stateRGB = meta.getStateRGB([tags for tags in reversed(ancestor_tags)]+node_tags)# reverse the ancestal line so that it become progeny + curr node			    
		    if node_tags:
			eventRGB = meta.getEventRGB(node_tags[0]) #get all event tags for the passed node and returns the colour associated with the last event** Need to change
		    else:
			eventRGB = (255, 255, 255, 100)
		
                    empty_path = False # whether this path follows a harvesting
		    event_status = False # whether this node has event
		    children_status = False # whether the children nodes have any events associated
		    
		    if children_tags:
			children_status = True
		    
                    ys = []
                    for child in node.get_children():
                        ys.append(nodeY[child.id])
                    Y = (min(ys) + max(ys)) / 2
		    
                    if len(node.get_tags()) > 0:
			#Event occurred
                        dc.SetBrush(wx.Brush(eventRGB))
			dc.SetPen(wx.Pen(stateRGB, 3))
			event_status = True			
                    else:
			#No event
			if eventRGB == (255,255,255,100) and stateRGB == (255,255,255,100):
			    dc.SetBrush(wx.Brush(wx.WHITE))
			    dc.SetPen(wx.Pen(wx.WHITE))
			else:
			    if children_status:
				#dc.SetBrush(wx.Brush(wx.BLACK))
				#dc.SetPen(wx.Pen(wx.BLACK))
				dc.SetBrush(wx.Brush('#D1CDCF'))
				dc.SetPen(wx.Pen('#D1CDCF'))
			    else:
				dc.SetBrush(wx.Brush(wx.WHITE))
				dc.SetPen(wx.Pen(wx.WHITE))			    
			    
			if 'Transfer|Harvest' in self.get_ancestral_tags(node):
			    empty_path = True
		
                    if hover(self.cursor_pos, (X,Y), self.NODE_R):
                        # MouseOver
			if event_status:
			    dc.SetPen(wx.Pen(stateRGB, 1))
			    self.current_node = node                        
			    self.SetToolTipString(self.ShowTooltipsInfo())
			    #print self.current_node.get_tags()
			    #print self.current_node.get_well_ids()
			   			    
                    else:
                        # No MouseOver
			if event_status:
			    dc.SetPen(wx.Pen(stateRGB, 3))
                    
                    #if t == -1:
                        #dc.DrawRectangle(X-NODE_R, Y-NODE_R, NODE_R*2, NODE_R*2)
                    #else:
		    if not empty_path:
			if event_status:
			    if (node_tags[0].startswith('Transfer|Seed') and 
				        meta.get_field('Transfer|Seed|CellLineInstance|'+exp.get_tag_instance(node_tags[0])) is not None):
				event = 'CellLine'
			    else:
				event = exp.get_tag_event(node_tags[0])
			    dc.DrawBitmap(meta.getEventIcon(self.ICON_SIZE, event), X - self.ICON_SIZE / 2.0, Y - self.ICON_SIZE / 2.0)
				
			else:
			    #dc.DrawCircle(X-NODE_R,Y, SM_NODE_R) # draws the node slightly left hand side on the furcation point
			    #dc.SetBrush(wx.Brush(stateRGB))
			    dc.DrawCircle(X,Y, SM_NODE_R)
			#dc.DrawText(str(node.get_tags()), X, Y+NODE_R)
                        
                    # DRAW LINES CONNECTING THIS NODE TO ITS CHILDREN
                    dc.SetBrush(wx.Brush('#FAF9F7'))
                    dc.SetPen(wx.Pen(wx.BLACK, 1))
		    #dc.SetPen(wx.Pen('#D1CDCF'))
		    #dc.SetPen(wx.Pen(stateRGB))
                    harvest_tag = False
                    for tag in node.get_tags():
                        if tag.startswith('Transfer|Harvest'):
                            harvest_tag = tag
		    # for children of this node check whether furhter event had occured to them if not do not draw the line 
                    for child in node.get_children():
			if harvest_tag:
			    # TODO: improve performance by caching reseed 
			    #       events from the previous timepoint
			    for nn in nodes_by_tp[timepoints[i-1]]:
				for tag in nn.get_tags():
				    if (tag.startswith('Transfer|Seed') and 
				        meta.get_field('Transfer|Seed|HarvestInstance|'+exp.get_tag_instance(tag)) == exp.get_tag_instance(harvest_tag)):
					#dc.SetPen(wx.Pen('#948BB3', 1, wx.SHORT_DASH))
					dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SHORT_DASH))
					dc.DrawLine(X + NODE_R, Y, 
				                    X + x_gap - NODE_R ,nodeY[nn.id])
			else:
			    if not empty_path:
				if event_status:
				    if children_status:
					dc.DrawLine(X + NODE_R, Y, 
					            X + x_gap - NODE_R, nodeY[child.id])	
				else:
				    if children_status and stateRGB != (255,255,255,100):
					    #dc.SetPen(wx.Pen('#D1CDCF'))
					    dc.SetPen(wx.Pen(wx.BLACK))
					    #dc.SetPen(wx.Pen(stateRGB))
					    dc.DrawLine(X, Y,
						        X + x_gap, nodeY[child.id])
			
                    nodeY[node.id] = Y
		    
	# Draw time slider insync with the slider in the Bench	    
	if self.timepoint_cursor is not None:  
	    timepoints = meta.get_timeline().get_unique_timepoints()	
	    if timepoints and len(timepoints)>1:
		px_per_ti = (w_win - PAD * 2 - FLASK_GAP) /(len(timepoints)-1)
		if self.timepoint_cursor <= max(timepoints) and self.timepoint_cursor >= min(timepoints):   
		    ti = bisect.bisect_left(timepoints, self.timepoint_cursor)
		    time_interval =  timepoints[ti]-timepoints[ti-1]	
		    adjusted_factor = px_per_ti/time_interval		    
		    X = PAD + FLASK_GAP + px_per_ti*(ti-1) + (self.timepoint_cursor - timepoints[ti-1])* adjusted_factor

		elif self.timepoint_cursor > max(timepoints): # after adding new 24hr to the timeline and start to hover	
		    X = PAD + FLASK_GAP + px_per_ti*(len(timepoints)-1)		    
				       
		penclr   = wx.Colour(178, 34, 34, wx.ALPHA_TRANSPARENT)
		dc.SetPen(wx.Pen('Blue',3))
		dc.DrawLine(X, 0, X, h_win)		    
      
        dc.EndDrawing()
        
    def _on_mouse_motion(self, evt):
        self.cursor_pos = (evt.X, evt.Y)
        self.Refresh(eraseBackground=False)

    def _on_mouse_exit(self, evt):
        self.cursor_pos = None
        self.Refresh(eraseBackground=False)


    def _on_mouse_click(self, evt):
        if self.current_node is None:
            return
	# first check whehter the tag is Harvest if so call the method.
	#self.remove_harvest_seed_track(self.current_node.tags[0])
	    
	    #meta.remove_field(ctags)
        # --- Update the Bench view ---
        try:
            bench = wx.GetApp().get_bench()
        except: 
            return
	
	bench.selected_harvest_inst = self.current_node.tags[0]
        bench.set_timepoint(self.current_node.get_timepoint())
        bench.taglistctrl.set_selected_protocols(
            [exp.get_tag_protocol(tag) for tag in self.current_node.get_tags()])
        bench.group_checklist.SetCheckedStrings(
            [exp.PlateDesign.get_plate_group(well[0]) 
             for well in self.current_node.get_well_ids()])
        bench.update_plate_groups()
        bench.update_well_selections()
	bench.del_evt_button.Enable()
	
        # -- Update the expt setting/metadata view --#
        try:
            exptsettings = wx.GetApp().get_exptsettings()
        except:
            return
	
        exptsettings.OnLeafSelect()
        if self.current_node.get_tags():
	    tag = self.current_node.get_tags()[0] # TO DO: if multiple event tag are there need to itterate through the list
	    if meta.get_field('Transfer|Seed|HarvestInstance|'+exp.get_tag_instance(tag)) is None or exp.get_tag_event(tag) is 'Harvest':
		exptsettings.ShowInstance(tag)
            
	# -- show the data url list --- #
        data_acquis = False

	for tag in self.current_node.get_tags():
	    if tag.startswith('DataAcquis'):
		data_acquis = True
		break
	    
	if data_acquis: 
	    dia = DataLinkListDialog(self, self.current_node.get_well_ids(), self.current_node.get_timepoint(), self.find_ancestral_tags(self.current_node))
	    if dia.ShowModal() == wx.ID_OK:
		if dia.output_options.GetSelection() == 0:
		    file_dlg = wx.FileDialog(None, message='Exporting Data URL...', 
		                             defaultDir=os.getcwd(), defaultFile='data urls', 
		                             wildcard='.csv', 
		                             style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
		    if file_dlg.ShowModal() == wx.ID_OK:
			os.chdir(os.path.split(file_dlg.GetPath())[0])
			try:
			    myfile = open(file_dlg.GetPath(), 'wb')
			    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			    for row in dia.get_selected_urls():
				wr.writerow(row)
			    myfile.close()	
			    file_dlg.Destroy()
			except:
			    err_dlg = wx.MessageDialog(None, 'Cant open file for writing', 'Error', wx.OK | wx.ICON_ERROR)
			    err_dlg.ShowModal()			    
			    
		if dia.output_options.GetSelection() == 1:
		    file_dlg = wx.FileDialog(None, message='Exporting Data URL...', 
		                            defaultDir=os.getcwd(), defaultFile='data urls', 
		                            wildcard='.csv', 
		                            style=wx.SAVE|wx.FD_OVERWRITE_PROMPT)
		    if file_dlg.ShowModal() == wx.ID_OK:
			os.chdir(os.path.split(file_dlg.GetPath())[0])
			myfile = open(file_dlg.GetPath(), 'wb')
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			for row in dia.get_all_urls():
			    wr.writerow(filter(None, row))
			myfile.close()	
			file_dlg.Destroy()
		
		if dia.output_options.GetSelection() == 2:
		    image_urls = []
		    for row in dia.get_selected_urls():
			image_urls.append(row[3])
				
				
		    if os.path.isfile('C:\Program Files\ImageJ\ImageJ.exe') is False:
			for r,d,f in os.walk("c:\\"):
			    if r.endswith('ImageJ'):
				for files in f:
				    if files == "ImageJ.exe":
					ImageJPath = os.path.join(r,files)	
			if not ImageJPath:
			    err_dlg = wx.MessageDialog(None, 'ImageJ was not found in C\Program Files directory to show images!!', 'Error', wx.OK | wx.ICON_ERROR)
			    err_dlg.ShowModal()			 
			    return 			
		    else:
			#TO DO: check the image format and image path are compatible with mageJ    
			ImageJPath = 'C:\Program Files\ImageJ\ImageJ.exe'
			
		    subprocess.Popen('%s %s' % (ImageJPath, ' '.join('"' + item + '"' for item in image_urls)))
	    dia.Destroy()	
	    
      
    def ShowTooltipsInfo(self):
        what = ''
	where = ''
        for tag in self.current_node.get_tags():
	    what = exp.get_tag_event(exp.get_tag_protocol(tag))+' instance %s was used on'%exp.get_tag_attribute(exp.get_tag_protocol(tag))
	for pw in self.current_node.get_well_ids():
	    where += str(pw) 
        return what+'\n'+where  

    
    def get_description(self, protocol):
        return '\n'.join(['%s=%s'%(k, v) for k, v in meta.get_attribute_dict(exp.get_tag_protocol(protocol))])  
    
    #----------------------------------------------------------------------
    def get_children_tags(self, node, stump_no):
	"""returns the children node tags"""    
	return [exp.get_tag_stump(ctag, stump_no)
	        for cnodes in timeline.get_progeny(node) if cnodes
	        for ctag in cnodes.tags]	
    
    def remove_harvest_seed_track(self, h_tag):
	'''Completely removes all events associated with a harvest_seed (sample transfer) track including the harvest seed coupled event'''
	h_instance = exp.get_tag_instance(h_tag)
	harvest_tp = exp.get_tag_timepoint(h_tag)
	tag_list = [h_tag]
	
	for s_instance in meta.get_field_instances('Transfer|Seed|HarvestInstance'):
	    if meta.get_field('Transfer|Seed|HarvestInstance|%s'%s_instance) == h_instance:
		s_tag = 'Transfer|Seed|Wells|%s|%s'%(s_instance, str(harvest_tp+1)) # coupled seed is always 1 min after from harvest
		for tpnode in self.nodes_by_timepoint[harvest_tp+1]:
		    if tpnode:
			if s_tag in tpnode.tags:
			    for c_tag in self.get_children_tags(tpnode, 5):
				if c_tag.startswith('Transfer|Harvest'): # in case further harvest-seed is there then make it recursive
				    self.remove_harvest_seed_track(c_tag)
				else:
				    for s_well in meta.get_field(s_tag):
					c_wells = meta.get_field(c_tag)
					if s_well in c_wells:
					    c_wells.remove(s_well)
					    meta.remove_associated_dataacquis_tag([s_well]) 
					    if c_wells:  # if at least one other affected well
						meta.set_field(c_tag, c_wells)
					    else:
						meta.remove_field(c_tag) # tag with single well
						meta.remove_timeline_attachments(exp.get_tag_timepoint(c_tag))
			    meta.remove_field(h_tag)
			    meta.remove_field(s_tag)		    
			    meta.remove_harvest_seed_tags(h_instance, s_instance)	
	
   
    def find_ancestral_tags(self, node):
	ancestral_tags = []
	for pnode in timeline.reverse_iter_tree(node):
	    if pnode: 
		for ptag in pnode.tags:
		    if ptag.startswith('Transfer|Seed')and meta.get_field('Transfer|Seed|HarvestInstance|'+exp.get_tag_instance(ptag)) is not None:
			for tpnode in self.nodes_by_timepoint[pnode.get_timepoint()-1]:
			    if tpnode:
				for tptag in tpnode.tags:
				    if exp.get_tag_protocol(tptag) == 'Transfer|Harvest|%s'%meta.get_field('Transfer|Seed|HarvestInstance|'+exp.get_tag_instance(ptag)):
					for npnode in timeline.reverse_iter_tree(tpnode):
					    if npnode:
						for nptag in npnode.tags:
						    ancestral_tags.append(nptag)	
		    else:
			ancestral_tags.append(ptag)
			
	return list(reversed(ancestral_tags))
		

	
    def get_ancestral_tags(self, node):
	return [exp.get_tag_stump(ptag, 2)
	        for pnode in timeline.reverse_iter_tree(node) if pnode
	        for ptag in pnode.tags]
    
    #----------------------------------------------------------------------
    #def order_nodes(self, node):
	#"""Sort the node according to the Plate_Well ids"""
	#x = node.get_well_ids()
	#return tuple(sorted([("PTFCD".find(item[0][0]), item[0], item[1]) for item in x]))
    def order_nodes(self, node):
	"""Sort the node according to the Plate_Well ids"""
	x = node.get_well_ids()
	container_index = ["PTFCD".find(item[0][0]) for item in x]   #P for Plate, T for Tube etc update according to vessel prefix
	container_number = [int(re.search("([0-9]+)$", item[0]).group(1)) for item in x]
	container = [item[0] for item in x]
	well = [item[1] for item in x]
	return [(item[3], item[2]) for item in sorted(zip(container_index, container_number, well, container))]
    

        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    
    f = LineageFrame(None)
    f.Show()
    app.MainLoop()