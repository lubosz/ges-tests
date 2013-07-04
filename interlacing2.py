#!/usr/bin/python

from gi.repository import GES, Gst, GLib

videoFile = "file:///home/bmonkey/workspace/ges/data/trailer_480p.mov"
imageFile = "file:///home/bmonkey/workspace/ges/data/wallpaper-1946968.jpg"

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.Layer()
  
  timeline.add_layer(layer)

  asset = GES.UriClipAsset.request_sync(videoFile)
  
  imageasset = GES.UriClipAsset.request_sync(imageFile)

  layer.add_asset(imageasset, 0 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset, 0 * Gst.SECOND, 0, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)

  mainLoop = GLib.MainLoop.new(None, False)
  GLib.timeout_add_seconds(10, quit, mainLoop)
  GLib.MainLoop().run()
  
simple()
