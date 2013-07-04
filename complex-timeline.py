#!/usr/bin/python

from IPython import embed

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal

# File URL http://download.blender.org/peach/trailer/trailer_400p.ogg

videoFile1 = "file:///home/bmonkey/workspace/ges/data/trailer_480p.mov"

videoFile2 = "file:///home/bmonkey/workspace/ges/data/Sesame Street- Kermit and Joey Say the Alphabet.mp4"

videoFile3 = "file:///home/bmonkey/workspace/ges/data/BlenderFluid.webm"

videoFile4 = "file:///home/bmonkey/workspace/ges/data/Blender Physics Animation HD.flv"

musicFile = "file:///home/bmonkey/workspace/ges/data/prof.ogg"

imageFile1 = "file:///home/bmonkey/workspace/ges/data/LAMP_720_576.jpg"
imageFile2 = "file:///home/bmonkey/workspace/ges/data/wallpaper-1946968.jpg"
imageFile3 = "file:///home/bmonkey/workspace/ges/data/Fish.png"

outputFile = 'file:///home/bmonkey/workspace/ges/data/shakemGESEncode'

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
    #embed()
    return True

def encoderProfile(container, video, audio):
  container_profile = GstPbutils.EncodingContainerProfile.new(
    "pitivi-profile",
    "Pitivi encoding profile",
    Gst.Caps.new_empty_simple(container),
    None)
 
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

  return container_profile

def simple():
  Gst.init(None)
  GES.init()

  timeline = GES.Timeline.new_audio_video()
  
  layer = GES.Layer()
  audiolayer = GES.Layer()
  #imagelayer = GES.Layer()
  
  timeline.add_layer(layer)
  timeline.add_layer(audiolayer)
  #timeline.add_layer(imagelayer)

  asset1 = GES.UriClipAsset.request_sync(videoFile1)
  asset2 = GES.UriClipAsset.request_sync(videoFile2)
  asset3 = GES.UriClipAsset.request_sync(videoFile3)
  asset4 = GES.UriClipAsset.request_sync(videoFile4)
  musicAsset = GES.UriClipAsset.request_sync(musicFile)
  
  imageasset1 = GES.UriClipAsset.request_sync(imageFile1)
  imageasset2 = GES.UriClipAsset.request_sync(imageFile2)
  imageasset3 = GES.UriClipAsset.request_sync(imageFile3)

  layer.add_asset(imageasset1, 0 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset1, 1 * Gst.SECOND, 0, 9 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(imageasset2, 10 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset2, 11 * Gst.SECOND, 0, 9 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(imageasset3, 20 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset3, 21 * Gst.SECOND, 3 * Gst.SECOND, 9 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset4, 30 * Gst.SECOND, 10 * Gst.SECOND, 30 * Gst.SECOND, GES.TrackType.UNKNOWN)
  audiolayer.add_asset(musicAsset, 0, 0, timeline.get_duration(), GES.TrackType.AUDIO)
  
  timeline.commit()

  pipeline = GES.TimelinePipeline()
  pipeline.add_timeline(timeline)
  
  # Firefox
  #format = ["application/ogg", "video/x-theora", "audio/x-vorbis", "ogv"] # very slow after 20 secs, bugs

  # Chrome
  #format = ["video/webm", "video/x-vp8", "audio/x-vorbis", "webm"] # first element
  
  # Safari
  #format = ["video/quicktime", "video/x-h264", "audio/x-aac", "mp4"] #no start
  
  # MPEG
  #format = ["video/mpeg", "video/mpeg", "audio/mpeg", "mpg"] #no start
  
  # Works
  #format = ["video/x-matroska", "video/x-h264", "audio/x-vorbis", "mkv"]
  
  # mkv / mpeg
  #(GError('GStreamer error: negotiation problem.',), 'gstvideoencoder.c(1363): gst_video_encoder_chain (): /GESTimelinePipeline:gestimelinepipeline0/GstEncodeBin:internal-encodebin/avenc_mpeg1video:avenc_mpeg1video0:\nencoder not initialized')

  # works, slow after 20 secs, vorbis glitches
  #format = ["video/x-matroska", "video/x-theora", "audio/x-vorbis", "mkv"]
  
  # slow after 20 secs, stream kaputt, very big
  #format = ["video/x-matroska", "video/x-raw", "audio/x-vorbis", "mkv"]
  
  # slower after 20 secs, wrong positioning, output shaky
  #format = ["video/x-matroska", "video/x-dv", "audio/x-vorbis", "mkv"]
  
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
  
simple()
