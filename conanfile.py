from conans import ConanFile, CMake, tools
import os, fnmatch

class OpenCVConan(ConanFile):
    # Description must be very short for conan.io
    description = "OpenCV: Open Source Computer Vision Library."
    name = "opencv"
    version = "3.4.1"
    opencv_version_suffix = "341"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_contrib": [True, False],
        "with_cuda": [True, False],
        "with_qt": [True, False],
        "with_tbb": [True, False],
    }
    default_options = (
        "shared=False", 
        "with_contrib=True", 
        "with_cuda=False",
        "with_qt=False",
        "with_tbb=False",
        )

    url = "https://github.com/ulricheck/conan-opencv"
    license = "http://http://opencv.org/license.html"
    generators = "cmake"
    short_paths = True

    def source(self):
        source_url = "https://github.com/opencv/opencv/archive/{0}.tar.gz".format(self.version)
        archive_name = "opencv-{0}".format(self.version)
        tools.get(source_url)
        os.rename(archive_name, "opencv")

        if self.options.with_contrib:
            source_url = "https://github.com/opencv/opencv_contrib/archive/{0}.tar.gz".format(self.version)
            archive_name = "opencv_contrib-{0}".format(self.version)
            tools.get(source_url)
            os.rename(archive_name, "opencv_contrib")


    def build(self):
        cmake = CMake(self)
        cmake_options = {
            "CMAKE_INSTALL_PREFIX": "install",
            #"PYTHON_PACKAGES_PATH": os.path.join("install", "lib", "python2"),
            #"PYTHON3_PACKAGES_PATH": os.path.join("install", "lib", "python3"),
            "WITH_OPENXL": False,
            "WITH_IPP": True,
            "WITH_QT": self.options.with_qt,
            "WITH_GTK": False,
            "WITH_OPENGL": True,
            "WITH_CUDA": self.options.with_cuda,
            "WITH_JPEG": True,
            "BUILD_JPEG": True,
            "WITH_PNG": True,
            "BUILD_PNG": True,
            "WITH_JASPER": True,
            "BUILD_JASPER": True,
            "WITH_ZLIB": True,
            "BUILD_ZLIB": True,
            "WITH_TIFF": True,
            "BUILD_TIFF": True,
            "WITH_TBB": self.options.with_tbb,
            "BUILD_TBB": self.options.with_tbb,
            "WITH_OPENEXR": True,
            "BUILD_OPENEXR": True,
            "WITH_WEBP": True,
            "BUILD_WEBP": True,
            "BUILD_SHARED_LIBS": self.options.shared,
            "BUILD_TESTS": False,
            "BUILD_PERF_TESTS": False,
            "BUILD_opencv_apps": False,
            "CPACK_BINARY_NSIS": False,
            "BUILD_opencv_calib3d": True,
            "BUILD_opencv_features2d": True,
            "BUILD_opencv_flann": True,
            "BUILD_opencv_highgui": True,
            "BUILD_opencv_imgcodecs": True,
            "BUILD_opencv_imgproc": True,
            "BUILD_opencv_ml": True,
            "BUILD_opencv_objectdetect": True,
            "BUILD_opencv_photo": True,
            "BUILD_opencv_shape": True,
            "BUILD_opencv_stitching": True,
            "BUILD_opencv_superres": True,
            "BUILD_opencv_ts": True,
            "BUILD_opencv_video": True,
            "BUILD_opencv_videoio": True,
            "BUILD_opencv_videostab": True,
            "BUILD_opencv_python2": False,
            "BUILD_opencv_python3": False,
        }

        if self.options.with_contrib:
            cmake_options["OPENCV_EXTRA_MODULES_PATH"] = os.path.join(self.source_folder, "opencv_contrib", "modules")

        if self.settings.compiler == "Visual Studio":
            cmake_options["BUILD_WITH_STATIC_CRT"] = self.settings.compiler.runtime in ["MT","MTd"]
        cmake.configure(defs=cmake_options, source_dir="opencv")
        cmake.build(target="install")

    def package(self):
        self.copy(pattern="*.h*", dst="include", src =os.path.join("install", "include"), keep_path=True)

        if self.settings.os == "Windows":
            self.copy(pattern="*.lib", dst="lib", src="3rdparty\\lib", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="3rdparty\\ippicv\\ippicv_win\\lib\\intel64", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.exe", dst="bin", src="bin", keep_path=False)

        if self.settings.os == "Linux":
            self.copy(pattern="*.a", dst="lib", src="3rdparty/lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="3rdparty/ippicv/ippicv_lnx/lib/intel64", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="install", keep_path=False)

        if self.settings.os == "Macos":
            self.copy(pattern="*.a", dst="lib", src="3rdparty/lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="3rdparty/ippicv/ippicv_mac/lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src="install", keep_path=False)

    def package_info(self):
        self.cpp_info.defines.append("HAVE_OPENCV")
        
        libs_opencv = [
            "opencv_calib3d",
            "opencv_flann",
            "opencv_features2d",
            "opencv_highgui",
            "opencv_imgcodecs",
            "opencv_imgproc",
            "opencv_ml",
            "opencv_objdetect",
            "opencv_photo",
            "opencv_shape",
            "opencv_stitching",
            "opencv_superres",
            "opencv_video",
            "opencv_videoio",
            "opencv_videostab",
            "opencv_core" # GCC wants this last
        ]

        if self.options.with_contrib:
            libs_opencv.extend([
                "opencv_aruco",
                "opencv_bgsegm",
                "opencv_bioinspired",
                "opencv_ccalib",
                "opencv_dnn",
                "opencv_dnn_objdetect",
                "opencv_dpm",
                "opencv_face",
                "opencv_freetype",
                "opencv_fuzzy",
                "opencv_hdf",
                "opencv_hfs",
                "opencv_img_hash",
                "opencv_line_descriptor",
                "opencv_optflow",
                "opencv_phase_unwrapping",
                "opencv_plot",
                "opencv_reg",
                "opencv_rgbd",
                "opencv_saliency",
                "opencv_sfm",
                "opencv_stereo",
                "opencv_structured_light",
                "opencv_surface_matching",
                "opencv_text",
                "opencv_tracking",
                "opencv_xfeatures2d",
                "opencv_ximgproc",
                "opencv_xobjdetect",
                "opencv_xphoto",
                ])

        libs_3rdparty = [
            "zlib",
            "libjpeg",
            "libpng",
            "libjasper",
            "libtiff",
            "libwebp",
            "IlmImf"
        ]
        libs_win = [
            "ippicvmt"
        ]
        libs_linux = [
            "ippicv",
            "pthread",
            "dl" # GCC wants this last
        ]
        libs_macos = [
            "ippicv",
            "pthread",
            "dl" # GCC wants this last
        ]
        if self.settings.compiler == "Visual Studio":
            debug_suffix = ("d" if self.settings.build_type=="Debug" else "")
            libs_opencv_win = [n + self.opencv_version_suffix + debug_suffix for n in libs_opencv]
            libs_3rdparty_win = [n + debug_suffix for n in libs_3rdparty]
            libs = libs_opencv_win + libs_3rdparty_win + libs_win
            self.cpp_info.libs.extend(libs)
        elif self.settings.os == "Linux":
            libs = libs_opencv + libs_3rdparty + libs_linux
            self.cpp_info.libs.extend(libs)
        elif self.settings.os == "Macos":
            libs = libs_opencv + libs_3rdparty + libs_macos
            self.cpp_info.libs.extend(libs)
