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
include CMakeFiles/key.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/key.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/key.dir/flags.make

CMakeFiles/key.dir/keys.cpp.obj: CMakeFiles/key.dir/flags.make
CMakeFiles/key.dir/keys.cpp.obj: CMakeFiles/key.dir/includes_CXX.rsp
CMakeFiles/key.dir/keys.cpp.obj: ../keys.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=C:\Users\Xavier\monero\scripts\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/key.dir/keys.cpp.obj"
	C:\MinGW\bin\g++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\key.dir\keys.cpp.obj -c C:\Users\Xavier\monero\scripts\keys.cpp

CMakeFiles/key.dir/keys.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/key.dir/keys.cpp.i"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E C:\Users\Xavier\monero\scripts\keys.cpp > CMakeFiles\key.dir\keys.cpp.i

CMakeFiles/key.dir/keys.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/key.dir/keys.cpp.s"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S C:\Users\Xavier\monero\scripts\keys.cpp -o CMakeFiles\key.dir\keys.cpp.s

# Object files for target key
key_OBJECTS = \
"CMakeFiles/key.dir/keys.cpp.obj"

# External object files for target key
key_EXTERNAL_OBJECTS =

key.exe: CMakeFiles/key.dir/keys.cpp.obj
key.exe: CMakeFiles/key.dir/build.make
key.exe: C:/MinGW/lib/libboost_system.a
key.exe: C:/MinGW/lib/libboost_iostreams.a
key.exe: C:/MinGW/lib/libboost_filesystem.a
key.exe: C:/MinGW/lib/libboost_regex.a
key.exe: CMakeFiles/key.dir/linklibs.rsp
key.exe: CMakeFiles/key.dir/objects1.rsp
key.exe: CMakeFiles/key.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=C:\Users\Xavier\monero\scripts\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable key.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\key.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/key.dir/build: key.exe

.PHONY : CMakeFiles/key.dir/build

CMakeFiles/key.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\key.dir\cmake_clean.cmake
.PHONY : CMakeFiles/key.dir/clean

CMakeFiles/key.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" C:\Users\Xavier\monero\scripts C:\Users\Xavier\monero\scripts C:\Users\Xavier\monero\scripts\build C:\Users\Xavier\monero\scripts\build C:\Users\Xavier\monero\scripts\build\CMakeFiles\key.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/key.dir/depend
