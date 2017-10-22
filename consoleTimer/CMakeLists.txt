cmake_minimum_required(VERSION 3.8)
project(time)

set(CMAKE_C_STANDARD 11)

set(SOURCE_FILES consoleTimer.c)
# set(CMAKE_CXX_FLAGS "-lncurses")
add_compile_options(-Wall)
add_executable(consoleTimer ${SOURCE_FILES})
TARGET_LINK_LIBRARIES(consoleTimer curses)
