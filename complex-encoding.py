#!/usr/bin/python

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal
import time

from GESEncoder import EncoderManager

from sys import stdout

videoFile1 = "file:///home/bmonkey/workspace/ges/data/trailer_480p.mov"
videoFile2 = "file:///home/bmonkey/workspace/ges/data/Sesame Street- Kermit and Joey Say the Alphabet.mp4"
videoFile3 = "file:///home/bmonkey/workspace/ges/data/BlenderFluid.webm"
videoFile4 = "file:///home/bmonkey/workspace/ges/data/Blender Physics Animation HD.flv"

musicFile = "file:///home/bmonkey/workspace/ges/data/prof.ogg"

imageFile1 = "file:///home/bmonkey/workspace/ges/data/LAMP_720_576.jpg"
imageFile2 = "file:///home/bmonkey/workspace/ges/data/wallpaper-1946968.jpg"
imageFile3 = "file:///home/bmonkey/workspace/ges/data/Fish.png"

outputFile = 'file:///home/bmonkey/workspace/ges/export/shakemGESEncode'

def handle_sigint(sig, frame):
  Gtk.main_quit()

def videoAudioTimeline():
  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.Layer()
  
  timeline.add_layer(layer)

  asset1 = GES.UriClipAsset.request_sync(videoFile1)
  asset2 = GES.UriClipAsset.request_sync(videoFile2)
  asset3 = GES.UriClipAsset.request_sync(videoFile3)
  asset4 = GES.UriClipAsset.request_sync(videoFile4)

  layer.add_asset(asset1, 0 * Gst.SECOND, 1 * Gst.SECOND, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset2, 10 * Gst.SECOND, 2 * Gst.SECOND, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset3, 20 * Gst.SECOND, 3 * Gst.SECOND, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset4, 30 * Gst.SECOND, 10 * Gst.SECOND, 30 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  
  return (pipeline, timeline.get_duration())

def videoTimeline():
  timeline = GES.Timeline.new_video()
  
  layer = GES.Layer()
  audiolayer = GES.Layer()
  
  timeline.add_layer(audiolayer)

  musicAsset = GES.UriClipAsset.request_sync(musicFile)
  
  timeline.add_layer(layer)

  asset1 = GES.UriClipAsset.request_sync(videoFile1)
  asset2 = GES.UriClipAsset.request_sync(videoFile2)
  asset3 = GES.UriClipAsset.request_sync(videoFile3)
  asset4 = GES.UriClipAsset.request_sync(videoFile4)

  layer.add_asset(asset1, 0 * Gst.SECOND, 1 * Gst.SECOND, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset2, 10 * Gst.SECOND, 2 * Gst.SECOND, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset3, 20 * Gst.SECOND, 3 * Gst.SECOND, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset4, 30 * Gst.SECOND, 10 * Gst.SECOND, 30 * Gst.SECOND, GES.TrackType.UNKNOWN)
  audiolayer.add_asset(musicAsset, 0, 0, timeline.get_duration(), GES.TrackType.AUDIO)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  
  return (pipeline, timeline.get_duration())

def complexTimeline():
  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.Layer()
  audiolayer = GES.Layer()
  imagelayer = GES.Layer()
  
  timeline.add_layer(layer)
  timeline.add_layer(audiolayer)
  timeline.add_layer(imagelayer)

  asset1 = GES.UriClipAsset.request_sync(videoFile1)
  asset2 = GES.UriClipAsset.request_sync(videoFile2)
  asset3 = GES.UriClipAsset.request_sync(videoFile3)
  asset4 = GES.UriClipAsset.request_sync(videoFile4)
  musicAsset = GES.UriClipAsset.request_sync(musicFile)
  
  imageasset1 = GES.UriClipAsset.request_sync(imageFile1)
  imageasset2 = GES.UriClipAsset.request_sync(imageFile2)
  imageasset3 = GES.UriClipAsset.request_sync(imageFile3)

  #layer.add_asset(imageasset1, 0 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset1, 0 * Gst.SECOND, 0, 11 * Gst.SECOND, GES.TrackType.UNKNOWN)
  imagelayer.add_asset(imageasset2, 10 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset2, 11 * Gst.SECOND, 0, 9 * Gst.SECOND, GES.TrackType.UNKNOWN)
  imagelayer.add_asset(imageasset3, 20 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset3, 21 * Gst.SECOND, 3 * Gst.SECOND, 9 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset4, 30 * Gst.SECOND, 10 * Gst.SECOND, 30 * Gst.SECOND, GES.TrackType.UNKNOWN)
  audiolayer.add_asset(musicAsset, 0, 0, timeline.get_duration(), GES.TrackType.AUDIO)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  
  return (pipeline, timeline.get_duration())

def imageTimeline():
  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.Layer()
  imagelayer = GES.Layer()
  
  timeline.add_layer(layer)
  timeline.add_layer(imagelayer)

  asset1 = GES.UriClipAsset.request_sync(videoFile1)
  
  imageasset1 = GES.UriClipAsset.request_sync(imageFile1)
  imageasset2 = GES.UriClipAsset.request_sync(imageFile2)
  imageasset3 = GES.UriClipAsset.request_sync(imageFile3)

  layer.add_asset(imageasset1, 0 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset1, 0 * Gst.SECOND, 0, 11 * Gst.SECOND, GES.TrackType.UNKNOWN)
  imagelayer.add_asset(imageasset2, 10 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  imagelayer.add_asset(imageasset3, 20 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  
  return (pipeline, timeline.get_duration())

if __name__ =="__main__":
  Gst.init(None)
  GES.init()
  
  em = EncoderManager()
  em.addJob("file:///home/bmonkey/workspace/ges/export/videoAudioTimeline", "matroska-h264-vorbis", videoAudioTimeline)
  
  em.addJob("file:///home/bmonkey/workspace/ges/export/videoTimeline", "matroska-h264-vorbis", videoTimeline)

  em.addJob("file:///home/bmonkey/workspace/ges/export/complexTimeline", "matroska-h264-vorbis", complexTimeline)

  
  em.encodeNext()
  
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
  
  
  
