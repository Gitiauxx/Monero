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
include CMakeFiles/keys.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/keys.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/keys.dir/flags.make

CMakeFiles/keys.dir/keys.cpp.obj: CMakeFiles/keys.dir/flags.make
CMakeFiles/keys.dir/keys.cpp.obj: CMakeFiles/keys.dir/includes_CXX.rsp
CMakeFiles/keys.dir/keys.cpp.obj: ../keys.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=C:\Users\Xavier\monero\scripts\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/keys.dir/keys.cpp.obj"
	C:\MinGW\bin\g++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\keys.dir\keys.cpp.obj -c C:\Users\Xavier\monero\scripts\keys.cpp

CMakeFiles/keys.dir/keys.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/keys.dir/keys.cpp.i"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E C:\Users\Xavier\monero\scripts\keys.cpp > CMakeFiles\keys.dir\keys.cpp.i

CMakeFiles/keys.dir/keys.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/keys.dir/keys.cpp.s"
	C:\MinGW\bin\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S C:\Users\Xavier\monero\scripts\keys.cpp -o CMakeFiles\keys.dir\keys.cpp.s

# Object files for target keys
keys_OBJECTS = \
"CMakeFiles/keys.dir/keys.cpp.obj"

# External object files for target keys
keys_EXTERNAL_OBJECTS =

keys.exe: CMakeFiles/keys.dir/keys.cpp.obj
keys.exe: CMakeFiles/keys.dir/build.make
keys.exe: C:/MinGW/lib/libboost_system.a
keys.exe: C:/MinGW/lib/libboost_iostreams.a
keys.exe: C:/MinGW/lib/libboost_filesystem.a
keys.exe: C:/MinGW/lib/libboost_regex.a
keys.exe: CMakeFiles/keys.dir/linklibs.rsp
keys.exe: CMakeFiles/keys.dir/objects1.rsp
keys.exe: CMakeFiles/keys.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=C:\Users\Xavier\monero\scripts\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable keys.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\keys.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/keys.dir/build: keys.exe

.PHONY : CMakeFiles/keys.dir/build

CMakeFiles/keys.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\keys.dir\cmake_clean.cmake
.PHONY : CMakeFiles/keys.dir/clean

CMakeFiles/keys.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" C:\Users\Xavier\monero\scripts C:\Users\Xavier\monero\scripts C:\Users\Xavier\monero\scripts\build C:\Users\Xavier\monero\scripts\build C:\Users\Xavier\monero\scripts\build\CMakeFiles\keys.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/keys.dir/depend
