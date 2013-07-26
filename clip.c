#include <gst/gst.h>
#include <ges/ges.h>

// File URL http://download.blender.org/peach/trailer/trailer_400p.ogg

GESTimeline * no_window() {
  // no window is openened at all
  GError **error = NULL;
  GESProject *project;
  GESTimeline *timeline;
  project = ges_project_new(NULL);
  timeline = GES_TIMELINE(ges_asset_extract (GES_ASSET (project), error));
  return timeline;
}

GESTimeline * does_not_play_often() {
  // the video stops at its inpoint in 9/10 times. in 1/10 it works with sound
  // prints this warning:
  // CRITICAL **: ges_project_add_asset: assertion `GES_IS_PROJECT (project)' failed
  
  GESTimeline *timeline;
  GESTrack *track_video, *track_audio;
  timeline = ges_timeline_new();
  
  track_video = ges_video_track_new();
  track_audio = ges_audio_track_new();
  
  ges_timeline_add_track(timeline, track_video);
  ges_timeline_add_track(timeline, track_audio);
  
  return timeline;
}

GESTimeline * no_audio() {
  // works, there is a warning though
  // CRITICAL **: ges_project_add_asset: assertion `GES_IS_PROJECT (project)' failed
  
  GESTimeline *timeline;
  GESTrack *track_video;
  timeline = ges_timeline_new();
  
  track_video = ges_video_track_new();
  
  ges_timeline_add_track(timeline, track_video);
  
  return timeline;
}

void main() {
  GMainLoop *mainloop;
  GESLayer *layer;

  GESPipeline *timeline_pipeline;
  GESTimeline *timeline;
  GESUriClip *clip;

  gchar *uri = "file:///home/bmonkey/workspace/ges/data/trailer_400p.ogg";

  gst_init (NULL, NULL);
  ges_init ();

  timeline = does_not_play_often();
  //timeline = no_window();
  //timeline = no_audio();

  timeline_pipeline = ges_timeline_pipeline_new();
  layer = ges_layer_new();

  ges_timeline_add_layer (timeline, layer);
  ges_timeline_pipeline_add_timeline (timeline_pipeline, timeline);
  
  clip = ges_uri_clip_new(uri);
  
  g_object_set (clip, 
    "start", (guint64) 0, 
    "duration", (guint64) 3000000000,
    "in-point", (guint64) 0, NULL);
    
  ges_layer_add_clip (layer, GES_CLIP (clip));
  
  gst_element_set_state (timeline_pipeline, GST_STATE_PLAYING);
  
  mainloop = g_main_loop_new (NULL, FALSE);
  g_timeout_add_seconds (3, (GSourceFunc) g_main_loop_quit, mainloop);

  g_main_loop_run (mainloop);

  g_main_loop_unref (mainloop);
}
