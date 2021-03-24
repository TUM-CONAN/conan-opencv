from conans import ConanFile, CMake, tools
import os, fnmatch

class OpenCVConan(ConanFile):
    # Description must be very short for conan.io
    description = "OpenCV: Open Source Computer Vision Library."
    name = "opencv"
    version = "3.4.13"
    opencv_version_suffix = version.replace(".","")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_cuda": [True, False],
        "with_opengl": [True, False],
        "with_qt": [True, False],
        "with_gtk": [True, False],
        "with_tbb": [True, False],
        "with_calib3d": [True, False],
        "with_features2d": [True, False],
        "with_flann": [True, False],
        "with_highgui": [True, False],
        "with_imgcodecs": [True, False],
        "with_imgproc": [True, False],
        "with_ml": [True, False],
        "with_objectdetect": [True, False],
        "with_photo": [True, False],
        "with_shape": [True, False],
        "with_stitching": [True, False],
        "with_superres": [True, False],
        "with_ts": [True, False],
        "with_video": [True, False],
        "with_videoio": [True, False],
        "with_videostab": [True, False],
        "with_viz": [True, False],
        "with_python2": [True, False],
        "with_python3": [True, False],
        "with_aruco": [True, False],
        "with_bgsegm": [True, False],
        "with_bioinspired": [True, False],
        "with_ccalib": [True, False],
        "with_dataset": [True, False],
        "with_dnn": [True, False],
        "with_dnn_objdetect": [True, False],
        "with_dpm": [True, False],
        "with_face": [True, False],
        "with_freetype": [True, False],
        "with_fuzzy": [True, False],
        "with_hdf": [True, False],
        "with_hfs": [True, False],
        "with_img_hash": [True, False],
        "with_line_descriptor": [True, False],
        "with_optflow": [True, False],
        "with_phase_unwrapping": [True, False],
        "with_plot": [True, False],
        "with_reg": [True, False],
        "with_rgbd": [True, False],
        "with_saliency": [True, False],
        "with_sfm": [True, False],
        "with_stereo": [True, False],
        "with_structured_light": [True, False],
        "with_surface_matching": [True, False],
        "with_text": [True, False],
        "with_tracking": [True, False],
        "with_xfeatures2d": [True, False],
        "with_ximgproc": [True, False],
        "with_xobjdetect": [True, False],
        "with_xphoto": [True, False],
    }

    default_options = (
        "shared=False", 
        "with_cuda=False",
        "with_opengl=False",
        "with_qt=False",
        "with_gtk=False",
        "with_tbb=False",
        "with_calib3d=True",
        "with_features2d=True",
        "with_flann=True",
        "with_highgui=True",
        "with_imgcodecs=True",
        "with_imgproc=True",
        "with_ml=True",
        "with_objectdetect=True",
        "with_photo=True",
        "with_shape=False",
        "with_stitching=False",
        "with_superres=False",
        "with_ts=False",
        "with_video=True",
        "with_videoio=True",
        "with_videostab=True",
        "with_viz=False",
        "with_python2=False",
        "with_python3=False",
        "with_aruco=True",
        "with_bgsegm=False",
        "with_bioinspired=False",
        "with_ccalib=False",
        "with_dataset=False",
        "with_dnn=False",
        "with_dnn_objdetect=False",
        "with_dpm=False",
        "with_face=False",
        "with_freetype=False",
        "with_fuzzy=False",
        "with_hdf=False",
        "with_hfs=False",
        "with_img_hash=False",
        "with_line_descriptor=False",
        "with_optflow=False",
        "with_phase_unwrapping=False",
        "with_plot=False",
        "with_reg=False",
        "with_rgbd=False",
        "with_saliency=False",
        "with_sfm=False",
        "with_stereo=False",
        "with_structured_light=False",
        "with_surface_matching=False",
        "with_text=False",
        "with_tracking=False",
        "with_xfeatures2d=False",
        "with_ximgproc=False",
        "with_xobjdetect=False",
        "with_xphoto=False",
        )

    url = "https://github.com/ulricheck/conan-opencv"
    license = "http://http://opencv.org/license.html"
    generators = "cmake"
    short_paths = True

    core_modules = [
        "calib3d", "flann", "features2d", "highgui", "imgcodecs", "imgproc", "ml", 
        "objdetect", "photo", "shape", "stitching", "superres", "video", "videoio", 
        "videostab", "viz", "core",
        ]

    cuda_modules = [
        "cudaarithm", "cudabgsegm", "cudafeatures2d", "cudafilters", "cudaimgproc", 
        "cudalegacy", "cudaobjdetect", "cudaoptflow", "cudastereo", "cudawarping", "cudev",
    ]

    contrib_modules = [
        "aruco", "bgsegm", "bioinspired", "ccalib", "dnn", "dnn_objdetect", "dpm", 
        "face", "freetype", "fuzzy", "hdf", "hfs", "img_hash", "line_descriptor", 
        "optflow", "phase_unwrapping", "plot", "reg", "rgbd", "saliency", "sfm", 
        "stereo", "structured_light", "surface_matching", "text", "tracking", 
        "xfeatures2d", "ximgproc", "xobjdetect", "xphoto", 
        ]

    def requirements(self):
        if self.options.with_qt:
            self.requires("qt/5.12.4-r2@camposs/stable")
        if self.options.with_viz:
            self.requires("vtk/[>=8.0.0]@camposs/stable")
        if self.options.with_cuda:
            self.requires("cuda_dev_config/[>=1.0]@camposs/stable")

    def source(self):
        source_url = "https://github.com/opencv/opencv/archive/{0}.tar.gz".format(self.version)
        archive_name = "opencv-{0}".format(self.version)
        tools.get(source_url)
        os.rename(archive_name, "opencv")

        if self.need_contrib():
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
            "WITH_GTK": self.options.with_gtk,
            "WITH_OPENGL": self.options.with_opengl, # @TODO TestPackage might fail due to missing OpenGL
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

            # temporary .. doesn work on linux/cuda10
            "BUILD_opencv_cudacodec": False,

            "BUILD_opencv_calib3d": self.options.with_calib3d,
            "BUILD_opencv_features2d": self.options.with_features2d,
            "BUILD_opencv_flann": self.options.with_flann,
            "BUILD_opencv_highgui": self.options.with_highgui,
            "BUILD_opencv_imgcodecs": self.options.with_imgcodecs,
            "BUILD_opencv_imgproc": self.options.with_imgproc,
            "BUILD_opencv_ml": self.options.with_ml,
            "BUILD_opencv_objectdetect": self.options.with_objectdetect,
            "BUILD_opencv_photo": self.options.with_photo,
            "BUILD_opencv_shape": self.options.with_shape,
            "BUILD_opencv_stitching": self.options.with_stitching,
            "BUILD_opencv_superres": self.options.with_superres,
            "BUILD_opencv_ts": self.options.with_ts,
            "BUILD_opencv_video": self.options.with_video,
            "BUILD_opencv_videoio": self.options.with_videoio,
            "BUILD_opencv_videostab": self.options.with_videostab,
            "BUILD_opencv_viz": self.options.with_viz,
            "BUILD_opencv_python2": self.options.with_python2,
            "BUILD_opencv_python3": self.options.with_python3,

            "BUILD_opencv_aruco": self.options.with_aruco,
            "BUILD_opencv_bgsegm": self.options.with_bgsegm,
            "BUILD_opencv_bioinspired": self.options.with_bioinspired,
            "BUILD_opencv_ccalib": self.options.with_ccalib,
            "BUILD_opencv_dataset": self.options.with_dataset,
            "BUILD_opencv_dnn": self.options.with_dnn,
            "BUILD_opencv_dnn_objdetect": self.options.with_dnn_objdetect,
            "BUILD_opencv_dpm": self.options.with_dpm,
            "BUILD_opencv_face": self.options.with_face,
            "BUILD_opencv_freetype": self.options.with_freetype,
            "BUILD_opencv_fuzzy": self.options.with_fuzzy,
            "BUILD_opencv_hdf": self.options.with_hdf,
            "BUILD_opencv_hfs": self.options.with_hfs,
            "BUILD_opencv_img_hash": self.options.with_img_hash,
            "BUILD_opencv_line_descriptor": self.options.with_line_descriptor,
            "BUILD_opencv_optflow": self.options.with_optflow,
            "BUILD_opencv_phase_unwrapping": self.options.with_phase_unwrapping,
            "BUILD_opencv_plot": self.options.with_plot,
            "BUILD_opencv_reg": self.options.with_reg,
            "BUILD_opencv_rgbd": self.options.with_rgbd,
            "BUILD_opencv_saliency": self.options.with_saliency,
            "BUILD_opencv_sfm": self.options.with_sfm,
            "BUILD_opencv_stereo": self.options.with_stereo,
            "BUILD_opencv_structured_light": self.options.with_structured_light,
            "BUILD_opencv_surface_matching": self.options.with_surface_matching,
            "BUILD_opencv_text": self.options.with_text,
            "BUILD_opencv_tracking": self.options.with_tracking,
            "BUILD_opencv_xfeatures2d": self.options.with_xfeatures2d,
            "BUILD_opencv_ximgproc": self.options.with_ximgproc,
            "BUILD_opencv_xobjdetect": self.options.with_xobjdetect,
            "BUILD_opencv_xphoto": self.options.with_xphoto,
        }

        if self.need_contrib():
            cmake_options["OPENCV_EXTRA_MODULES_PATH"] = os.path.join(self.source_folder, "opencv_contrib", "modules")

        if self.settings.compiler == "Visual Studio":
            cmake_options["BUILD_WITH_STATIC_CRT"] = self.settings.compiler.runtime in ["MT","MTd"]
        cmake.configure(defs=cmake_options, source_dir="opencv")
        cmake.build(target="install")

    def need_contrib(self):
        for name in self.contrib_modules:
            if (getattr(self.options, "with_%s" % name, False)):
                return True
        return False

    def package(self):
        self.copy(pattern="*.h*", dst="include", src =os.path.join("install", "include"), keep_path=True)

        arch_name = "intel64" if self.settings.arch == "x86_64" else "ia32"

        if self.settings.os == "Windows":
            self.copy(pattern="*.lib", dst="lib", src="3rdparty\\lib", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="3rdparty\\ippicv\\ippicv_win\\icv\\lib\\%s" % arch_name, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.exe", dst="bin", src="bin", keep_path=False)

        if self.settings.os == "Linux":
            self.copy(pattern="*.a", dst="lib", src="3rdparty/lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="3rdparty/ippicv/ippicv_lnx/icv/lib/%s" % arch_name, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="install", keep_path=False)

        if self.settings.os == "Macos":
            self.copy(pattern="*.a", dst="lib", src="3rdparty/lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="3rdparty/ippicv/ippicv_mac/icv/lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="install", keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src="install", keep_path=False)

    def package_info(self):
        # set environment variables
        self.cpp_info.defines.append("HAVE_OPENCV")
        if self.options.shared:
            if self.settings.os == "Macos":
                self.env_info.DYLD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))
            if self.settings.os == "Linux":
                self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "lib"))

        # collect installed libraries and specify linking order explicitly
        compiled_libs = tools.collect_libs(self) 
        libs_opencv = []

        for name in self.contrib_modules + self.core_modules:
            libname = "opencv_%s" % name
            for ln in compiled_libs:
                if (libname in ln) and (libname not in libs_opencv):
                    libs_opencv.append(libname)

        if self.options.with_cuda:
            for name in self.cuda_modules:
                libname = "opencv_%s" % name
                for ln in compiled_libs:
                    if (libname in ln) and (libname not in libs_opencv):
                        libs_opencv.append(libname)

        # can we distinguish which libraries are needed for shared vs. static linking?
        libs_3rdparty = [
            "zlib",
            "libjpeg-turbo",
            "libpng",
            "libjasper",
            "libtiff",
            "libwebp",
            "IlmImf",
            "ittnotify",
            "ippiw",
        ]
        libs_win = [
            "ippicvmt",
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
            # intel performance primitives are only available on x86 and x86_64
            if self.settings.arch not in ['x86', 'x86_64']:
                libs.remove("ippicv")
                libs.remove("ittnotify")
                libs.remove("ippiw")
            self.cpp_info.libs.extend(libs)
        elif self.settings.os == "Macos":
            libs = libs_opencv + libs_3rdparty + libs_macos
            self.cpp_info.libs.extend(libs)
