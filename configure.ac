#
# configure.ac
#
# Written by: Francesco Salvestrini <f DOT salvestrini AT nextworks DOT it>
#

AC_INIT([RINA Configuration Generator],
        m4_esyscmd([build-aux/git-version-gen .tarball-version]),
        [f.salvestrini@nextworks.it],
        [rina-confgen],
        [http://irati.eu])

AC_PREREQ([2.68])

AC_CONFIG_SRCDIR([src/confgen.in])
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([m4])

AC_CANONICAL_BUILD
AC_CANONICAL_HOST
AC_CANONICAL_TARGET

AM_INIT_AUTOMAKE([1.11.1 tar-pax foreign std-options -Wall])

AC_PROG_SED
AC_PROG_GREP
AC_PROG_MKDIR_P
AC_PROG_LN_S

AC_PATH_PROG([FMT],  [fmt],  [/bin/false])
AC_PATH_PROG([SORT], [sort], [/bin/false])
AC_PATH_PROG([UNIQ], [uniq], [/bin/false])
AC_PATH_PROG([GIT],  [git],  [/bin/false])

PYTHON_VERSION_MIN="3.3.0"
AM_PATH_PYTHON([$PYTHON_VERSION_MIN],[
    AX_PYTHON_MODULE([sys],,[
        AC_MSG_ERROR([Python module sys seems missing (???)])
    ])
    AX_PYTHON_MODULE([os],,[
        AC_MSG_ERROR([Python module os seems missing (???)])
    ])
    AX_PYTHON_MODULE([argparse],,[
        AC_MSG_ERROR([Python module arparse seems missing (???)])
    ])
    AX_PYTHON_MODULE([xml.dom.minidom],,[
        AC_MSG_ERROR([Python module xml.dom.minidom seems missing (???)])
    ])
    AX_PYTHON_MODULE([json],,[
        AC_MSG_ERROR([Python module json seems missing (???)])
    ])
    AX_PYTHON_MODULE([socket],,[
        AC_MSG_ERROR([Python module socket seems missing (???)])
    ])
    AX_PYTHON_MODULE([paramiko],,[
        AC_MSG_ERROR([Python module paramiko seems missing (???)])
    ])
    AX_PYTHON_MODULE([time],,[
        AC_MSG_ERROR([Python module time seems missing (???)])
    ])
    AX_PYTHON_MODULE([ast],,[
        AC_MSG_ERROR([Python module ast seems missing (???)])
    ])
    AX_PYTHON_MODULE([re],,[
        AC_MSG_ERROR([Python module re seems missing (???)])
    ])
],[
    AC_MSG_ERROR([Python (>= $PYTHON_VERSION_MIN) seems missing])
])

AC_CONFIG_FILES([
    Makefile

    src/Makefile
    src/inputs/Makefile
    src/inputs/2nodes/Makefile
    src/inputs/datnet/Makefile
])

AC_OUTPUT
