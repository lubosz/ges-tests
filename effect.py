#!/usr/bin/python

from IPython import embed

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal

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
  
  #asset = GES.UriClipAsset.request_sync(videoFile1)
  
  asset = GES.Asset.request(GES.TestClip, None)
  
  #src = GES.TestClip()
  #asset.set_property("pattern", GES.VideoTestPattern.SMPTE75)
  #src.set_property("duration", 5 * Gst.SECOND)
  #src.set_property("in-point", 5 * Gst.SECOND)
  #src.set_property("supported-formats", GES.TrackType.VIDEO)
  
  #effect = GES.Effect.new("videobalance")

  # this works
  #effect = GES.Effect.new("videobalance hue=0.5")

  #effect = GES.Effect.new("agingtv")
  #effect = GES.Effect.new("videobalance saturation=1.5 hue=+0.5")
  effect = GES.Effect.new("frei0r-filter-scale0tilt")
  #embed()
    
  clip = layer.add_asset(asset, 0 * Gst.SECOND, 0  * Gst.SECOND, 2  * Gst.SECOND, GES.TrackType.VIDEO)
  
  clip.add(effect)
  clip.set_property("vpattern", GES.VideoTestPattern.SMPTE75)

  timeline.commit()

  print(effect.list_children_properties())
  effect.set_child_property("tilt-x", 0.8)

  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)
  pipeline.set_state(Gst.State.PLAYING)
  
  bus = pipeline.get_bus()
  bus.add_signal_watch()
  bus.connect("message", busMessageCb)
  GObject.timeout_add(1000, duration_querier, pipeline)
 
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
  
simple()
