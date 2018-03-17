from conan.packager import ConanMultiPackager
from conans.tools import os_info
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="opencv:shared", pure_c=True)
    # @todo macos static builds need opencl/lapack linking to make test_package work 
    builder.builds = [
        [settings, options, env_vars, build_requires]
        for settings, options, env_vars, build_requires in builder.builds
        if (not ((os_info.is_macos or os_info.is_windows) and options['opencv:shared'] == False))
    ]
    builder.run()
