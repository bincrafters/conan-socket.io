#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "socket.io++"
    version = "1.6.0"
    description = "C++11 implementation of Socket.IO client"
    topics = ["conan", "libname", "socket.io", "socket", "c++"]
    url = "https://github.com/bincrafters/conan-socket.io"
    homepage = "https://github.com/socketio/socket.io-client-cpp"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "Boost_USE_STATIC_LIBS": [True, False]}
    default_options = {"shared": False, "Boost_USE_STATIC_LIBS": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "boost/1.68.0@conan/stable"
    )

    def source(self):
        self.run("git clone self.homepage --depth 1 %s" % self._source_subfolder)
        self.run("cd %s" % self._source_subfolder)
        self.run("git checkout 6063cb1d612f6ca0232d4134a018053fb8faea20") # checkout latest Commit

   def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
