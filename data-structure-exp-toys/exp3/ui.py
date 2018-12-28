from tkinter import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import subprocess as sp
from multiprocessing import Process, Queue
import pygraphviz as pgv


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.master.geometry("800x600")

        self.openfile_name = "./test.txt"
        self.openfile_label_str = StringVar(None, self.openfile_name)
        self.status_label_str = StringVar(None, "Ready.")
        self.isGenerateGraph = IntVar()
        self.pyVar_generate_pic = False

        self.program_output = ""

        self.create_widgets()

    def create_widgets(self):
        open_button = Button(self, text="Open...", command=self.openfile)
        open_button.grid(column=0, row=0)
        open_label = Label(self, textvariable=self.openfile_label_str)
        open_label.grid(column=0, row=1)

        vcmd = (self.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        from_label = Label(self, text="From")
        from_label.grid(column=0, row=2)
        self.from_point_box = Entry(self, validate="key", validatecommand=vcmd, width=5)
        self.from_point_box.grid(column=1, row=2)
        to_label = Label(self, text="To")
        to_label.grid(column=0, row=3)
        self.to_point_box = Entry(self, validate="key", validatecommand=vcmd, width=5)
        self.to_point_box.grid(column=1, row=3)

        generate = Checkbutton(self, text="Generate Graph Picture (ALPHA, SLOW)", variable=self.isGenerateGraph)
        generate.grid(column=0, row=4)

        self.start_button = Button(self, text="Start!", command=self.start)
        self.stop_button = Button(self, text="Stop", command=self.stop)
        self.start_button.grid(column=0, row=5)
        self.stop_button.grid(column=1, row=5)

        label_status = Label(self, textvariable=self.status_label_str)
        label_status.grid(column=0, row=6)

        self.textarea = Text(self, width=40, height=30, border=2)
        self.textarea.grid(column=0, row=7)

    def openfile(self):
        self.openfile_name = askopenfilename()
        self.openfile_label_str.set(self.openfile_name)

    def validate(self, d, i, P, s, S, v, V, W):
        # valid percent substitutions (from the Tk entry man page)
        # note: you only have to register the ones you need; this
        # example registers them all for illustrative purposes
        #
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        # from https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
        try:
            if len(P) > 5:
                raise ValueError
            S = int(S)
            return True
        except:
            self.bell()
            return False

    def start(self):
        try:
            if not self.from_point_box.get() or not self.to_point_box.get():
                raise ValueError("Fill in from and to!")
            self.q = Queue()
            self.pyVar_generate_pic = self.isGenerateGraph.get()
            self.p = Process(target=communicate, args=(self.q,
                                                       self.openfile_name,
                                                       int(self.from_point_box.get()),
                                                       int(self.to_point_box.get()),
                                                       int(self.pyVar_generate_pic)))
            self.p.start()
            self.after(50, self.update_status)

        except Exception as e:
            self.status_label_str.set(e)

    def update_status(self):
        while not self.q.empty():
            x = self.q.get()
            print(x)
            if x[0] == "status":
                self.status_label_str.set(x[1])
                if x[1] == "OK." and self.pyVar_generate_pic:
                    imageViewerFromCommandLine = {'linux': 'eog',
                                                  'win32': 'explorer',
                                                  'darwin': 'open'}[sys.platform]
                    sp.run([imageViewerFromCommandLine, "graph.png"])
            else:
                for i in x[1]:
                    self.textarea.insert(END, i)
        else:
            if self.p.is_alive():
                self.status_label_str.set("Running...")
        self.after(50, self.update_status)

    def stop(self):
        if self.p and self.p.is_alive():
            self.p.terminate()
            self.status_label_str.set("Terminated.")
            if not self.q.empty():
                self.q.close()


def communicate(queue, filename, from_value, to_value, generate_pic):
    try:
        print("from: {}, to: {}".format(from_value, to_value))
        f = open(filename, "r")
        content = f.readlines()
        for i in reversed(content):
            i = i.rstrip()
            if i == "":
                content.pop()
            else:
                try:
                    _, __, ___ = i.split()
                except:
                    content.pop()
                break

        # print(content)
        # print("".join(content).encode("ascii"))
        process = sp.Popen("./graph", stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        process.stdin.write("".join(content).encode("ascii"))
        process.stdin.write("\n{} {}\n".format(from_value, to_value).encode("ascii"))
        process.stdin.flush()
        process.wait()
        if process.returncode != 0:
            msg = process.stderr.readline()
            raise RuntimeError(msg)
        out = process.stdout.readlines()

        if generate_pic:
            g = pgv.AGraph(strict=True, directed=False)
            queue.put(("status", "Drawing..."))
            for i in content[1:]:
                try:
                    from_v, to_v, weight_v = i.split()
                    g.add_edge(to_v, from_v)
                except:
                    break

            path = out[-1].strip()[6:].decode("ascii").split(" -> ")
            print(out)
            for i in range(len(path) - 1):
                try:
                    e = g.get_edge(path[i + 1], path[i])
                except:
                    e = g.get_edge(path[i], path[i + 1])
                e.attr['color'] = 'red'
                n1 = g.get_node(path[i]); n2 = g.get_node(path[i + 1])
                n1.attr['color'] = 'red'
                n2.attr['color'] = 'red'

            # dot, circo is too slow
            # neato, sfdp, twopi is too terrible
            g.layout("fdp")
            g.draw("graph.png")

        queue.put(("progout", out))
        queue.put(("status", "OK."))

    except Exception as e:
        queue.put(("status", e))


if __name__ == "__main__":
    app = Application()
    app.mainloop()