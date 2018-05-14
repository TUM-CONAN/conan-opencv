#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        bin_path = os.path.join("bin", "test_package")
        if self.settings.os == "Macos":
            self.run('DYLD_LIBRARY_PATH=%s %s' % (os.environ['DYLD_LIBRARY_PATH'], bin_path))
        else:
            self.run(bin_path)
