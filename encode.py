#!/usr/bin/python2

from gi.repository import GstPbutils
from gi.repository import Gtk
from gi.repository import Gst
from gi.repository import GES
from gi.repository import GObject
 
import sys
import signal
 
def handle_sigint(sig, frame):
    Gtk.main_quit()
 
def busMessageCb(unused_bus, message):
    if message.type == Gst.MessageType.EOS:
        print("eos")
        Gtk.main_quit()
 
def duration_querier(pipeline):
    print(pipeline.query_position(Gst.Format.TIME))
    return True
 
def mylog(x):
    return (x / (1 + x))
 
def createLayers(timeline, asset):
    alpha = 1.0
    for i in range(int(sys.argv[2])):
        layer = timeline.append_layer()
        clip = layer.add_asset(asset, i * Gst.SECOND * 0.3, 0, asset.get_duration(), GES.TrackType.UNKNOWN)
        for source in clip.get_children():
            if source.props.track_type == GES.TrackType.VIDEO:
                break
 
        source.set_child_property("alpha", alpha)
        alpha = mylog(alpha)
 
if __name__ =="__main__":
    if len(sys.argv) < 4:
        print("usage : " + sys.argv[0] + " file:///video/uri number_of_layers file:///audio/uri [file:///output_uri]")
        print("If you specify a output uri, the pipeline will get rendered")
        exit(0)
 
    GObject.threads_init()
    Gst.init(None)
    GES.init()
 
    timeline = GES.Timeline.new_audio_video()
 
    asset = GES.UriClipAsset.request_sync(sys.argv[1])
    audio_asset = GES.UriClipAsset.request_sync(sys.argv[3])
 
    createLayers(timeline, asset)
 
    layer = timeline.append_layer()
 
    layer.add_asset(audio_asset, 0, 0, timeline.get_duration(), GES.TrackType.AUDIO)
 
    pipeline = GES.TimelinePipeline()
    pipeline.add_timeline(timeline)
 
    container_profile = \
        GstPbutils.EncodingContainerProfile.new("pitivi-profile",
                                                "Pitivi encoding profile",
                                                Gst.Caps.new_empty_simple("video/webm"),
                                                None)
 
    video_profile = GstPbutils.EncodingVideoProfile.new(Gst.Caps.new_empty_simple("video/x-vp8"),
                                                        None,
                                                        Gst.Caps.new_empty_simple("video/x-raw"),
                                                        0)
 
    container_profile.add_profile(video_profile)
 
    audio_profile = GstPbutils.EncodingAudioProfile.new(Gst.Caps.new_empty_simple("audio/x-vorbis"),
                                                        None,
                                                        Gst.Caps.new_empty_simple("audio/x-raw"),
                                                        0)
 
    container_profile.add_profile(audio_profile)
 
    if len(sys.argv) > 4:
        print ("render settings", sys.argv[4])
        pipeline.set_render_settings(sys.argv[4], container_profile)
        pipeline.set_mode(GES.PipelineFlags.RENDER)
 
    pipeline.set_state(Gst.State.PLAYING)
 
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", busMessageCb)
    GObject.timeout_add(300, duration_querier, pipeline)
 
    signal.signal(signal.SIGINT, handle_sigint)
    Gtk.main()
