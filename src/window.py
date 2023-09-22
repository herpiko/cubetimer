# window.py
#
# Copyright 2023 Herpiko Dwi Aguno
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.

from gi.repository import Gtk, Gdk, GLib
import random
import time
import threading


@Gtk.Template(resource_path='/xyz/aguno/CubeTimer/window.ui')
class CubetimerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'CubetimerWindow'

    ScrambleNotation = Gtk.Template.Child("ScrambleNotation")
    Timer = Gtk.Template.Child("Timer")
    Menu = Gtk.Template.Child("Menu")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Events 
        event_controller = Gtk.EventControllerKey()
        event_controller.connect("key-pressed", self.on_key_pressed)
        event_controller.connect("key-released", self.on_key_released)
        self.add_controller(event_controller)
        
                         
        self.timer_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.reset_id = 0
        self.state = "reset"
        
        self.Menu.set_can_focus(False)
        self.Timer.set_can_focus(True)
        self.Timer.grab_focus()
        
        self.generate_scramble()
       
    def generate_scramble(self):
        moves = ["U", "U'", "U2", "D", "D'", "D2", "L", "L'", "L2", "R", "R'", "R2", "F", "F'", "F2", "B", "B'", "B2"]
        scramble = []
        for _ in range(21):
            random_move = random.choice(moves)
            scramble.append(random_move)
        scrambled =  "  ".join(scramble)
        self.ScrambleNotation.set_text(scrambled)

    def update_timer(self):
        print("yo1")
        while self.timer_running:
            GLib.idle_add(self.update_label)
            time.sleep(0.001)           
            
    def update_label(self):
        self.elapsed_time = time.time() - self.start_time
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        milliseconds = int((self.elapsed_time % 1) * 1000)
        self.Timer.set_label(f"{minutes:02}:{seconds:02}.{milliseconds:03}")
       
    def on_start_timer(self):
        self.timer_running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self.update_timer)
        self.thread.start()
        
    def on_key_released(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_space:
            if not self.timer_running and self.elapsed_time == 0 and self.state == "ready":
                self.state = "running"
                self.timer_running = True
                self.start_time = time.time()
                self.thread = threading.Thread(target=self.update_timer)
                self.thread.start()
                
    def on_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_space:
            if self.state == "reset":
                GLib.timeout_add(100, self.ready)
            if self.state == "stopped":
                self.reset()
            if self.timer_running:
                self.state = "stopped"
                self.timer_running = False
                self.generate_scramble()
                
    def ready(self):
        self.state = "ready"
        
    def reset(self):
        if self.state == "stopped":
            self.elapsed_time = 0
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            milliseconds = int((self.elapsed_time % 1) * 1000)
            self.Timer.set_label(f"{minutes:02}:{seconds:02}.{milliseconds:03}")
            self.state = "ready"

       


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'cubetimer'
        self.props.version = "0.1.0"
        self.props.authors = ['Herpiko Dwi Aguno']
        self.props.copyright = '2022 Herpiko Dwi Aguno'
        self.props.logo_icon_name = 'xyz.aguno.CubeTimer'
        self.props.modal = True
        self.set_transient_for(parent)
