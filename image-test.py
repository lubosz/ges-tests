#!/usr/bin/python

from IPython import embed

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import signal

videoFile1 = "file:///home/bmonkey/workspace/ges/data/trailer_480p.mov"
videoFile2 = "file:///home/bmonkey/workspace/ges/data/Sesame Street- Kermit and Joey Say the Alphabet.mp4"
videoFile3 = "file:///home/bmonkey/workspace/ges/data/BlenderFluid.webm"
videoFile4 = "file:///home/bmonkey/workspace/ges/data/Blender Physics Animation HD.flv"

imageFile1 = "file:///home/bmonkey/workspace/ges/data/gradient720x576.jpg"
imageFile2 = "file:///home/bmonkey/workspace/ges/data/gradient1280x576.jpg"
imageFile3 = "file:///home/bmonkey/workspace/ges/data/gradient720x720.jpg"
imageFile4 = "file:///home/bmonkey/workspace/ges/data/gradient1280x720.jpg"
imageFile5 = "file:///home/bmonkey/workspace/ges/data/gradient1920x1080.jpg"

outputFile = 'file:///home/bmonkey/workspace/ges/export/shakemGESimageTest'

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
  #audiolayer = GES.Layer()
  imagelayer = GES.Layer()
  
  timeline.add_layer(imagelayer)
  timeline.add_layer(layer)
  #timeline.add_layer(audiolayer)

  asset = GES.Asset.request(GES.TestClip, None)
  #musicAsset = GES.UriClipAsset.request_sync(musicFile)
  
  asset1 = GES.UriClipAsset.request_sync(videoFile1)
  asset2 = GES.UriClipAsset.request_sync(videoFile2)
  asset3 = GES.UriClipAsset.request_sync(videoFile3)
  asset4 = GES.UriClipAsset.request_sync(videoFile4)
  
  imageasset1 = GES.UriClipAsset.request_sync(imageFile1)
  imageasset2 = GES.UriClipAsset.request_sync(imageFile2)
  imageasset3 = GES.UriClipAsset.request_sync(imageFile3)
  imageasset4 = GES.UriClipAsset.request_sync(imageFile4)
  imageasset5 = GES.UriClipAsset.request_sync(imageFile5)
  
  #layer.add_asset(imageasset1, 0 * Gst.SECOND, 0, 1 * Gst.SECOND, GES.TrackType.UNKNOWN)
  layer.add_asset(asset4, 0 * Gst.SECOND, 0, 10  * Gst.SECOND, GES.TrackType.VIDEO)
  imagelayer.add_asset(imageasset5, 5 * Gst.SECOND, 10  * Gst.SECOND, 2 * Gst.SECOND, GES.TrackType.VIDEO)
  #layer.add_asset(asset2, 10 * Gst.SECOND, 0, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  #imagelayer.add_asset(imageasset3, 20 * Gst.SECOND, 0, 2 * Gst.SECOND, GES.TrackType.UNKNOWN)
  #layer.add_asset(asset3, 20 * Gst.SECOND, 5 * Gst.SECOND, 10 * Gst.SECOND, GES.TrackType.UNKNOWN)
  #layer.add_asset(asset4, 30 * Gst.SECOND, 10 * Gst.SECOND, 30 * Gst.SECOND, GES.TrackType.UNKNOWN)
  #audiolayer.add_asset(musicAsset, 0, 0, timeline.get_duration(), GES.TrackType.AUDIO)
  
  timeline.commit()

  pipeline = GES.Pipeline()
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
  format = ["video/x-matroska", "video/x-h264", "audio/x-vorbis", "mkv"]
  
  # mkv / mpeg
  #(GError('GStreamer error: negotiation problem.',), 'gstvideoencoder.c(1363): gst_video_encoder_chain (): /GESPipeline:gestimelinepipeline0/GstEncodeBin:internal-encodebin/avenc_mpeg1video:avenc_mpeg1video0:\nencoder not initialized')

  # works, slow after 20 secs, vorbis glitches
  #format = ["video/x-matroska", "video/x-theora", "audio/x-vorbis", "mkv"]
  
  # slow after 20 secs, stream kaputt, very big
  #format = ["video/x-matroska", "video/x-raw", "audio/x-vorbis", "mkv"]
  
  # slower after 20 secs, wrong positioning, output shaky
  #format = ["video/x-matroska", "video/x-dv", "audio/x-vorbis", "mkv"]
  
  container_profile = encoderProfile(format[0], format[1], format[2])
  
  pipeline.set_render_settings(outputFile + "." + format[3], container_profile)
  #pipeline.set_mode(GES.PipelineFlags.RENDER)
  pipeline.set_state(Gst.State.PLAYING)
  
  bus = pipeline.get_bus()
  bus.add_signal_watch()
  bus.connect("message", busMessageCb)
  GObject.timeout_add(1000, duration_querier, pipeline)
 
  signal.signal(signal.SIGINT, handle_sigint)
  Gtk.main()
  
simple()
