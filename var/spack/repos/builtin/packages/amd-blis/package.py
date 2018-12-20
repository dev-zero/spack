# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class AmdBlis(Package):
    """AMD-fork of BLIS with improvements for AMD and ARM"""

    homepage = "https://github.com/amd/blis"
    url      = "https://github.com/amd/blis/archive/1.2.0.tar.gz"
    git      = "https://github.com/amd/blis.git"

    version('develop', branch='master')
    version('1.2', sha256='b2e7d055c37faa5bfda5a1be63a35d1e612108a9809d7726cedbdd4722d76b1d')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('pthreads', 'openmp', 'none'),
        multi=False
    )

    variant(
        'blas', default=True,
        description='BLAS compatibility',
    )

    variant(
        'cblas', default=False,
        description='CBLAS compatibility',
    )

    variant(
        'shared', default=True,
        description='Build shared library',
    )

    variant(
        'static', default=True,
        description='Build static library',
    )

    # TODO: add cpu variants. Currently using auto.
    # If one knl, should the default be memkind ?

    # BLIS has it's own API but can be made compatible with BLAS
    # enabling CBLAS automatically enables BLAS.

    provides('blas', when="+blas")
    provides('blas', when="+cblas")

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        config_args = []

        config_args.append("--enable-threading=" +
                           spec.variants['threads'].value)

        if '+cblas' in spec:
            config_args.append("--enable-cblas")
        else:
            config_args.append("--disable-cblas")

        if '+blas' in spec:
            config_args.append("--enable-blas")
        else:
            config_args.append("--disable-blas")

        if '+shared' in spec:
            config_args.append("--enable-shared")
        else:
            config_args.append("--disable-shared")

        if '+static' in spec:
            config_args.append("--enable-static")
        else:
            config_args.append("--disable-static")

        config_args.append("auto")

        configure("--prefix=" + prefix,
                  *config_args)

    def build(self, spec, prefix):
        make()

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check(self):
        make('checkblis-fast')

        if '+blas' in self.spec:
            make('checkblas')

    def install(self, spec, prefix):
        make('install')
