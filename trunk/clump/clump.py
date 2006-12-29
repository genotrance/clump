import wx, sys, os, threading, time, re

# Constants
ID_SAVE  = 101
ID_CLEAR = 102
ID_EXIT  = 103

# Frame class
class MyFrame(wx.Frame):
    # Initialization
    def __init__(self, parent, id, title):
        # Members
        self.save_prevfile = ""
        self.save_prevdir = ""
        self.fileno = 0

        # See if command line filename specified
        if (len(sys.argv) == 2): self.filename = sys.argv[1]
        else: self.filename = 0

        # Create frame object
        wx.Frame.__init__(self, parent, id, title)

		# Set the icon
        iconfile = re.sub('.exe|.py', '.ico', sys.argv[0])
        if os.path.isfile(iconfile): self.SetIcon(wx.Icon(iconfile, wx.BITMAP_TYPE_ICO))

        # Create text box and set font
        self.textBox = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.textBox.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))

        # Create status bar
        self.statusBar = self.CreateStatusBar(1)

        # Start thread to read stdin or file
        self.Read()

        # Create menu
        file = wx.Menu();
        file.Append(ID_SAVE, "&Save", "Save buffer to file")
        file.Append(ID_CLEAR, "&Clear", "Clear buffer")
        file.AppendSeparator
        file.Append(ID_EXIT, "E&xit", "Exit application")

        # Create menu bar
        menu = wx.MenuBar()
        menu.Append(file, "&File")
        self.SetMenuBar(menu)

        # Bind menu events
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, ID_CLEAR, self.OnClear)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)

        # Bind close event
        wx.EVT_CLOSE(self, self.OnClose)

        # Resize GUI
        self.SetSize(wx.Size(1000, 700))

    # Start the reading thread
    def Read(self):
        # Return if open failed
        if (self.Open() != True): sys.exit(1)

        # Start the child thread to pipe the input
        self.child = threading.Thread(target=self.Pipe)
        self.child.setDaemon(True)
        self.child.start()

    # Open file if applicable
    def Open(self):
        # Read from stdin
        if (self.filename == 0): self.SetStatusText("Reading STDIN")
        else:
            # Read from file
            self.SetStatusText("Reading " + self.filename)

            # Catch unopenable file exception
            try: self.fileno = open(self.filename)
            except IOError:
                wx.MessageBox("Could not open file '" + self.filename + "'", "Error")
                self.SetStatusText("Done")
                return False

        return True

    # Pipe STDIN to the text box
    def Pipe(self):
        while (1):
            # Read from file/stdin
            try:
                if (self.fileno): line = self.fileno.read(1024)
                else: line = os.read(self.fileno, 1024)
            except (OSError, ValueError): return

            # Add line to textbox
            if (line != ''): self.textBox.AppendText(line)
            else:
                # Nothing left to print on stdin then break
                if (self.fileno == 0):
                    # Set status to done and close the file descriptor
                    sys.stdin.close()
                    break

            time.sleep(0.01)

        self.SetStatusText("Done")

    # Save buffer to file
    def OnSave(self, event):
        # Create a file dialog
        dialog = wx.FileDialog(self, "Select a file", self.save_prevfile,
            self.save_prevdir, "All files (*.*)|*.*", wx.SAVE|wx.OVERWRITE_PROMPT)

        # Display dialog and save buffer to file
        if (dialog.ShowModal() != wx.ID_CANCEL):
            file = dialog.GetPath()
            self.textBox.SaveFile(file)

        # Close dialog
        dialog.Destroy()

    # Clear the text box
    def OnClear(self, event):
        self.textBox.Clear()

    # Exit application
    def OnExit(self, event):
        self.Close(True)

    # Destroy the frame
    def OnClose(self, event):
        if (self.fileno): self.fileno.close()
        else: sys.stdin.close()
        time.sleep(0.01)
        self.Destroy()

# Application class
class MyApp(wx.App):
    # Initialization
    def OnInit(self):
        # Create a frame object
        frame = MyFrame(None, -1, "Clump")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

# Application startup code
if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
