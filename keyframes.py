#!/usr/bin/env python

import sys
import optparse

from gi.repository import GES, Gst, Gtk, GstPbutils, GObject, GLib, GstController

from IPython import embed

GObject.threads_init()

class KeyFrame:
    def __init__(self, property, time, value):
        self.property = property
        self.time = time
        self.value = value

class Effect:
    def __init__(self, effects):
        Gst.init(None)
        GES.init()
        self.mainloop = GLib.MainLoop()
        self._effects = []

        self.timeline = GES.Timeline.new_audio_video()
        #layer = GES.Layer()
        layer = GES.SimpleLayer.new()
        
        """
        #self.src = GES.TimelineTestSource()
        self.src = GES.VideoTestSource()
        self.src.set_start(0)

        self.src.set_duration(3 * Gst.SECOND)
        self.src.set_pattern(GES.VideoTestPattern.SMPTE75)
        #layer.add_object(self.src, 0)
        #layer.add_asset(self.src, 0, 0, 3 * Gst.SECOND, GES.TrackType.VIDEO)
        """
        
        self.src = GES.TestClip()
        self.src.set_property("vpattern", GES.VideoTestPattern.SMPTE)
        self.src.set_property("duration", 5 * Gst.SECOND)
        layer.add_clip(self.src)
        
        self.timeline.add_layer(layer)
        
        effect = GES.Effect.new("videobalance hue=-1")
        self.src.add(effect)

        """
        self.add_effects(effects)

        element = self.get_element_from_effect(self._effects[0], "videobalance")
        #embed()
        #self.controller = Gst.Controller(element, "hue")
        #self.controller = Gst.InterpolationControlSource(element, "hue")
        #self.controller = GstController.InterpolationControlSource.new(element, "hue")
        self.controller = GstController.InterpolationControlSource.new()
        self.controller.set_property("mode", GstController.InterpolationMode.CUBIC)
        #self.controller.set_interpolation_mode("hue", Gst.InterpolationMode.CUBIC)
        #self.controller.set("hue", 0, -1.0)
        self.controller.set(0, -1.0)
        #self.controller.set("hue", 3000000000, 1.0)
        self.controller.set(3 * Gst.SECOND, 1.0)
        """
        self.timeline.commit()
        
        self.pipeline = GES.Pipeline()
        self.pipeline.add_timeline(self.timeline)
        bus = self.pipeline.get_bus()
        bus.set_sync_handler(self.bus_handler, None)

    def add_effects(self, effects):
        for e in effects:
            print("effect:", e)
            #effect = GES.TrackParseLaunchEffect(e)
            effect = GES.Effect.new(e)
            self.src.add(effect)
            #self.src.add_track_object(effect)
            for track in self.timeline.get_tracks():
                print("trackcaps", track.get_caps().to_string())
                if track.get_caps().to_string() == "video/x-raw":
                    print("setting effect: " + e)
                    track.add_element(effect)
                    self._effects.append(effect)

    def get_element_from_effect(self, effect, name):
        for element in effect.get_element().children:
              if name in element.get_name():
                  print("found %s\n" % element.get_name())
                  return element

    def bus_handler(self, unused_bus, message, foo):
        if message.type == Gst.MessageType.ERROR:
            print("ERROR")
            self.mainloop.quit()
        elif message.type == Gst.MessageType.EOS:
            print("Done")
            self.mainloop.quit()

        #return Gst.BUS_PASS

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        #if (self.pipeline.set_state(Gst.State.PLAYING) == \
        #        Gst.State.CHANGE_FAILURE):
        #    print("Couldn't start pipeline")

        self.mainloop.run()

def main(args):
    usage = "usage: %s effect_name-1 .. effect_name-n\n" % args[0]

    if len(args) < 2:
        print(usage + "using aging tv as a default instead")
        args.append("videobalance")

    parser = optparse.OptionParser (usage=usage)
    (opts, args) = parser.parse_args ()

    effect = Effect(args)
    effect.run()

if __name__ == "__main__":
    main(sys.argv)
