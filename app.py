import os, math
from tkinter import *
from tkinter.ttk import *
from functools import partial
from MyCanvas import *
from Node import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400

# TODO: Add delete buttons for nodes and io ports

class App(Frame):
  def __init__(self, parent):
    Frame.__init__(self, parent)
    self.move_pos = ()
    self.nodes = []
    self.draw = False
    self.from_io = None
    self.to_io = None
    self.current_bezier = None

    control_frame = Frame(self, relief='raise', borderwidth=1)
    control_frame.pack(side=TOP, fill=BOTH, expand=YES)
    Button(control_frame, width=8, text='test').grid()

    graph_frame = Frame(self, relief='raise', borderwidth=1)
    graph_frame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    self.canvas = MyCanvas(graph_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='#141414')
    self.canvas.pack()

    #self.canvas.create_line(5, 5, 50, 5, 100, 50, 150, 50, smooth=1)
    # c1 = (20, 50)
    # c2 = (80, 50)
    # c3 = (30, 100)
    # c4 = (90, 100)
    # self.canvas.create_bezier(c1, c2, c3, c4)

    self.nodes.append(Node(self.canvas, x=100, y=200, label="Hello Node", input=2, output=3))
    self.nodes.append(Node(self.canvas, x=400, y=200, label="My Node 1", input=2, output=2))
    self.nodes.append(Node(self.canvas, x=600, y=200, label="My Node 2", input=4, output=1))
    self.nodes.append(Node(self.canvas, x=600, y=300, width=180, height=40 , label="My Node 3", input=1))

    self.canvas.bind('<Button-1>', self.cb_click)
    self.canvas.bind("<ButtonRelease-1>", self.cb_release)

  def cb_click(self, evt):
    # Check for all nodes, if user clicked inside their geometries
    for node in self.nodes:
        io = node.io_interaction(evt) # returns io object, if user clicked inside an io port
        # user clicked inside io port
        if io:
            if not io['connected']:
                self.draw = True
                self.from_io = io
                self.canvas.bind("<B1-Motion>", lambda event, n=node: self.cb_move(event, n))
            break
        # user clicked inside node
        elif node.inbounds(evt):        
            self.move_pos = (evt.x, evt.y)
            self.canvas.bind("<B1-Motion>", lambda event, n=node: self.cb_move(event, n))
            break

  def cb_release(self, event):
    if self.draw:
        for node in self.nodes:
            io = node.io_interaction(event)
            if io and io != self.from_io and not io['connected']:
                self.from_io['connected'] = True
                io['connected'] = True
                if self.from_io['type'] == 'input':
                    self.from_io['out'] = io
                    io['in'] = self.from_io
                else:
                    self.from_io['in'] = io
                    io['out'] = self.from_io
                from_coords = self.canvas.coords(self.from_io['object'])
                to_coords = self.canvas.coords(io['object'])
                xFrom = from_coords[0]+5
                yFrom = from_coords[1]+5
                xTo = to_coords[0]+5
                yTo = to_coords[1]+5
                c1 = (xFrom, yFrom)
                c2 = (xFrom+60, yFrom)
                c3 = (xTo-60, yTo)
                c4 = (xTo, yTo)
                if self.to_io:
                    self.to_io = None
                final_bezier = self.canvas.create_bezier(c1, c2, c3, c4)
                self.from_io['bezier'] = final_bezier
                io['bezier'] = final_bezier
                if self.from_io['type'] == 'input':
                    self.canvas.itemconfig(self.from_io['object'], fill='#D3382F')
                else:
                    self.canvas.itemconfig(self.from_io['object'], fill='#1E6DBA')
                break
        if self.current_bezier:
            self.canvas.delete_bezier(self.current_bezier)
            self.current_bezier = None
        self.draw = False
    self.canvas.unbind("<B1-Motion>")

  def cb_move(self, event, node):
    if self.draw:
        if self.current_bezier:
            self.canvas.delete_bezier(self.current_bezier)
        from_coords = self.canvas.coords(self.from_io['object'])
        xFrom = from_coords[0]+5
        yFrom = from_coords[1]+5
        xTo = event.x
        yTo = event.y
        c1 = (xFrom, yFrom)
        c2 = (xFrom+60, yFrom)
        c3 = (xTo-60, yTo)
        c4 = (xTo, yTo)
        self.current_bezier = self.canvas.create_bezier(c1, c2, c3, c4)
        self.from_io['bezier'] = self.current_bezier
        for n in self.nodes:
            if n == node:
                continue 
            io = n.io_interaction(event)
            # if user hovers over legal io port, we want to fill the port with active color
            if io and io != self.from_io and io['type'] != self.from_io['type'] and not io['connected']:
                if io['type'] == 'input':
                    self.canvas.itemconfig(io['object'], fill='#D3382F')
                else:
                    self.canvas.itemconfig(io['object'], fill='#1E6DBA')
                self.to_io = io
                return
        # if a port was filled due to hovering, but user left the port without releasing button
        if self.to_io:
            if self.to_io['type'] == 'input':
                self.canvas.itemconfig(self.to_io['object'], fill='#E57373')
            else:
                self.canvas.itemconfig(self.to_io['object'], fill='#90CAF9')
            self.to_io = None
    else:
        x = event.x - self.move_pos[0]
        y = event.y - self.move_pos[1]
        node.move(x, y)
        for io in node.input + node.output:
            if io['connected']:
                if io['type'] == 'input':
                    from_io = io['out']
                    from_coords = self.canvas.coords(from_io['object'])
                    to_coords = self.canvas.coords(io['object'])
                else:
                    from_io = io['in']
                    from_coords = self.canvas.coords(io['object'])
                    to_coords = self.canvas.coords(from_io['object'])
                xFrom = from_coords[0]+5
                yFrom = from_coords[1]+5
                xTo = to_coords[0]+5
                yTo = to_coords[1]+5
                c1 = (xFrom, yFrom)
                c2 = (xFrom+60, yFrom)
                c3 = (xTo-60, yTo)
                c4 = (xTo, yTo)
                self.canvas.delete_bezier(io['bezier'])
                new_bezier = self.canvas.create_bezier(c1, c2, c3, c4)
                from_io['bezier'] = new_bezier
                io['bezier'] = new_bezier
    self.move_pos = (event.x, event.y)

if __name__ == "__main__":
  root = Tk()

  main = App(root)
  main.pack(fill=BOTH, expand=YES)

  root.title('Node Editor v0.1')
  root.resizable(False, False)
  #root.geometry('800x600')
  root.mainloop()
