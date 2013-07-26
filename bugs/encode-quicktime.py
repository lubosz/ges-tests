#!/usr/bin/python
from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal

outputFile = 'file:///home/bmonkey/workspace/ges/export/quickTimeTest'

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

  cont_caps = Gst.Caps.from_string(container)

  container_profile = GstPbutils.EncodingContainerProfile.new(
    "quicktime",
    "QuickTime Encoding Profile",
    cont_caps,
    None)
 
  video_profile = GstPbutils.EncodingVideoProfile.new(
    Gst.Caps.from_string(video),
    None,
    Gst.Caps.from_string("video/x-raw"),
    0)
  container_profile.add_profile(video_profile)
 
  audio_profile = GstPbutils.EncodingAudioProfile.new(
    Gst.Caps.from_string(audio),
    None,
    Gst.Caps.from_string("audio/x-raw"),
    0)
  container_profile.add_profile(audio_profile)

  return container_profile
  
if __name__ =="__main__":
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  layer = GES.Layer()
  timeline.add_layer(layer)
  asset = GES.Asset.request(GES.TestClip, None)
  
  layer.add_asset(asset, 0 * Gst.SECOND, 0, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  timeline.commit()

  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)
  
  #dudio/mpeg mpegversion: 4 stream-format: raw 
  
  format = ["video/quicktime,variant=iso", "video/x-h264", "audio/mpeg,mpegversion=4,stream-format=raw", "mov"]
  
  container_profile = encoderProfile(format[0], format[1], format[2])
  
  pipeline.set_render_settings(outputFile + "." + format[3], container_profile)
  pipeline.set_mode(GES.PipelineFlags.RENDER)
  pipeline.set_state(Gst.State.PLAYING)
  
  bus = pipeline.get_bus()
  bus.add_signal_watch()
  bus.connect("message", busMessageCb)
  GObject.timeout_add(300, duration_querier, pipeline)
 
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
