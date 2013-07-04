#!/usr/bin/python

from gi.repository import GES, Gst, GLib

imageFile = "file:///home/bmonkey/workspace/ges/data/LAMP_720_576.jpg"

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  imagelayer = GES.Layer()
  

  timeline.add_layer(imagelayer)
  
  imageasset = GES.UriClipAsset.request_sync(imageFile)
  
  imagelayer.add_asset(imageasset, 5 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.VIDEO)

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)
    
  mainLoop = GLib.MainLoop.new(None, False)
  GLib.timeout_add_seconds(60, quit, mainLoop)
  GLib.MainLoop().run()
  
simple()
