# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.14

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "C:\Program Files\CMake\bin\cmake.exe"

# The command to remove a file.
RM = "C:\Program Files\CMake\bin\cmake.exe" -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = C:\Users\Xavier\monero\scripts

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = C:\Users\Xavier\monero\scripts\build

# Include any dependencies generated for this target.
include CMakeFiles/reduce.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/reduce.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/reduce.dir/flags.make

CMakeFiles/reduce.dir/reduce.cpp.obj: CMakeFiles/reduce.dir/flags.make
CMakeFiles/reduce.dir/reduce.cpp.obj: CMakeFiles/reduce.dir/includes_CXX.rsp
CMakeFiles/reduce.dir/reduce.cpp.obj: ../reduce.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=C:\Users\Xavier\monero\scripts\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/reduce.dir/reduce.cpp.obj"
	C:\MinGW\bin\g++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\reduce.dir\reduce.cpp.obj -c C:\Users\Xavier\monero\scripts\reduce.cpp

CMakeFiles/reduce.dir/reduce.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/reduce.dir/reduce.cpp.i"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E C:\Users\Xavier\monero\scripts\reduce.cpp > CMakeFiles\reduce.dir\reduce.cpp.i

CMakeFiles/reduce.dir/reduce.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/reduce.dir/reduce.cpp.s"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S C:\Users\Xavier\monero\scripts\reduce.cpp -o CMakeFiles\reduce.dir\reduce.cpp.s

# Object files for target reduce
reduce_OBJECTS = \
"CMakeFiles/reduce.dir/reduce.cpp.obj"

# External object files for target reduce
reduce_EXTERNAL_OBJECTS =

reduce.exe: CMakeFiles/reduce.dir/reduce.cpp.obj
reduce.exe: CMakeFiles/reduce.dir/build.make
reduce.exe: C:/MinGW/lib/libboost_system.a
reduce.exe: C:/MinGW/lib/libboost_iostreams.a
reduce.exe: C:/MinGW/lib/libboost_filesystem.a
reduce.exe: C:/MinGW/lib/libboost_regex.a
reduce.exe: CMakeFiles/reduce.dir/linklibs.rsp
reduce.exe: CMakeFiles/reduce.dir/objects1.rsp
reduce.exe: CMakeFiles/reduce.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=C:\Users\Xavier\monero\scripts\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable reduce.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\reduce.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/reduce.dir/build: reduce.exe

.PHONY : CMakeFiles/reduce.dir/build

CMakeFiles/reduce.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\reduce.dir\cmake_clean.cmake
.PHONY : CMakeFiles/reduce.dir/clean

CMakeFiles/reduce.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" C:\Users\Xavier\monero\scripts C:\Users\Xavier\monero\scripts C:\Users\Xavier\monero\scripts\build C:\Users\Xavier\monero\scripts\build C:\Users\Xavier\monero\scripts\build\CMakeFiles\reduce.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/reduce.dir/depend
