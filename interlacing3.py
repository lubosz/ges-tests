#!/usr/bin/python

from gi.repository import GES, Gst, GLib

imageFile = "file:///home/bmonkey/workspace/ges/data/LAMP_720_576.jpg"

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline()
  timeline.add_track(GES.VideoTrack.new())

  layer = GES.Layer()
  timeline.add_layer(layer)
  
  asset = GES.UriClipAsset.request_sync(imageFile)

  layer.add_asset(asset, 0 * Gst.SECOND, 0, 3 * Gst.SECOND, GES.TrackType.VIDEO)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)

  mainLoop = GLib.MainLoop.new(None, False)
  GLib.timeout_add_seconds(3, quit, mainLoop)
  GLib.MainLoop().run()
  
simple()
