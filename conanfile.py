from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import os

class NetcdffortranConan(ConanFile):
    name = "netcdf-fortran"
    license = "MIT"
    url = "https://github.com/kevinrichardgreen/conan-netcdf-fortran"
    description = "Unidata network Common Data Form Fortran"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}

    generators = "cmake"

    source_subfolder = "netcdf-fortran"


    def requirements(self):
        self.requires("netcdf-c/[>=4.7]@CHM/stable")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("netcdf-fortran-{0}".format(self.version), self.source_subfolder)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        configure_args = [ ]
        # add to configuration args

        with tools.chdir(self.source_subfolder):

            autotools.configure(args=configure_args)
            autotools.make()
            autotools.install()


        # if tools.os_info.is_macos:
        #     tools.replace_in_file("netcdf-cxx4/CMakeLists.txt", "PROJECT(NCXX C CXX)",
        #                           '''PROJECT(NCXX C CXX)
        #                             include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        #                             conan_basic_setup(KEEP_RPATHS)''')
        # else:
        #     tools.replace_in_file("netcdf-cxx4/CMakeLists.txt", "PROJECT(NCXX C CXX)",
        #                           '''PROJECT(NCXX C CXX)
        #                             include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                                    # conan_basic_setup()''')


    def configure(self):
        if not tools.os_info.is_linux:
            raise ConanInvalidConfiguration("Library netcddf-fortran is currently only supported for Linux")


    def package(self):
        # all include files should go in include
        self.copy("*.h", dst="include", src="netcdf-fortran")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("libgsl*.a", dst="lib", keep_path=False)

        # if tools.os_info.is_linux:
        #     with tools.chdir(self.package_folder):
        #         cmd = "patchelf --remove-rpath lib/libnetcdf-cxx4.so"
        #         os.system(cmd)

    def package_info(self):
        self.cpp_info.libs = ["netcdff"]
