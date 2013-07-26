#!/usr/bin/python

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal

#http://download.blender.org/peach/trailer/trailer_400p.ogg
videoFile = "file:///home/bmonkey/workspace/ges/data/trailer_400p.ogg"

#https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png
imageFile = "file:///home/bmonkey/workspace/ges/data/PNG_transparency_demonstration_1.png"

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
  
  imagelayer = GES.Layer()
  videolayer = GES.Layer()
  timeline.add_layer(imagelayer)
  timeline.add_layer(videolayer)

  asset = GES.UriClipAsset.request_sync(videoFile)
  imageasset = GES.UriClipAsset.request_sync(imageFile)

  imagelayer.add_asset(imageasset, 1 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  videolayer.add_asset(asset, 0 * Gst.SECOND, 0, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  timeline.commit()

  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)

  pipeline.set_state(Gst.State.PLAYING)

  bus = pipeline.get_bus()
  bus.add_signal_watch()
  bus.connect("message", busMessageCb)
  GObject.timeout_add(300, duration_querier, pipeline)
 
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
  
simple()
