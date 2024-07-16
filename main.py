from panda3d.core import loadPrcFileData
loadPrcFileData("", "textures-power-2 up")
loadPrcFileData("", "show-frame-rate-meter f")
loadPrcFileData("", "win-size 800 600")
from panda3d.core import *
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectButton import DirectButton
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task

class MusicPlayer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Load music
        self.music = loader.loadSfx("LetOurVoicesRiseLikeIncense.ogg")
        self.music.setLoop(True)
        # Create GUI elements
        self.slider = DirectSlider(range=(0, self.music.length()),value=0,command=self.set_music_time, scale=(1.1, 0.6, 0.6), pos=(-0.2, 0, -0.93))
        self.start_button = DirectButton(text=" Play ", command=self.start_music, scale=(0.1, 0.08, 0.07), pos=(1, 0, -0.93))
        # Initial state
        self.playing = False
        self.mainLoop = taskMgr.add(self.update, "update")
        self.image = self.loadImageAsPlane("dining-hall.jpg")
        self.image.reparentTo(render)    
        self.image.setPos(0,10,0.1)   
    def set_music_time(self):
        if(self.playing == False):
            self.music.setTime(self.slider["value"])
    def start_music(self):
        self.start_button["text"] = "Stop"
        if(self.playing == False):
            self.music.play()
            self.playing = True
        else:
           self.start_button["text"] = "Play"
           self.music.stop()
           self.playing = False 
    def loadImageAsPlane(self, filepath, yresolution = 600):
        tex = loader.loadTexture(filepath)
        tex.setBorderColor(Vec4(0,0,0,0))
        tex.setWrapU(Texture.WMBorderColor)
        tex.setWrapV(Texture.WMBorderColor)
        cm = CardMaker(filepath + " card")
        cm.setFrame(-tex.getOrigFileXSize(), tex.getOrigFileXSize(), -tex.getOrigFileYSize(), tex.getOrigFileYSize())
        card = NodePath(cm.generate())
        card.setTexture(tex)
        card.setTransparency(1)
        card.setScale(card.getScale()/ yresolution)
        card.flattenLight()
        return card
    def update(self, task):
      if(self.playing):
          self.slider["value"] = self.music.getTime()
      return Task.cont
app = MusicPlayer()
app.run()