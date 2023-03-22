import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RadioDialog(Gtk.Dialog):
    def __init__(self, parent,options,term):
        Gtk.Dialog.__init__(self, "Choose External Ontology for \""+term+"\"", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        parent.addTextChatBot("Choose External Ontology for \""+term+"\"")
        self.set_default_size(150, 100)
        self.selected_option = None
        # Create a box to hold the radio buttons
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.get_content_area().add(box)
        previousButton=None
        buttons=[]
        i=0
        for option in options:
            buttons.append(Gtk.RadioButton.new_with_label_from_widget(previousButton,option))
            buttons[i].connect("toggled", self.on_button_toggled, option)
            box.pack_start(buttons[i], False, False, 0)
            if previousButton==None:
                previousButton=buttons[i]
                self.selected_option=option
            i+=1
        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.selected_option = name

    def run(self):
        Gtk.Dialog.run(self)
        self.destroy()

        return self.selected_option

class CheckDialog(Gtk.Dialog):
    def __init__(self, parent, options,type,term=None):
        Gtk.Dialog.__init__(self, "Choose "+type+" of \""+term+"\"", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        parent.addTextChatBot("Choose Parents of \""+term+"\"")
        self.set_default_size(150, 100)
    
        self.selected_options = []
        # Create a box to hold the check buttons
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.get_content_area().add(box)


        # Create the check buttons and add them to the box
        for option in options:
            button = Gtk.CheckButton.new_with_label(option)
            button.connect("toggled", self.on_button_toggled, option)
            box.pack_start(button, False, False, 0)


        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.selected_options.append(name)
        else:
            self.selected_options.remove(name)

    def run(self):
        Gtk.Dialog.run(self)
        self.destroy()
        return self.selected_options
    
class CheckDialogRelationship(Gtk.Dialog):
    def __init__(self, parent, options):
        Gtk.Dialog.__init__(self, "Choose the relationships you want to keep", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        parent.addTextChatBot("Choose the relationships you want to keep")
        self.set_default_size(150, 100)
    
        self.selected_options = []
        # Create a box to hold the check buttons
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.get_content_area().add(box)


        # Create the check buttons and add them to the box
        for option in options:
            button = Gtk.CheckButton.new_with_label(option)
            button.toggled()
            button.connect("toggled", self.on_button_toggled, option)
            box.pack_start(button, False, False, 0)


        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.selected_options.append(name)
        else:
            self.selected_options.remove(name)

    def run(self):
        Gtk.Dialog.run(self)
        self.destroy()
        return self.selected_options