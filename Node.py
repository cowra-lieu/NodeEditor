
SPAWN_X = 100
SPAWN_Y = 100

class Node:
  def __init__(self, canvas, x=SPAWN_X, y=SPAWN_Y, width=140, height=90, label="New Node", **kwargs):
    self.canvas = canvas
    self.x = x
    self.y = y
    self.geometry = self.canvas.create_round_rect(self.x, self.y, width, height, fill='#444444', outline='black')
    self.label = self.canvas.create_text((self.x,self.y+(height/4)), text=label, fill='white')
    self.input = []
    self.output = []

    if 'input' in kwargs:
      for i in range(kwargs['input']):
        posX = self.x - width/2 + 12
        posY = self.y - height/2 - 4 + (i+1)*15
        in_circle = {'object': self.canvas.create_circle(posX, posY, 5, fill='#E57373', activefill='#D3382F'), 'type': 'input', 'connected': False, 'out': None, 'bezier': None}
        self.input.append(in_circle) # selected color: #1E6DBA
        #self.canvas.bind("<Enter>", lambda event, obj=in_circle: self.on_hover_input(event, in_circle))
        #self.canvas.bind("<Leave>", lambda event, obj=in_circle: self.on_leave_input(event, in_circle))

    if 'output' in kwargs:
      for i in range(kwargs['output']):
        posX = self.x + width/2 - 12
        posY = self.y - height/2 - 4 + (i+1)*15
        out_circle = {'object': self.canvas.create_circle(posX, posY, 5, fill='#90CAF9', activefill='#1E6DBA'), 'type': 'output', 'connected': False, 'in': None, 'bezier': None}
        self.output.append(out_circle) # selected color: #E93F33
        #self.canvas.bind("<Enter>", lambda event, obj=out_circle: self.on_hover_output(event, out_circle))
        #self.canvas.bind("<Leave>", lambda event, obj=out_circle: self.on_leave_output(event, out_circle))

  def move(self, x, y):
    self.canvas.move(self.geometry, x, y)
    label_coords = self.canvas.coords(self.label)
    self.canvas.coords(self.label, label_coords[0]+x, label_coords[1]+y)
    for io in self.input + self.output:
      self.canvas.move(io['object'], x, y)

  def inbounds(self, event):
    node_bbox = self.canvas.bbox(self.geometry)
    if (node_bbox[0] < event.x and event.x < node_bbox[2] and
        node_bbox[1] < event.y and event.y < node_bbox[3]):
      return True
    return False

  def io_interaction(self, event):
    for io in self.input + self.output:
      io_bbox = self.canvas.bbox(io['object'])
      if (io_bbox[0] < event.x and event.x < io_bbox[2] and
          io_bbox[1] < event.y and event.y < io_bbox[3]):
        return io
    return None

  def check_move(self, event, lastX, lastY):
    node_bbox = self.canvas.bbox(self.geometry)
    if (node_bbox[0] < event.x and event.x < node_bbox[2] and
        node_bbox[1] < event.y and event.y < node_bbox[3]):
        x = event.x - lastX
        y = event.y - lastY
        self.move(x, y)
        return True
    return False
        

  # def on_hover_input(self, event, obj):
  #   bbox = self.canvas.bbox(obj)
  #   if (bbox[0] < event.x and event.x < bbox[2]
  #       and bbox[1] < event.x and event.x < bbox[3]):
  #     self.canvas.itemconfig(obj, fill='#1E6DBA')

  # def on_hover_output(self, event, obj):
  #   print("hover_output")
  #   self.canvas.itemconfig(obj, fill='#E93F33')

  # def on_leave_input(self, event, obj):
  #   print("leave_input")
  #   self.canvas.itemconfig(obj, fill='#EA525F')

  # def on_leave_output(self, event, obj):
  #   print("leave_input")
  #   self.canvas.itemconfig(obj, fill='#2582DC')