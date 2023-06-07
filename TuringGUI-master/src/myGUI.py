import customtkinter

try:  # python 3: default
    import tkinter as tk
    import customtkinter as ctk
    from tkinter import ttk, scrolledtext, filedialog
    import graphviz
except ImportError:  # python 2
    import Tkinter as tk
    import customtkinter as ctk
    import ttk, ScrolledText as scrolledtext, tkFileDialog as filedialog
    import graphviz

import os, graphviz

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
        self.labelEditor = customtkinter.CTkLabel(self.frameEditor, text="Editeur")
        self.labelEditor.grid(row=0, column=1)
        self.textEditor = ctk.CTkTextbox(self.frameEditor, height=590, width=40, wrap=ctk.WORD)
        self.textEditor.grid(row=1, column=0, columnspan=3, pady=7, padx=7, sticky='news')



        self.buttonSave = ctk.CTkButton(self.frameEditor, width=10, text="      Enregistrer      ",
                                        command=self.saveTM)
        self.buttonSave.grid(row=2, column=2, padx=20, pady=5)
        self.buttonLoad = ctk.CTkButton(self.frameEditor, width=10, text="           Charger           ",
                                        command=self.loadTM)

        self.buttonLoad.grid(row=2, column=0, padx=20, pady=5)


        #self.frameEditor.grid(row=3, column=3, padx=15, pady=10, sticky='news')
        self.frameEditor.place(x=900, y=10)

        default_resize(self.frameEditor)

        ### LEFT FRAME: Simulator
        self.frameSim = customtkinter.CTkFrame(self.main, width=830)
        self.labelSim = customtkinter.CTkLabel(self.frameSim, text="Simulateur de machine de Turing")
        #self.labelSim.grid(row=0, column=0, columnspan=3, pady=7, padx=7)
        self.labelSim.place(x=300, y=18)

        self.frameInput = customtkinter.CTkFrame(self.frameSim)
        customtkinter.CTkLabel(self.frameInput, text="Entrée du ruban : ", pady=7, padx=7).pack(side='left')
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
                                             values=["Inverser une chaine de caractère",
                                                     "Addition de deux nombre",
                                                     "Language de concaténation 1",
                                                     "Language de concaténation 2"
                                                     ],
                                             command=combobox_callback, width=400, height=40,
                                             variable=combobox_var)
        #self.combobox.pack(padx=20, pady=10)
        self.combobox.place(x=424,y=63)


        self.frameStep = customtkinter.CTkFrame(self.frameSim)
        self.buttonStep = ctk.CTkButton(self.frameStep, width=10, text="   Une étape   ", command=self.stepTM)
        self.buttonStep.grid(row=0, column=0, pady=7, padx=7)
        self.buttonStepBack = ctk.CTkButton(self.frameStep, width=10, text="   Reculer   ", command=self.stepBackTM)
        self.buttonStepBack.grid(row=0, column=2, pady=5, padx=7)
        self.labelSim = customtkinter.CTkLabel(self.frameSim, text=" ")
        # self.labelSim.grid(row=0, column=0, columnspan=3, pady=7, padx=7)
        self.labelSim.place(x=415, y=160)
        self.buttonGraph = ctk.CTkButton(self.frameSim, width=50, text="             Générer le graphe             ",
                                        command=self.graphTM)

        self.buttonGraph.place(x=620,y=160)

        self.frameStep.place(x=620, y=110)

        # Check boxes
        #####################################################################################################
        self.frameCheck = customtkinter.CTkFrame(self.frameSim)
        self.bidirectional = tk.BooleanVar()

        # self.bidirectional = ctk.Variable
        # self.checkbox2Way = tk.Checkbutton(
        # self.frameCheck, text="Bidirectional", var=self.bidirectional, command=checkbox_event, onvalue=True, offvalue=False)

        #self.checkbox2Way = ctk.CTkCheckBox(self.frameCheck,text="Bidirectional", onvalue=True, offvalue=False)
        #self.checkbox2Way.select()
        #self.checkbox2Way.grid(row=0, sticky='w', pady=7, padx=7)
        self.two_tape = tk.BooleanVar()
        # self.checkbox2Tape = ctk.CTkCheckBox(self.frameCheck, text="Two Tape", var=self.two_tape, onvalue=True, offvalue=False)

        # self.checkbox2Tape = ctk.CTkCheckBox(self.frameCheck, text="Two Tape", onvalue=True, offvalue=False)

        # self.checkbox2Tape.grid(row=1, sticky='w', pady=7, padx=7)
        # self.two_tape.trace("w", self.setTwoTape)
        # self.bidirectional.trace("w", self.setBidirectional)
        # self.frameCheck.grid(row=3, column=2)c
        #self.frameCheck.place(x=408, y=110)
        #####################################################################################################


        # Controls
        self.frameRun = customtkinter.CTkFrame(self.frameSim)
        self.buttonRun = ctk.CTkButton(self.frameRun, width=100, text="              Exécuter              ", command=self.runTM)
        self.buttonRun.grid(row=0, column=0, pady=7, padx=7)
        self.buttonStop = ctk.CTkButton(self.frameRun, width=100, text="              Arrêter              ", command=self.stopTM)
        self.buttonStop.grid(row=0, column=1, pady=7, padx=7)
        self.buttonReset = ctk.CTkButton(self.frameRun, width=100, text="         Réinitialiser         ", command=self.resetTM)
        self.buttonReset.grid(row=1, column=1, pady=7, padx=7)
        self.frameDelay = ctk.CTkFrame(self.frameRun)
        ctk.CTkLabel(self.frameDelay, text="Retardement (s)").pack(side='left', padx=5)
        self.textDelay = ctk.CTkEntry(self.frameDelay, width=50)
        self.textDelay.insert(0, "0.1")
        self.textDelay.pack(side='right')
        self.frameDelay.grid(row=1, column=0, pady=7, padx=7)
        self.frameRun.place(x=20, y=110)




        # Tape frame

        self.tapeframe = customtkinter.CTkFrame(self.frameSim, width=200)
        self.tapeframe.place(x=10, y=220)
        self.tabview = customtkinter.CTkTabview(self.tapeframe,width=828, height=420)
        self.tabview.pack(padx=10, pady=10)

        self.tabview.add("     Ruban     ")  # add tab at the end
        self.tabview.add("     Texte     ")  # add tab at the end
        self.tabview.set("     Ruban     ")  # set currently visible tab

        #################################### Tape Frame     ####################################

        self.canvasSimOut = ctk.CTkCanvas(self.tabview.tab("     Ruban     "), bg="#2b2b2b", width=10, height=10, highlightbackground="#2b2b2b")
        self.drawFirstTape()
        self.canvasSimOut.pack(expand=1, fill='both')

        # Text Frame
        self.textSimOut = scrolledtext.ScrolledText(self.tabview.tab("     Texte     "), state='disabled', height=10, width=55, wrap=tk.WORD)
        self.textSimOut.configure(bg='#2b2b2b', fg='white',highlightbackground='red')
        self.textSimOut.pack(expand=1, fill='both')

        self.frameSim.grid(row=0, column=0, rowspan=10, padx=15, pady=10, sticky="news")

        default_resize(self.frameSim)
        self.frameSim.grid_rowconfigure(0, weight=0)
        self.frameSim.grid_rowconfigure(1, weight=0)

    # Editor Buttons

    def loadTMSelectList(self, choice):
        """Load a TM from a specification file into the editor and simulator"""
        if choice == 'Inverser une chaine de caractère':
            tmFileName = '../Docs/Examples/reverse_oneway.tm'

        if choice == 'Addition de deux nombre':
            tmFileName = '../Docs/Examples/addition.tm'

        if choice == 'Language de concaténation 1':
            tmFileName = '../Docs/Examples/language_aabbaaaa.tm'

        if choice == 'Language de concaténation 2':
            tmFileName = '../Docs/Examples/another_lang2.tm'

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

    def graphTM(self):
        """Get a TM specification file from the user, and graph it"""
        tmFileName = filedialog.askopenfilename(
            initialdir=CWD, title="Select TM File", filetypes=[("TM files", "*.tm"), ("all", "*.*")])
        if tmFileName == '':
            return
        tmgraphdict = TMGUI.make_state_dict(tmFileName)
        file = os.path.basename(tmFileName)[:-3]
        TMGUI.generate_graph(tmgraphdict, file)

    @staticmethod
    def generate_graph(dict, file="turing_machine"):
        """Take the dictionary from make_state_dict(), turn it into a Digraph object and render"""
        d = dict
        g = graphviz.Digraph(graph_attr={"dpi": "300"})
        for key in d:
            state = str(key[0])
            newstate = str(key[1])
            if newstate == '-1':
                newstate = 'Accept'
            if newstate == '-2':
                newstate = 'Reject'
            if newstate == '-3':
                newstate = 'Halt'
            val = d[key]
            sym = str(val[0])
            newsym = str(val[1])
            direction = val[2]
            comma = ', ' if newsym else ''
            g.edge(state, newstate, label="< " + sym + " &#8594; " + newsym + comma + direction + ">")  #use HTML labels
        g.render(file, directory='img', format="png", cleanup=True, view=True)

    @staticmethod
    def make_state_dict(filename):
        """Turn a configuration file into a state-state dictionary. Used in generating images of the TM.
        Returns:
        a dictionary with key-value pairs (q,q'):(C,C',D,X) where q,q' are states, C, C' are the lists of input and output symbols, D is direction, and X is a flag for coloring
        """
        f = open(filename, 'r')
        d = {}
        for line in f:
            seq = line.split()
            if (len(seq) > 0) and (seq[0][0] != '#'):
                state = int(seq[0])
                sym = seq[1]
                if sym == 'B':
                    sym = "&#9633;"  # a square character
                newstate = int(seq[2])
                newsym = seq[3]
                direction = seq[4]
                if newsym == 'B':
                    newsym = "&#9633;"
                if newsym == sym:
                    newsym = ''
                k = (state, newstate)
                if k in d:
                    cur = tuple(d[k])
                    if (cur[0] != sym):
                        sym = cur[0] + ', ' + sym
                    if not (cur[1] == newsym):
                        newsym = cur[1] + ', ' + newsym
                    if not (cur[2] == direction):
                        direction = cur[2] + ', ' + direction
                d[k] = (sym, newsym, direction)
        f.close()
        return d

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
        for i in range(30):
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
        state_text = "État: "
        state = config[4]
        if state < 0:
            if state == -1:
                state_text += 'Accepter'
            elif state == -2:
                state_text += 'Rejeter'
            else:
                state_text += 'Halt'
        else:
            state_text += str(state)

        self.canvasSimOut.create_text(125, 100, text=state_text, font="Times 20", tag='text', fill='white')
        self.canvasSimOut.create_text(725, 100, text="Étape: " + str(step), font="Times 20", tag='text',fill='white')
        starty = 150
        if not self.two_tape.get():
            self.canvasSimOut.delete('twotape')
            tape = config[0]
            position = config[3] - 8
            if not self.bidirectional.get():
                self.canvasSimOut.delete('left')
                for i in range(15):
                    if (position + i) >= 0:
                        self.canvasSimOut.create_rectangle(
                            50 * i + 2, starty, 50 * i + 52, starty + 50, fill="#1f6aa5", outline='white', tag='left')
                # draw highlighted square last to make sure sides are properly colored
                i = 8
                self.canvasSimOut.create_rectangle(
                    50 * i + 2, starty, 50 * i + 52, starty + 50, fill="#333333", outline="white")
            for j in range(20):
                if (position + j) < 0 or (position + j) >= 20000:
                    continue
                text = tape[position + j] if tape[position + j] != " " else ""
                self.canvasSimOut.create_text(50 * j + 27, starty + 25, text=text, font="Times 20", tag='text', fill="white")
        else:
            tape1 = config[0][0]
            tape2 = config[0][1]
            position1 = config[3][0] - 8
            position2 = config[3][1] - 8
            for j in range(20):
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
            self.textSimOut.insert('end', "Étape: " + str(step) + '\n')
            self.textSimOut.insert('end', self.tm.format_config(config))
            if config[4] < 0:
                if config[4] == -1:
                    result = 'Acceptée'
                elif config[4] == -2:
                    result = 'Rejetée'
                else:
                    result = 'Halt'
                self.textSimOut.insert('end', result + '\n')
                self.textSimOut.insert('end', str(step) + ' Étapes' + '\n')
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
