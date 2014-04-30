from gettext import gettext as _
import gtk
import pygame
import sugar.activity.activity
import sugar.graphics.toolbutton
import libraries
libraries.setup_path()
import sugargame2
import sugargame2.canvas
import spyral

from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import StopButton

class Activity(sugar.activity.activity.Activity):
    def __init__(self, handle):
        super(Activity, self).__init__(handle)
        self.paused = False
        
        self._pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()
        
        def run():
            import game
            spyral.director.init((0,0), fullscreen = False, max_fps = 30)
            game.main()
            spyral.director.run(sugar = True)
            
        self._pygamecanvas.run_pygame(run)

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass


def main():
    spyral.director.init((0,0), fullscreen = False, max_fps = 30)
    import game
    game.main()
    try:
        spyral.director.run()
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()
