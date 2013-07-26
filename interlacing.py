#!/usr/bin/python

from gi.repository import GES, Gst, GLib

# File URL http://ftp.nluug.nl/ftp/graphics/blender/apricot/trailer/sintel_trailer-480p.ogv

videoFile = "file:///home/bmonkey/workspace/ges/data/sintel_trailer-480p.ogv"

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  video_layer = GES.Layer()
  
  timeline.add_layer(video_layer)

  video_asset = GES.UriClipAsset.request_sync(videoFile)
  video_layer.add_asset(video_asset, 0, 4 * Gst.SECOND, 3 * Gst.SECOND, video_asset.get_supported_formats())

  timeline.commit()

  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)
    
  mainLoop = GLib.MainLoop.new(None, False)
  GLib.timeout_add_seconds(3, quit, mainLoop)
  GLib.MainLoop().run()
  
simple()
