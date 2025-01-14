import wx
import wx.adv
import matplotlib as mpl
import numpy as np
import pandas as pd
import wx.grid

EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'

data = pd.read_csv('penalty_data_set_2.csv', index_col=False, low_memory=False)

class Main(wx.Frame):
    # Frame is top level window - contains both panels
	def __init__(self):
		wx.Frame.__init__(self, parent = None, title = "My Frame", size = (1500,900))
		

		splitter = wx.SplitterWindow(self)
		left = LeftPanel(splitter)
		right = RightPanel(splitter, left)
		splitter.SplitVertically(left, right)
		splitter.SetMinimumPaneSize(400)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.Centre()
  
class LeftPanel(wx.Panel):
    # This contains all the buttons, key words search and dates selection
	def __init__(self, parent):
		wx.Panel.__init__(self, parent = parent)
		self.SetBackgroundColour("gray") # Test Colours to see both panels clearly
		welcomeText = wx.StaticText(self, label="Helloo world!!", pos = (150, 10))

	# Exit Button
	
		Quitbutton = wx.Button(parent=self, label='Exit', pos = (150, 800))
		Quitbutton.Bind(wx.EVT_BUTTON, self.Quit) # bind action to button
  
 	# Visualise Button
	
		Visualbutton = wx.Button(parent=self, label='Visualise', pos = (150, 700))
		Visualbutton.Bind(wx.EVT_BUTTON, self.Visualise) # bind action to button
  
	# Calendar with dates 
 
		self.cal = wx.adv.CalendarCtrl(self, 10, wx.DateTime.Now())
		self.cal.Bind(wx.adv.EVT_CALENDAR, self.OnDate)
  
	# Filter or Choice box - NEED TO BING TO FILTER BUTTON
		
		FilterButton = wx.Button(parent=self, label='Select FIlter', pos = (150, 600))
		FilterButton.Bind(wx.EVT_BUTTON, self.Filter)
 
  
	#sizers !!!help
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.cal, 0, wx.ALL | wx.CENTER, 30)
		sizer.Add(Quitbutton, 0, wx.ALL| wx.CENTER, 100)
		self.SetSizer(sizer)

	def OnDate(self, e):
		sel_date = self.cal.GetDate()
		print(sel_date.Format("%d-%m-%Y"))
		
	def Quit(self, e):
		wx.Exit()
	
	def Visualise(self,e):
		pass # Does nothing atm

	def Filter(self, e):
		choiceBox = wx.SingleChoiceDialog(None, 'Please select a Filter', 
                                    	'Select Available Filter',
                                     	['OFFENCE MONTH', 'OFFENCE YEAR', 'OFFENCE CODE'])
		if choiceBox.ShowModal()==wx.ID_OK:
			filter = choiceBox.GetStringSelection()
		


class RightPanel(wx.Panel):
    # This is where all the data will be displayed 
	def __init__(self, parent, top):
		wx.Panel.__init__(self, parent = parent)
		self.SetBackgroundColour("white")
		self._init_gui()
		self.Layout()
		self.Show()

  
	def _init_gui(self):
     # assign the DataFrame to df
		df = pd.DataFrame(data[0:200])
		table = DataTable(df)
  
	# declare the grid and assign data
		grid = wx.grid.Grid(self, -1, size=(1075, 850)) # Need to fit panel
		grid.SetTable(table, takeOwnership=True)
		grid.AutoSizeColumns()

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(grid, 1, wx.EXPAND|wx.ALL)
  
	
		
		
class DataTable(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        if data is None:
            data = pd.DataFrame()
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data.columns) + 1

    def GetValue(self, row, col):
        if col == 0:
            return self.data.index[row]
        return self.data.iloc[row, col - 1]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col - 1] = value

    def GetColLabelValue(self, col):
        if col == 0:
            if self.data.index.name is None:
                return 'Index'
            else:
                return self.data.index.name
        return str(self.data.columns[col - 1])

    def GetTypeName(self, row, col):
        return wx.grid.GRID_VALUE_STRING

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr


if __name__ == "__main__":
	app = wx.App()
	frame = Main()
	frame.Show()
	app.MainLoop()