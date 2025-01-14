import pandas as pd
import matplotlib.pyplot as plt
import wx
import wx.grid
import matplotlib
import numpy as np
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'

data = pd.read_csv('penalty_data_set_2.csv', index_col=False, low_memory=False)
data['OFFENCE_MONTH'] = pd.to_datetime(data['OFFENCE_MONTH'], format='%d/%m/%Y')

def camera_radar_penalty(data):
    return data[data.OFFENCE_DESC.str.contains('Camera|Radar', na=False)][['OFFENCE_MONTH', 'OFFENCE_CODE', 'OFFENCE_DESC', 'FACE_VALUE', 'TOTAL_NUMBER']][0:100]

def code_count(data):
    return data['OFFENCE_CODE'].value_counts().sort_values(ascending=0)[:10].plot.bar(figsize=(10, 10)), plt.xlabel('Offence Code'), plt.ylabel('Count')

def date_penalty(data):
    return data.loc[(data['OFFENCE_MONTH'] >= '2016-01-01') & (data['OFFENCE_MONTH'] < '2016-12-21')][0:100]

def mobile_count(data):
    return data.groupby('OFFENCE_CODE')['MOBILE_PHONE_IND'].value_counts().sort_values(ascending=0)[:10].plot.bar(figsize=(10, 10)), plt.xlabel('Offence Code'), plt.ylabel('Count')

def offence_value(data):
    return data.groupby('OFFENCE_CODE')['TOTAL_VALUE'].sum().sort_values(ascending=0)[:10].plot.bar(figsize=(10, 10)), plt.xlabel('Offence Code'), plt.ylabel('value')


# declare DataTable to hold the wx.grid data to be displayed
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


class MyFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY)
        self._init_gui()
        self.Layout()
        self.Show()
        self.Centre()
        self.frame_number = 1

    def _init_gui(self):
        # assign the DataFrame to df
        df = pd.DataFrame(data[0:200])
        table = DataTable(df)

        # grid and assigned data
        grid = wx.grid.Grid(self, -1, size=(1000, 600))
        grid.SetTable(table, takeOwnership=True)
        grid.AutoSizeColumns()

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(grid, 0, wx.EXPAND)

        # buttons
        penaltiesButton = wx.Button(self, label='2016 Penalties')
        penaltiesButton.Bind(wx.EVT_BUTTON, self.penaltiesButton)

        plot1Button = wx.Button(self, label='Offence Code Distribution Chart')
        plot1Button.Bind(wx.EVT_BUTTON, self.plot1Button)

        cameraButton = wx.Button(self, label='Camera/Radar')
        cameraButton.Bind(wx.EVT_BUTTON, self.cameraButton)

        plot2Button = wx.Button(self, label='Mobile Offences Chart')
        plot2Button.Bind(wx.EVT_BUTTON, self.plot2Button)

        plot3Button = wx.Button(self, label='Offence Code Value Chart')
        plot3Button.Bind(wx.EVT_BUTTON, self.plot3Button)

        cancelButton = wx.Button(self, wx.ID_CANCEL, label="Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancel)

        sizerbtns = wx.BoxSizer(wx.HORIZONTAL)
        sizerbtns.Add(penaltiesButton, 0, wx.CENTER)
        sizerbtns.Add(plot1Button, 0, wx.CENTER)
        sizerbtns.Add(cameraButton, 0, wx.CENTER)
        sizerbtns.Add(plot2Button, 0, wx.CENTER)
        sizerbtns.Add(plot3Button, 0, wx.CENTER)
        sizerbtns.Add(cancelButton, 0, wx.CENTER)

        mainSizer.Add(sizer, 0, wx.ALL, 5)
        mainSizer.Add(sizerbtns, 0, wx.CENTER)

        sizer.SetSizeHints(self)
        self.SetSizerAndFit(mainSizer)

        self.Bind(wx.EVT_CLOSE, self.exit)

    def exit(self, event):
        self.Destroy()

    def OnCancel(self, event):
        self.Destroy()

    def penaltiesButton(self, event):

        df = pd.DataFrame(date_penalty(data))
        table = DataTable(df)

        # Destroy and create grid with new data assigned
        grid = wx.grid.Grid(self, -1, size=(1000, 600))
        grid.SetTable(table, takeOwnership=True)
        grid.AutoSizeColumns()

    def cameraButton(self, event):

        # Create new data
        df = pd.DataFrame(camera_radar_penalty(data))
        table = DataTable(df)

        # Destroy and create grid with new data assigned
        grid = wx.grid.Grid(self, -1, size=(1000, 600))
        grid.SetTable(table, takeOwnership=True)
        grid.AutoSizeColumns()


    def plot1Button(self, event):
        code_count(data)
        self.Centre()
        plt.show()

    def plot2Button(self, event):
        mobile_count(data)
        plt.show()

    def plot3Button(self, event):
        offence_value(data)
        plt.show()


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
