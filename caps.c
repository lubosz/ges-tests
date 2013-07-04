#include <gst/gst.h>

void main() {
  gst_init();
  GstCaps * caps = gst_caps_new_empty_simple("video/x-vp8");
}

