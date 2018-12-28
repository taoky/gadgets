from tkinter import *
from tkinter.filedialog import *
from multiprocessing import Process, Queue
from huffman import HuffZipFile
from sys import platform

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.mode = IntVar(None, 0) # set compress as default
        self.openfile_name = ""
        self.savefile_name = ""
        self.label_open = StringVar()
        self.label_save = StringVar()
        self.label_status = StringVar(None, "Ready.")
        self.pack()
        self.master.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):

        # Radio Buttons
        rbCompress = Radiobutton(self, text="Compress", variable=self.mode, value=0)
        rbDecompress = Radiobutton(self, text="Decompress", variable=self.mode, value=1)
        rbCompress.grid(column=0, row=0)
        rbDecompress.grid(column=1, row=0)

        # File Choose Buttons
        button = Button(self, text="Open From...", command=self.openfile)
        button.grid(column=0, row=1)

        button = Button(self, text="Save to...", command=self.savefile)
        button.grid(column=1, row=1)

        # File Information Labels
        label1 = Label(self, textvariable=self.label_open)
        label1.grid(column=0, row=2)
        label2 = Label(self, textvariable=self.label_save)
        label2.grid(column=0, row=3)

        # Start/Stop Buttons
        self.start_button = Button(self, text="Start!", command=self.start)
        self.stop_button = Button(self, text="Stop", command=self.stop)
        self.start_button.grid(column=0, row=4)
        self.stop_button.grid(column=1, row=4)

        # Status Label
        label3 = Label(self, textvariable=self.label_status)
        label3.grid(column=0, row=5)

    def openfile(self):
        if self.mode.get() == 1:
            filetypes = [("Huff files", ".huff"),
                         ("All files", ".*")]
        else:
            filetypes = []
        self.openfile_name = askopenfilename(filetypes=filetypes)
        if self.openfile_name:
            self.label_open.set("Open file: {}".format(self.openfile_name))

    def savefile(self):
        defaultextension = ''
        if self.mode.get() == 0:
            filetypes = [("Huff files", ".huff"),
                         ("All files", ".*")]
            if platform == 'darwin':
                defaultextension = '.huff'
        else:
            filetypes = []
        self.savefile_name = asksaveasfilename(filetypes=filetypes,
                                               defaultextension=defaultextension)
        self.label_save.set("Save file: {}".format(self.savefile_name))

    def start(self):
        self.q = Queue()
        self.p = Process(target=do_compression, args=(self.q,
                                                      self.openfile_name,
                                                      self.savefile_name,
                                                      self.mode.get()))
        self.p.start()

        self.after(100, self.update_status)

    def update_status(self):
        if not self.q.empty():
            self.label_status.set(self.q.get())
        else:
            self.label_status.set("Running...")
            self.after(50, self.update_status)

    def stop(self):
        if self.p and self.p.is_alive():
            self.p.terminate()
            self.label_status.set("Terminated.")
            if not self.q.empty():
                self.q.close()


def do_compression(queue, open_file, save_file, mode : int):
    try:
        from_file = open(open_file, "rb")
        to_file = open(save_file, "wb")
        zip_file = HuffZipFile(decompress=bool(mode),
                               file_stream=from_file)
        if mode:
            zip_file.decompress(to_file)
        else:
            zip_file.compress(to_file)
        queue.put("OK!")
    except Exception as e:
        queue.put(e)
