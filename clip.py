#!/usr/bin/python

from gi.repository import GES, Gst, GLib

# File URL http://download.blender.org/peach/trailer/trailer_400p.ogg

videoFile = "file:///home/bmonkey/workspace/ges/data/trailer_400p.ogg"

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  asset = GES.UriClipAsset.request_sync(videoFile)
  
  layer = GES.Layer()
  timeline.add_layer(layer)
  layer.add_asset(asset, 0, 0 * Gst.SECOND, 10 * Gst.SECOND, asset.get_supported_formats())
  
  #timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)
    
  mainLoop = GLib.MainLoop.new(None, False)
  GLib.timeout_add_seconds(10, quit, mainLoop)
  GLib.MainLoop().run()
  
simple()
