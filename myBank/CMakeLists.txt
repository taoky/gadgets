cmake_minimum_required(VERSION 3.8)
project(myBank)

set(CMAKE_C_STANDARD 11)

add_compile_options(-Wall)

set(SOURCE_FILES main.c link.c link.h interface.c interface.h main.h)
add_executable(myBank ${SOURCE_FILES})