#!/usr/bin/python

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal
import time

from GESEncoder import EncoderManager

from sys import stdout

videoFile = "file:///home/bmonkey/workspace/ges/data/trailer_400p.ogg"
musicFile = "file:///home/bmonkey/workspace/ges/data/02_Oliver_Huntemann_-_Rikarda.flac"
outputFile = 'file:///home/bmonkey/workspace/ges/export/gesEncode'

def handle_sigint(sig, frame):
  Gtk.main_quit()

def shortPipeLine():
  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.Layer()
  audiolayer = GES.Layer()
  
  timeline.add_layer(layer)
  timeline.add_layer(audiolayer)

  asset = GES.UriClipAsset.request_sync(videoFile)
  musicAsset = GES.UriClipAsset.request_sync(musicFile)
  
  layer.add_asset(asset, 0 * Gst.SECOND, 0, 30 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset, 30 * Gst.SECOND, 0, 30 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  audiolayer.add_asset(musicAsset, 0, 0, timeline.get_duration(), GES.TrackType.AUDIO)
  
  timeline.commit()

  pipeline = GES.Pipeline()
  pipeline.add_timeline(timeline)
  
  return (pipeline, timeline.get_duration())

if __name__ =="__main__":
  Gst.init(None)
  GES.init()
  
  em = EncoderManager()
  em.addJob(outputFile, "firefox", shortPipeLine)
  #em.addJob("chrome")
  #em.addJob("safari")
  #em.addJob("mpeg")
  em.addJob(outputFile, "matroska-h264-vorbis", shortPipeLine)
  em.encodeNext()
  
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
  
  
  
