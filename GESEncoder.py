from gi.repository import GES, Gst, Gtk, GstPbutils, GObject

import time

from sys import stdout

class Timer:
  def __init__(self):
    self.start = time.time()
    self.end = 0
  
  def stop(self):
    self.end = time.time()

  def duration(self):
    return self.end - self.start

    
class VideoFormat:
  def __init__(self, container, video, audio, suffix):
    self.container = container
    self.video = video
    self.audio = audio
    self.suffix = suffix
  
  def encoderProfile(self):
    container_profile = GstPbutils.EncodingContainerProfile.new(
      "pitivi-profile",
      "Pitivi encoding profile",
      Gst.Caps.new_empty_simple(self.container),
      None)
   
    video_profile = GstPbutils.EncodingVideoProfile.new(
      Gst.Caps.new_empty_simple(self.video),
      None,
      Gst.Caps.new_empty_simple("video/x-raw"),
      0)
    container_profile.add_profile(video_profile)
   
    audio_profile = GstPbutils.EncodingAudioProfile.new(
      Gst.Caps.new_empty_simple(self.audio),
      None,
      Gst.Caps.new_empty_simple("audio/x-raw"),
      0)
    container_profile.add_profile(audio_profile)

    return container_profile
  
  def print(self):
    print ("Container: %s (%s)\nVideo: %s\nAudio: %s" % (self.suffix, self.container, self.video, self.audio))

class Encoder:
    def __init__(self, em, destination, preset, pipeline, duration):
      self.formats = {
        "firefox" : VideoFormat("application/ogg", "video/x-theora", "audio/x-vorbis", "ogv"),
        "chrome" : VideoFormat("video/webm", "video/x-vp8", "audio/x-vorbis", "webm"),
        "safari" : VideoFormat("video/mp4", "video/x-h264", "audio/x-aac", "mp4"),
        "quicktime" : VideoFormat("video/quicktime", "video/x-h264", "audio/x-vorbis", "mov"),
        "mpeg" : VideoFormat("video/mpeg", "video/mpeg", "audio/mpeg", "mpg"),
        "matroska-vp8-vorbis" : VideoFormat("video/x-matroska", "video/x-vp8", "audio/x-vorbis", "mkv"),
        "matroska-h264-vorbis" : VideoFormat("video/x-matroska", "video/x-h264", "audio/x-vorbis", "mkv") 
      }
      
      self.em = em
      self.preset = preset
      self.renderTime = 0
      self.format = self.formats[preset]
      self.done = False
      self.destination = destination
      self.duration = duration
      self.pipeline = pipeline
      
    def busMessageCb(self, bus, message):
        if self.done:
          return
        if message.type == Gst.MessageType.EOS:
            self.done = True
            GObject.source_remove(self.timer)
            self.renderTime.stop()
            print("\n=")
            print("Rendering of %s took %.2f secs" % (self.preset, self.renderTime.duration()))
            print("=")
            self.format.print()
            print("=")
            self.pipeline.set_state(Gst.State.NULL)
            self.em.encodeNext()
        elif message.type == Gst.MessageType.ERROR:
            print (message.parse_error())
        else:
            pass
     
    def durationQuerier(self):
        curTime = self.pipeline.query_position(Gst.Format.TIME)[1]
        progress = "\r%s: %.2f%%\t%.2f/%.2f secs" % (
            self.preset, 
            curTime / self.duration * 100, 
            curTime / Gst.SECOND, 
            self.duration / Gst.SECOND)
        stdout.write(progress)
        stdout.flush()
        return True

      
    def encode(self):
      self.pipeline.set_render_settings(
        self.destination + "." + self.format.suffix, 
        self.format.encoderProfile())
    
      self.pipeline.set_mode(GES.PipelineFlags.RENDER)
      self.pipeline.set_state(Gst.State.PLAYING)
      
      self.renderTime = Timer()
      bus = self.pipeline.get_bus()
      bus.add_signal_watch()
      bus.connect("message", self.busMessageCb)
      self.timer = GObject.timeout_add(500, self.durationQuerier)

class EncoderManager:

  def __init__(self):
    self.renderJobs = []

  def encodeNext(self):
    for job in self.renderJobs:
      if not job.done:
        job.encode()
        return
    Gtk.main_quit()

  def addJob(self, outputFile, preset, pipeline_func):
    pipeline, duration = pipeline_func()
    self.renderJobs.append(Encoder(self, outputFile, preset, pipeline, duration))
