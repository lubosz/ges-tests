#!/usr/bin/python
from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal

from IPython import embed

outputFile = 'file:///home/bmonkey/workspace/ges/export/aacTest'

def handle_sigint(sig, frame):
    Gtk.main_quit()
 
def busMessageCb(bus, message):
    if message.type == Gst.MessageType.EOS:
        print("eos")
        Gtk.main_quit()
    elif message.type == Gst.MessageType.ERROR:
        print (message.parse_error())
 
def duration_querier(pipeline):
    print(pipeline.query_position(Gst.Format.TIME)[1] / Gst.SECOND)
    return True

def encoderProfile(container, video, audio):
  #embed()

  container_profile = GstPbutils.EncodingContainerProfile.new(
    "aac",
    "AAC Encoding Profile",
    Gst.Caps.new_empty_simple(container),
    None)
    
  #embed()
    
  print (container_profile)
 
  print (container_profile.get_profiles())
 
  video_profile = GstPbutils.EncodingVideoProfile.new(
    Gst.Caps.new_empty_simple(video),
    None,
    Gst.Caps.new_empty_simple("video/x-raw"),
    0)
  container_profile.add_profile(video_profile)
 
  audio_profile = GstPbutils.EncodingAudioProfile.new(
    Gst.Caps.new_empty_simple(audio),
    None,
    Gst.Caps.new_empty_simple("audio/x-raw"),
    0)
  container_profile.add_profile(audio_profile)
  
  #embed()

  return container_profile
  
if __name__ =="__main__":
  Gst.init(None)
  GES.init()
  
  timeline = GES.Timeline()
  track = GES.VideoTrack.new()
  timeline.add_track(track)
  layer = GES.Layer()
  timeline.add_layer(layer)
  asset = GES.Asset.request(GES.TestClip, None)
  
  layer.add_asset(asset, 0 * Gst.SECOND, 0, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  timeline.commit()

  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)
  # does not start, no error
  format = ["video/x-matroska", "video/x-h264", "audio/aac", "mov"]
  
  # Works
  #format = ["video/x-matroska", "video/x-h264", "audio/x-vorbis", "mkv"]
  
  container_profile = encoderProfile(format[0], format[1], format[2])
  #disc = GstPbutils.Discoverer()
  #info = disc.discover_uri("file:///home/bmonkey/workspace/ges/data/trailer_480p.mov")
  #container_profile = GstPbutils.EncodingProfile.from_discoverer(info)

  pipeline.set_render_settings(outputFile + "." + format[3], container_profile)
  pipeline.set_mode(GES.PipelineFlags.RENDER)
  pipeline.set_state(Gst.State.PLAYING)
  
  bus = pipeline.get_bus()
  bus.add_signal_watch()
  bus.connect("message", busMessageCb)
  GObject.timeout_add(300, duration_querier, pipeline)
 
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
