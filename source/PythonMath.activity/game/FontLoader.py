import spyral

#copied from https://github.com/platipy/spyral/blob/master/examples/fonts.py
#----------------------------------------------------------------------------
class Text(spyral.Sprite):
    def __init__(self, scene, font, text):
        spyral.Sprite.__init__(self, scene)
        self.image = font.render(text)


class GuidedText(spyral.Sprite):
    def __init__(self, scene, font, text, y):
        spyral.Sprite.__init__(self, scene)
        big_font = spyral.Font(font, 36)
        small_font = spyral.Font(font, 11)
        self.image = big_font.render(text)

        self.anchor = 'center'
        self.pos = scene.rect.center
        self.y = y

        guides = [("baseline", big_font.ascent),
                  ("linesize", big_font.linesize)]
        for name, height in guides:
            self.image.draw_rect((0,0,0),
                                 (0,0),
                                 (self.width, height),
                                 border_width = 1,
                                 anchor= 'topleft')
            guide = Text(scene, small_font, name)
            guide.pos = self.pos
            guide.x += self.width / 2
            guide.y += - self.height / 2 + height
            guide.anchor = 'midleft'

#end copy.
#-------------------------------------------------------------------

