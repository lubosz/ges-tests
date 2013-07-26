#!/usr/bin/python

from gi.repository import GES, Gst, GLib

# File URL http://download.blender.org/peach/trailer/trailer_400p.ogg

videoFile1 = "file:///home/bmonkey/workspace/ges/data/trailer_400p.ogg"

videoFile2 = "file:///home/bmonkey/workspace/ges/data/Sesame Street- Kermit and Joey Say the Alphabet.mp4"

musicFile = "file:///home/bmonkey/workspace/ges/data/prof.ogg"

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.Layer()
  timeline.add_layer(layer)

  asset1 = GES.UriClipAsset.request_sync(videoFile1)
  layer.add_asset(asset1, 0, 20 * Gst.SECOND, 3 * Gst.SECOND, asset1.get_supported_formats())

  asset2 = GES.UriClipAsset.request_sync(videoFile2)
  layer.add_asset(asset2, 3 * Gst.SECOND, 0 * Gst.SECOND, 3 * Gst.SECOND, asset2.get_supported_formats())


  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)
    
  mainLoop = GLib.MainLoop.new(None, False)
  GLib.timeout_add_seconds(6, quit, mainLoop)
  GLib.MainLoop().run()
  
simple()
