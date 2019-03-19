cmake_minimum_required(VERSION 2.8)

find_package(Boost REQUIRED COMPONENTS system iostreams filesystem)

# compiler flag
set(CMAKE_CXX_FLAGS "-std=c++0x -o3")

link_directories ( ${Boost_LIBRARY_DIRS} )
include_directories ( ${Boost_INCLUDE_DIRS} )

add_executable(cascade cascade.cpp)
target_link_libraries(cascade ${Boost_LIBRARIES})

