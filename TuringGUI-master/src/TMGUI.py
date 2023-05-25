import customtkinter

try:  # python 3: default
    import tkinter as tk
    import customtkinter as ctk
    from tkinter import ttk, scrolledtext, filedialog
except ImportError:  # python 2
    import Tkinter as tk
    import customtkinter as ctk
    import ttk, ScrolledText as scrolledtext, tkFileDialog as filedialog

from turing_machines import *
import os

ctk.set_appearance_mode("dark")


WIDTH = 1280
HEIGHT = 690
DIMENSIONS = str(WIDTH) + "x" + str(HEIGHT) + "+10+10"
CWD = os.getcwd()


class TMGUI:
    """A GUI for simulating Turing Machines"""

    def __init__(self, master):
        self.tm = None
        self._jobs = []

        self.main = master
        self.main.title("Turing Machine Simulator")
        self.main.geometry(DIMENSIONS)

        ### RIGHT FRAME: EDITOR
        self.frameEditor = customtkinter.CTkFrame(self.main)
        self.labelEditor = customtkinter.CTkLabel(self.frameEditor, text="Editor")
        self.labelEditor.grid(row=0, column=1)
        self.textEditor = ctk.CTkTextbox(self.frameEditor, height=590, width=40, wrap=ctk.WORD)
        # self.textEditor = scrolledtext.ScrolledText(self.frameEditor, height=35, width=40, wrap=tk.WORD)
        self.textEditor.grid(row=1, column=0, columnspan=3, pady=7, padx=7, sticky='news')

        ###----------------------------Tkinter save button---------------------------------###

        # self.buttonSave = tk.Button(self.frameEditor, width=10, relief='groove', text="Save", command=self.saveTM)
        # self.buttonSave.grid(row=2, column=2, padx=20, pady=5)

        # ----------------------------------------------------------------------------------###

        self.buttonSave = ctk.CTkButton(self.frameEditor, width=10, text="             Save             ",
                                        command=self.saveTM)
        self.buttonSave.grid(row=2, column=2, padx=20, pady=5)

        ###----------------------------Tkinter load button---------------------------------###
        # self.buttonLoad = tk.Button(self.frameEditor, width=10, relief='groove', text="Load", command=self.loadTM)
        # self.buttonLoad.grid(row=2, column=0, padx=20, pady=5)
        # ----------------------------------------------------------------------------------###

        self.buttonLoad = ctk.CTkButton(self.frameEditor, width=10, text="             Load             ",
                                        command=self.loadTM)
        self.buttonLoad.grid(row=2, column=0, padx=20, pady=5)

        #self.frameEditor.grid(row=3, column=3, padx=15, pady=10, sticky='news')
        self.frameEditor.place(x=900, y=10)

        default_resize(self.frameEditor)

        ### LEFT FRAME: Simulator
        self.frameSim = customtkinter.CTkFrame(self.main, width=830)
        self.labelSim = customtkinter.CTkLabel(self.frameSim, text="Turing machine Simulator")
        #self.labelSim.grid(row=0, column=0, columnspan=3, pady=7, padx=7)
        self.labelSim.place(x=300, y=18)

        self.frameInput = customtkinter.CTkFrame(self.frameSim)
        customtkinter.CTkLabel(self.frameInput, text="Tape Input: ", pady=7, padx=7).pack(side='left')
        self.tape_input = tk.StringVar()
        self.tape_input.trace("w", self.setTape)
        self.textTapeInput = customtkinter.CTkEntry(self.frameInput, textvariable=self.tape_input, width=225)
        self.textTapeInput.pack(side='right', pady=10, padx=10)
        #self.frameInput.grid(row=1, column=0, columnspan=3, pady=7, padx=7)
        self.frameInput.place(x=20,y=50)

        combobox_var = customtkinter.StringVar(value="Choisir un algorithme")  # set initial value

        def combobox_callback(choice):
            print("combobox dropdown clicked:", choice)
            self.loadTMSelectList(choice)

        self.combobox = customtkinter.CTkComboBox(self.main,
                                             values=["Create reverse",
                                                     "Create spaces"
                                                     ],
                                             command=combobox_callback, width=400, height=40,
                                             variable=combobox_var)
        #self.combobox.pack(padx=20, pady=10)
        self.combobox.place(x=424,y=63)


        self.frameStep = customtkinter.CTkFrame(self.frameSim)
        self.buttonStep = ctk.CTkButton(self.frameStep, width=10, text="     Step     ", command=self.stepTM)
        self.buttonStep.grid(row=0, column=0, pady=7, padx=7)
        self.buttonStepBack = ctk.CTkButton(self.frameStep, width=10, text="Step Back", command=self.stepBackTM)
        self.buttonStepBack.grid(row=0, column=2, pady=5, padx=7)
        #self.frameStep.grid(row=2, column=2, pady=7, padx=7)
        self.frameStep.place(x=640, y=110)

        #self.tabsSim = ttk.Notebook(self.frameSim, width=800, height=430)
        #self.tabsSim = ctk.CTkTabview(self.frameSim)
        #self.frameTape = customtkinter.CTkFrame(self.tabsSim)
        #self.frameText = customtkinter.CTkFrame(self.tabsSim)
        #self.tabsSim.add(self.frameTape, text='  Tape  ')
        #self.tabsSim.add(self.frameText, text='  Text  ')
        #self.tabsSim.grid(row=3, column=0, columnspan=3, pady=7, padx=7)

        # Check boxes
        #####################################################################################################
        self.frameCheck = customtkinter.CTkFrame(self.frameSim)
        self.bidirectional = tk.BooleanVar()
        self.bi = self.bidirectional.get();

        def checkbox_event():
            print("checkbox toggled, current value:", self.bi)
        #self.bidirectional = ctk.Variable
        #self.checkbox2Way = tk.Checkbutton(
            #self.frameCheck, text="Bidirectional", var=self.bidirectional, command=checkbox_event, onvalue=True, offvalue=False)

        self.checkbox2Way = ctk.CTkCheckBox(self.frameCheck, command=checkbox_event,
                                     text="Bidirectional", onvalue=True, offvalue=False)
        self.checkbox2Way.select()
        self.checkbox2Way.grid(row=0, sticky='w', pady=7, padx=7)
        self.two_tape = tk.BooleanVar()
        #self.checkbox2Tape = ctk.CTkCheckBox(self.frameCheck, text="Two Tape", var=self.two_tape, onvalue=True, offvalue=False)

        #self.checkbox2Tape = ctk.CTkCheckBox(self.frameCheck, text="Two Tape", onvalue=True, offvalue=False)

        #self.checkbox2Tape.grid(row=1, sticky='w', pady=7, padx=7)
        #self.two_tape.trace("w", self.setTwoTape)
        #self.bidirectional.trace("w", self.setBidirectional)
        #self.frameCheck.grid(row=3, column=2)
        self.frameCheck.place(x=408,y=110)
        #####################################################################################################

        # Controls
        self.frameRun = customtkinter.CTkFrame(self.frameSim)
        #self.buttonRun = tk.Button(self.frameRun, width=10, relief='groove', text="Run", command=self.runTM)
        self.buttonRun = ctk.CTkButton(self.frameRun, width=100, text="                  Run                  ", command=self.runTM)
        self.buttonRun.grid(row=0, column=0, pady=7, padx=7)

        self.buttonStop = ctk.CTkButton(self.frameRun, width=100, text="                  Stop                  ", command=self.stopTM)
        self.buttonStop.grid(row=0, column=1, pady=7, padx=7)
        self.buttonReset = ctk.CTkButton(self.frameRun, width=100, text="                  Reset                  ", command=self.resetTM)
        self.buttonReset.grid(row=1, column=1, pady=7, padx=7)
        self.frameDelay = ctk.CTkFrame(self.frameRun)
        ctk.CTkLabel(self.frameDelay, text="Delay (s)").pack(side='left', padx=5)
        self.textDelay = ctk.CTkEntry(self.frameDelay, width=50)
        self.textDelay.insert(0, "0.1")
        self.textDelay.pack(side='right')
        self.frameDelay.grid(row=1, column=0, pady=7, padx=7)
        #self.frameRun.grid(row=2, column=0)
        self.frameRun.place(x=20, y=110)




        # Tape frame

        self.tapeframe = customtkinter.CTkFrame(self.frameSim, width=200)
        self.tapeframe.place(x=10, y=220)
        self.tabview = customtkinter.CTkTabview(self.tapeframe,width=828, height=420)
        self.tabview.pack(padx=10, pady=10)

        self.tabview.add("     Tape     ")  # add tab at the end
        self.tabview.add("     Text     ")  # add tab at the end
        self.tabview.set("     Tape     ")  # set currently visible tab

        #self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("     Text     "), width=600, height=300)
        #self.scrollable_frame.place(x=10,y=30)






        #tape li ldakhl     ####################################

        self.canvasSimOut = ctk.CTkCanvas(self.tabview.tab("     Tape     "), bg="#2b2b2b", width=10, height=10, highlightbackground="#2b2b2b")
        self.drawFirstTape()
        #self.canvasSimOut.create_rectangle(10, 0, 10, 0, fill='red')
        self.canvasSimOut.pack(expand=1, fill='both')
        #self.canvasSimOut.pack(expand=1, fill='both')

        # Text Frame
        #self.textSimOut = tk.scrolledtext(self.tabview.tab("     Text     "), height=10, width=55, wrap=tk.WORD )
        #self.textSimOut.pack(expand=1, fill='both')

        self.textSimOut = scrolledtext.ScrolledText(self.tabview.tab("     Text     "), state='disabled', height=10, width=55, wrap=tk.WORD)
        self.textSimOut.configure(bg='#2b2b2b', fg='white',highlightbackground='red')
        self.textSimOut.pack(expand=1, fill='both')

        self.frameSim.grid(row=0, column=0, rowspan=10, padx=15, pady=10, sticky="news")

        default_resize(self.frameSim)
        self.frameSim.grid_rowconfigure(0, weight=0)
        self.frameSim.grid_rowconfigure(1, weight=0)
        ### Seperate the two sides
        #ttk.Separator(master, orient='vertical').grid(column=1, row=0, rowspan=21, sticky='nsew', padx=5)

    # Editor Buttons

    def loadTMSelectList(self, choice):
        """Load a TM from a specification file into the editor and simulator"""
        if choice == 'Create reverse':
            tmFileName = '../Docs/Examples/reverse_oneway.tm'
            print('yoo')

        if choice == 'Create spaces':
            tmFileName = '../Docs/Examples/create_spaces.tm'



        tmFile = open(tmFileName, "r")
        self.textEditor.delete('1.0', 'end')
        self.textEditor.insert(0.0, tmFile.read())
        tmFile.close()
        self.tm = None
        if self.two_tape.get():
            self.tm = two_tape_TM(tmFileName, input=self.textTapeInput.get())
        else:
            self.tm = turing_machine(tmFileName, input=self.textTapeInput.get(), bidirectional=self.bidirectional.get())
        self.resetTM()



    def loadTM(self):
        """Load a TM from a specification file into the editor and simulator"""
        tmFileName = filedialog.askopenfilename(
            initialdir=CWD, title="Select TM File", filetypes=[("TM files", "*.tm"), ("all", "*.*")])
        if tmFileName == '':
            return
        tmFile = open(tmFileName, "r")
        self.textEditor.delete('1.0', 'end')
        self.textEditor.insert(0.0, tmFile.read())
        tmFile.close()
        self.tm = None
        if self.two_tape.get():
            self.tm = two_tape_TM(tmFileName, input=self.textTapeInput.get())
        else:
            self.tm = turing_machine(tmFileName, input=self.textTapeInput.get(), bidirectional=self.bidirectional.get())
        self.resetTM()

    def saveTM(self):
        """Save a TM to a specification file from the editor and load it into the simulator"""
        tmFileName = filedialog.asksaveasfilename(
            initialdir=CWD,
            title="Select save directory",
            filetypes=[("TM files", "*.tm"), ("all", "*.*")],
            defaultextension=[("TM files", "*.tm"), ("all", "*.*")])
        if tmFileName == '':
            return
        tmFile = open(tmFileName, "w")
        tmFile.write(self.textEditor.get(0.0, 'end'))
        tmFile.close()
        self.tm = None
        if self.two_tape.get():
            self.tm = two_tape_TM(tmFileName, input=self.textTapeInput.get())
        else:
            self.tm = turing_machine(tmFileName, input=self.textTapeInput.get(), bidirectional=self.bidirectional.get())
        self.resetTM()

    # Simulator Buttons
    def runTM(self):
        """Run the TM continuouslyself.
        Completely run a machine and enqueue all of the updates to be displayed (with optional delay)
        """
        if self.tm != None:
            self._jobs = []  # store the "after" IDS so we can cancel it
            try:
                delay = float(self.textDelay.get())
            except ValueError:
                delay = 0.1  # a reasonable default value
                self.textDelay.delete(0, "end")
                self.textDelay.insert(0, "0.1")
            if delay == 0:  # don't bother with the waiting at all then
                for config in self.tm.run_tm_iter():
                    self.writeOutText(config)
                    c = config
                self.drawOutMachine(c)
            else:
                delay *= 1000  # convert to miliseconds
                delay = int(delay)
                count = 0
                for config in self.tm.run_tm_iter():
                    count += 1
                    step = self.tm.step
                    self._jobs.append(self.main.after(delay * count, self.drawOutMachine, config, step))
                    self._jobs.append(self.main.after(delay * count, self.writeOutText, config, step))

    def stepTM(self):
        """Step the TM forward once"""
        if self.tm != None:
            config = self.tm.next_config()
            self.drawOutMachine(config)
            self.writeOutText(config)

    def stepBackTM(self):
        """Step the TM backward once"""
        if self.tm != None:
            config = self.tm.previous_config()
            self.drawOutMachine(config)
            self.writeOutText("Stepping Back\n")
            self.writeOutText(config)

    def resetTM(self):
        """Reset the TM to an unrun state"""
        self.lastRunStep = 0
        self.stopTM()
        if self.bidirectional.get():
            self.drawFirstTape()
        if self.two_tape.get():
            self.drawSecondTape()
        self.drawOutMachine(self.tm.config)

        self.textSimOut.config(state='normal')
        self.textSimOut.delete(1.0, 'end')
        self.writeOutText(self.tm.config)
        self.textSimOut.config(state='disabled')

    def stopTM(self):
        """Stop the continuous run of the TM
        Cancels all tk.after()-scheduled updates and rewinds underlying the machine to the last displayed state.
        """
        if self.tm != None:
            for job in self._jobs:
                self.main.after_cancel(job)
            self.tm.go_back_to_step(self.lastRunStep)
        self._jobs = []

    # Callbacks
    def setTape(self, *args):
        """Callback for when tape input is changed.
        Inform the TM and reset the run.
        """
        if self.tm != None:
            self.tm.set_input_string(self.textTapeInput.get())
            self.resetTM()

    def setBidirectional(self, *args):
        """Callback for when the bidirectional option is changed.
        Inform the TM, reset the run, and disable the other checkbox
        """
        if self.tm != None:
            self.tm.set_bidirectional(self.bidirectional.get())
            self.resetTM()
        else:
            if self.bidirectional.get():
                self.drawFirstTape()
            else:
                self.canvasSimOut.delete('left')

        if (self.bidirectional.get()):
            self.checkbox2Tape.configure(state='normal')
        else:
            self.checkbox2Tape.configure(state='disabled')

    def setTwoTape(self, *args):
        """Callback for when the two tape option is changed.
        Inform the TM, reset the run, and disable the other checkbox
        """
        if self.tm != None:
            file = self.tm.file
            self.tm = None
            if self.two_tape.get():
                self.tm = two_tape_TM(file, input=self.textTapeInput.get(),fill='white')
            else:
                self.tm = turing_machine(file, input=self.textTapeInput.get(), bidirectional=self.bidirectional.get())
            self.resetTM()
        else:
            if self.two_tape.get():
                self.drawSecondTape()
            else:
                self.canvasSimOut.delete('twotape')
        if (not self.two_tape.get()):
            self.checkbox2Way.configure(state='normal')
        else:
            self.checkbox2Way.configure(state='disabled')

    # Drawing functions
    def drawFirstTape(self):
        """Helper function to draw the first tape on the canvas"""
        starty = 150
        for i in range(17):
            if i < 8:
                self.canvasSimOut.create_rectangle(50 * i + 2, starty, 50 * i + 52, starty + 50, fill="#1f6aa5", tag="left", outline="white")
            elif i > 8:
                self.canvasSimOut.create_rectangle(50 * i + 2, starty, 50 * i + 52, starty + 50, fill="#1f6aa5", outline="white")
        # draw highlighted square last to make sure sides are properly colored
        i = 8
        self.canvasSimOut.create_rectangle(50 * i + 2, starty, 50 * i + 52, starty + 50, fill="#333333", outline="white")

    def drawSecondTape(self):
        """Helper function to draw the second tape on the canvas"""
        starty = 300
        for i in range(17):
            if i != 8:
                self.canvasSimOut.create_rectangle(50 * i + 2, starty, 50 * i + 52, starty + 50, fill="", tag="twotape")
        # draw highlighted square last to make sure sides are properly colored
        i = 8
        self.canvasSimOut.create_rectangle(
            50 * i + 2, starty, 50 * i + 52, starty + 50, fill="white", outline="white", tag="twotape")

    def drawOutMachine(self, config, step=None):
        """Draw out the given configuration of the machine on the canvas."""
        if step == None:
            step = self.tm.step
        self.canvasSimOut.delete('text')
        state_text = "State: "
        state = config[4]
        if state < 0:
            if state == -1:
                state_text += 'Accept'
            elif state == -2:
                state_text += 'Reject'
            else:
                state_text += 'Halt'
        else:
            state_text += str(state)

        self.canvasSimOut.create_text(125, 100, text=state_text, font="Times 20", tag='text', fill='white')
        self.canvasSimOut.create_text(725, 100, text="Step: " + str(step), font="Times 20", tag='text',fill='white')
        starty = 150
        if not self.two_tape.get():
            self.canvasSimOut.delete('twotape')
            tape = config[0]
            position = config[3] - 8
            if not self.bidirectional.get():
                self.canvasSimOut.delete('left')
                for i in range(8):
                    if (position + i) >= 0:
                        self.canvasSimOut.create_rectangle(
                            50 * i + 2, starty, 50 * i + 52, starty + 50, fill="#1f6aa5", outline='white', tag='left')
                # draw highlighted square last to make sure sides are properly colored
                i = 8
                self.canvasSimOut.create_rectangle(
                    50 * i + 2, starty, 50 * i + 52, starty + 50, fill="#333333", outline="white")
            for j in range(17):
                if (position + j) < 0 or (position + j) >= 20000:
                    continue
                text = tape[position + j] if tape[position + j] != " " else ""
                self.canvasSimOut.create_text(50 * j + 27, starty + 25, text=text, font="Times 20", tag='text', fill="white")
        else:
            tape1 = config[0][0]
            tape2 = config[0][1]
            position1 = config[3][0] - 8
            position2 = config[3][1] - 8
            for j in range(17):
                if (position1 + j) < 20000:
                    text1 = tape1[position1 + j] if tape1[position1 + j] != " " else ""
                    self.canvasSimOut.create_text(50 * j + 27, starty + 25, text=text1, font="Times 20", tag='text', fill="white")
                if (position2 + j) < 20000:
                    text2 = tape2[position2 + j] if tape2[position2 + j] != " " else ""
                    self.canvasSimOut.create_text(50 * j + 27, starty + 175, text=text2, font="Times 20", tag='text', fill="white")

    def writeOutText(self, config, step=None):
        """Write out the given configuration of the machine in the text output."""
        if step == None:
            step = self.tm.step
        self.lastRunStep = step
        self.textSimOut.config(state='normal')
        if (type(config) != str):
            self.textSimOut.insert('end', "Step: " + str(step) + '\n')
            self.textSimOut.insert('end', self.tm.format_config(config))
            if config[4] < 0:
                if config[4] == -1:
                    result = 'Accept'
                elif config[4] == -2:
                    result = 'Reject'
                else:
                    result = 'Halt'
                self.textSimOut.insert('end', result + '\n')
                self.textSimOut.insert('end', str(step) + ' steps' + '\n')
                tape = ''
                if not self.two_tape.get():
                    for j in range(config[1], config[2] + 1):
                        tape += config[0][j]
                    self.textSimOut.insert('end', tape + '\n')
                else:
                    for j in range(config[1][0], config[2][0] + 1):
                        tape += config[0][0][j]
                    self.textSimOut.insert('end', tape + '\n')
                    tape = ''
                    for j in range(config[1][1], config[2][1] + 1):
                        tape += config[0][1][j]
                    self.textSimOut.insert('end', tape + '\n')

        else:
            self.textSimOut.insert('end', config)
        self.textSimOut.config(state='disabled')
        self.textSimOut.yview(tk.END)


def default_resize(frame):
    """When given a frame, sets all the row and column weights in the grid to 1.
    This means the frame resizes evenly with the window.
    """
    (rows, columns) = frame.grid_size()
    for i in range(rows):
        frame.grid_rowconfigure(i, weight=1)
    for i in range(columns):
        frame.grid_columnconfigure(i, weight=1)


root = ctk.CTk()
try:  # do a fancy icon if available
    img = tk.Image("photo", file="tm.png")
    root.call('wm', 'iconphoto', root._w, img)
except Exception:
    pass
tm_gui = TMGUI(root)
root.minsize(width=WIDTH, height=HEIGHT)
default_resize(root)
root.grid_columnconfigure(2, weight=2)
root.mainloop()
