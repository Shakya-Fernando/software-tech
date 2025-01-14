import wx


class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        
        #init Frame
        self.InitFrame()
    
    def InitFrame(self):
        frame = MyFrame(parent=None, title="This is a frame", pos = (100, 100))
        frame.Show()


class MyFrame(wx.Frame):
    # subclass of wx.MyApp; Frame is a top level window
    # A frame is a window whose size and position can (usually) be changed by the user.
    # Usually represents the first/main window a user will see
    def __init__(self, parent, title, pos):
        super().__init__(parent=parent, title=title, pos=pos, size=(1300, 900))
        self.OnInit()
        
    def OnInit(self):
        # Panel is within the Frame
        panel = MyPanel(parent=self)
        self.Centre()


class MyPanel(wx.Panel):
    # A panel is a window on which controls are placed. (e.g. buttons and text boxes)
    # wx.Panel class is usually put inside a wxFrame object. This class is also inherited from wxWindow class.
    def __init__(self,parent):
        super().__init__(parent=parent)
        
        
        #Randon welcome text
        welcomeText = wx.StaticText(self, label="Helloo world!!", pos=(20,20))

        Quitbutton = wx.Button(parent=self, label='Exit', pos = (20, 120))
        Quitbutton.Bind(wx.EVT_BUTTON, self.Quit) # bind action to button
        
     
    def Quit(self, e):
        # stuff for the button to do
        wx.Exit()   





if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()