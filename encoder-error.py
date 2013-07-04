#!/usr/bin/python

from IPython import embed
from gi.repository import GES, Gst, GLib, Gtk, GstPbutils, GObject

import signal

videoFile1 = "file:///home/bmonkey/workspace/ges/data/trailer_480p.mov"
videoFile2 = "file:///home/bmonkey/workspace/ges/data/sintel_trailer-480p.mp4"

outputFile = 'file:///home/bmonkey/workspace/ges/data/GESEncode.webm'

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
  
  layer = GES.Layer()
  
  timeline.add_layer(layer)

  asset = GES.UriClipAsset.request_sync(videoFile1)
  asset2 = GES.UriClipAsset.request_sync(videoFile2)

  layer.add_asset(asset, 0 * Gst.SECOND, 0, 3 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset2, 3 * Gst.SECOND, 0, 3 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  
  #encoding
  container_profile = GstPbutils.EncodingContainerProfile.new(
      "pitivi-profile",
      "Pitivi encoding profile",
      Gst.Caps.new_empty_simple("video/x-matroska"),
      None)
 
  video_profile = GstPbutils.EncodingVideoProfile.new(
      Gst.Caps.new_empty_simple("video/x-h264"),
      None,
      Gst.Caps.new_empty_simple("video/x-raw"),
      0)
 
  container_profile.add_profile(video_profile)
 
  audio_profile = GstPbutils.EncodingAudioProfile.new(
      Gst.Caps.new_empty_simple("audio/x-vorbis"),
      None,
      Gst.Caps.new_empty_simple("audio/x-raw"),
      0)
 
  container_profile.add_profile(audio_profile)

  pipeline.set_render_settings(outputFile, container_profile)
  pipeline.set_mode(GES.PipelineFlags.RENDER)
  pipeline.set_state(Gst.State.PLAYING)
  
  bus = pipeline.get_bus()
  bus.add_signal_watch()
  bus.connect("message", busMessageCb)
  GObject.timeout_add(1000, duration_querier, pipeline)
 
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
  
simple()
