#include <ges/ges.h>

  GMainLoop *mainloop;
  GESLayer *layer;
  GESProject *project;
  GESTimelinePipeline *timeline_pipeline;
  GESTimeline *timeline;
  GESUriClip *clip;
  GError **error = NULL;
  gchar *uri = ges_test_file_uri ("trailer_400p.ogg");

  gst_init (NULL, NULL);
  ges_init ();

  project = ges_project_new(NULL);
  timeline = GES_TIMELINE(ges_asset_extract (GES_ASSET (project), error));
  timeline_pipeline = ges_timeline_pipeline_new();
  layer = ges_layer_new();

  ges_timeline_add_layer (timeline, layer);
  ges_timeline_pipeline_add_timeline (timeline_pipeline, timeline);
  
  clip = ges_uri_clip_new(uri);
  
  g_object_set (clip, 
    "start", (guint64) 0, 
    "duration", (guint64) 2000000000,
    "in-point", (guint64) 0, NULL);
    
  ges_layer_add_clip (layer, GES_CLIP (clip));
  
  gst_element_set_state (GST_ELEMENT (timeline_pipeline), GST_STATE_PLAYING);
  
  mainloop = g_main_loop_new (NULL, FALSE);
  g_timeout_add_seconds (4, (GSourceFunc) g_main_loop_quit, mainloop);

  g_main_loop_run (mainloop);

  g_main_loop_unref (mainloop);
