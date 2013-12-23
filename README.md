Joseph Mansfield
================

This is the source for Joseph Mansfield's personal website. The website is
generated as static HTML pages that can then be deployed to a HTTP server. The
build process includes the following steps:

1.  **Process**: process data files to determine which pages need to be
    generated and the content that needs to be inserted into them.
2.  **Generate**: perform template substitution to generate the appropriate
    static HTML pages.
3.  **Post-process**: optimize the website with techniques such as minimisation,
    compression, and so on.

Building
--------

To build, run `build.sh` from a build directory. For example:

    $ mkdir build
    $ cd build
    $ ../build.sh

If you create the build directory in the source tree (as in the example) and
wish to commit some changes you've made, make sure your build directory has been
added to `.git/info/exclude`.
