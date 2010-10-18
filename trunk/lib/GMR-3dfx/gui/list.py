import container, widget, misc

class ListEntry(widget.Widget):
    widget_type = "Entry"
    def __init__(self, parent, pos, text):
        widget.Widget.__init__(self, parent, pos, None)

        self.size = self.get_text_size(text)

        self.text = text

    def get_size(self):
        return self.size

    def render(self):
        pad = self.get_padding()
        down = 0
        x,y = self.pos.get_pos()
        w,h = self.get_size()
        self.draw_canvas_border((x,y,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                                'background')
        self.draw_text(self.text, (x+pad[0], y+pad[1]))

class List(container.Container):
    widget_type = "List"
    def __init__(self, parent, pos, entries=[], name=None):
        container.Container.__init__(self, parent, (1,1), pos, name)

        self.entries = entries

        self.build_entries()

    def build_entries(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.entries:
            if self.widgets:
                pos = misc.RelativePos()
            else:
                pos = misc.AbsolutePos((0,0))
            new = ListEntry(self, pos, opt)

            s = new.get_size_with_padding()
            width = max(width, s[0])
            height = new.get_pos()[1]+s[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width, height))
