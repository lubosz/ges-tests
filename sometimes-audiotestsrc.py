#!/usr/bin/python

from IPython import embed

from gi.repository import GES, Gst, GLib, Gtk, GstPbutils, GObject

import sys
import signal


videoFile = "file:///home/bmonkey/workspace/ges/data/trailer_480p.mov"

imageFile1 = "file:///home/bmonkey/workspace/ges/data/LAMP_720_576.jpg"
imageFile2 = "file:///home/bmonkey/workspace/ges/data/wallpaper-1946968.jpg"
imageFile3 = "file:///home/bmonkey/workspace/ges/data/Fish.png"

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

def quit(bar):
  GLib.MainLoop.quit(bar)
  exit()

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  #timeline = GES.Timeline()
  
  #videotrack = GES.VideoTrack.new()
  #timeline.add_track(videotrack)

  imagelayer = GES.Layer()
  videolayer = GES.Layer()
  
  #imagelayer.set_property("priority", 1)
  #videolayer.set_property("priority", 0)
  #g_object_set (layer2, "priority", 1, NULL);

  timeline.add_layer(imagelayer)
  timeline.add_layer(videolayer)

  asset = GES.UriClipAsset.request_sync(videoFile)
  
  imageasset1 = GES.UriClipAsset.request_sync(imageFile1)
  imageasset2 = GES.UriClipAsset.request_sync(imageFile2)
  imageasset3 = GES.UriClipAsset.request_sync(imageFile3)

  imagelayer.add_asset(imageasset1, 0 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.VIDEO)
  #imagelayer.add_asset(imageasset2, 6 * Gst.SECOND, 0, 2 * Gst.SECOND, GES.TrackType.VIDEO)
  #imagelayer.add_asset(imageasset3, 8 * Gst.SECOND, 0, 2 * Gst.SECOND, GES.TrackType.VIDEO)
  #videolayer.add_asset(asset, 1 * Gst.SECOND, 0, 10 * Gst.SECOND, GES.TrackType.VIDEO)
  
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
