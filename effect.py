#!/usr/bin/python

from IPython import embed

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal

videoFile1 = "file:///home/bmonkey/workspace/ges/data/trailer_480p.mov"
videoFile2 = "file:///home/bmonkey/workspace/ges/data/Sesame Street- Kermit and Joey Say the Alphabet.mp4"
videoFile3 = "file:///home/bmonkey/workspace/ges/data/BlenderFluid.webm"
videoFile4 = "file:///home/bmonkey/workspace/ges/data/Blender Physics Animation HD.flv"

imageFile1 = "file:///home/bmonkey/workspace/ges/data/gradient720x576.jpg"
imageFile2 = "file:///home/bmonkey/workspace/ges/data/gradient1280x576.jpg"
imageFile3 = "file:///home/bmonkey/workspace/ges/data/gradient720x720.jpg"
imageFile4 = "file:///home/bmonkey/workspace/ges/data/gradient1280x720.jpg"
imageFile5 = "file:///home/bmonkey/workspace/ges/data/gradient1920x1080.jpg"

outputFile = 'file:///home/bmonkey/workspace/ges/export/shakemGESimageTest'

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
  
  #layer = GES.Layer()
  layer = GES.SimpleLayer.new()
  
  timeline.add_layer(layer)
  
  asset = GES.UriClipAsset.request_sync(videoFile1)
  
  #src = GES.UriClip.new(videoFile1)
  #src = GES.SourceClip()
  #src.add_asset(asset)
  src = GES.TestClip()
  src.set_property("vpattern", GES.VideoTestPattern.SMPTE75)
  
  src.set_property("duration", 5 * Gst.SECOND)
  src.set_property("in-point", 5 * Gst.SECOND)
  #src.set_property("supported-formats", GES.TrackType.VIDEO)
  
  effect = GES.Effect.new("agingtv")
  #effect = GES.Effect.new("videobalance saturation=1.5 hue=+0.5")
  #effect = GES.Effect.new("frei0r-filter-scale0tilt scale-x=1.0")
  #embed()
    
  #layer.add_asset(asset, 0 * Gst.SECOND, 5  * Gst.SECOND, 10  * Gst.SECOND, GES.TrackType.VIDEO)
  
  layer.add_clip(src)
  
  #layer.add_object(src, 0)
  
  src.add(effect)

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
