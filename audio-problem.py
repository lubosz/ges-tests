#!/usr/bin/python

from gi.repository import GES, Gst, GLib

# File URL http://download.blender.org/peach/trailer/trailer_400p.ogg

videoFile = "file:///home/bmonkey/workspace/ges/data/trailer_400p.ogg"

audioFile = "file:///home/bmonkey/workspace/ges/data/prof.ogg"

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  video_layer = GES.Layer()
  audio_layer = GES.Layer()
  
  timeline.add_layer(video_layer)
  timeline.add_layer(audio_layer)

  video_asset = GES.UriClipAsset.request_sync(videoFile)
  #video_layer.add_asset(video_asset, 0, 0, 3 * Gst.SECOND, GES.TrackType.UNKNOWN)
  video_layer.add_asset(video_asset, 0, 0, 3 * Gst.SECOND, video_asset.get_supported_formats())

  audio_asset = GES.UriClipAsset.request_sync(audioFile)
  audio_layer.add_asset(audio_asset, 0, 0, timeline.get_duration(), GES.TrackType.AUDIO)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)
    
  mainLoop = GLib.MainLoop.new(None, False)
  GLib.timeout_add_seconds(3, quit, mainLoop)
  GLib.MainLoop().run()
  
simple()
