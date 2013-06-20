cmake_minimum_required(VERSION 2.8)

set(CMAKE_C_FLAGS "-std=c99") 

include_directories(
  /usr/include/gstreamer-1.0
  /usr/include/glib-2.0
  /usr/lib/glib-2.0/include/
)
add_executable(clip clip.c)
