#!/usr/bin/python

from gi.repository import GES, Gst, Gtk, GObject

import signal

def handle_sigint(sig, frame):
    Gtk.main_quit()
 
def busMessageCb(bus, message):
    if message.type == Gst.MessageType.EOS:
        print("eos")
        Gtk.main_quit()
    elif message.type == Gst.MessageType.ERROR:
        print (message.parse_error())
    else:
        pass
 
def duration_querier(pipeline):
    print(pipeline.query_position(Gst.Format.TIME)[1] / Gst.SECOND)
    return True

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.SimpleLayer.new()
  
  timeline.add_layer(layer)
  
  """
  GES.VideoTestPattern.BLACK
  GES.VideoTestPattern.BLINK
  GES.VideoTestPattern.BLUE
  GES.VideoTestPattern.CHECKERS_1
  GES.VideoTestPattern.CHECKERS_2
  GES.VideoTestPattern.CHECKERS_4
  GES.VideoTestPattern.CHECKERS_8
  GES.VideoTestPattern.CHROMA_ZONE_PLATE
  GES.VideoTestPattern.CIRCULAR
  GES.VideoTestPattern.GAMUT
  GES.VideoTestPattern.GREEN
  GES.VideoTestPattern.RED
  GES.VideoTestPattern.SMPTE
  GES.VideoTestPattern.SMPTE75
  GES.VideoTestPattern.SNOW
  GES.VideoTestPattern.SOLID_COLOR
  GES.VideoTestPattern.WHITE
  GES.VideoTestPattern.ZONE_PLATE
  """
  for i in range(0, 18):
    src = GES.TestClip()
    src.set_property("vpattern", i)
    src.set_property("duration", 1 * Gst.SECOND)
    layer.add_clip(src)

  timeline.commit()

  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)
  
  bus = pipeline.get_bus()
  bus.add_signal_watch()
  bus.connect("message", busMessageCb)
  GObject.timeout_add(1000, duration_querier, pipeline)
 
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
  
simple()
