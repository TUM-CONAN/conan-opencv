# conan-opencv

[Conan.io](https://conan.io) package for opencv library. 

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload opencv/3.2.0@camposs/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install opencv/3.2.0@camposs/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    opencv/3.2.0@camposs/stable

    [options]
    opencv:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
