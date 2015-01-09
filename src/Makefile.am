#
# Makefile.am
#
# Written by: Francesco Salvestrini <f DOT salvestrini AT nextworks DOT it>
#

SUBDIRS                            =
EXTRA_DIST                         =
DISTCLEANFILES                     =
bin_PROGRAMS                       =
bin_SCRIPTS                        =
AM_INSTALLCHECK_STD_OPTIONS_EXEMPT =

edit = $(SED)							\
        -e 's|@PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g'		\
        -e 's|@PACKAGE_NAME[@]|$(PACKAGE_NAME)|g'		\
        -e 's|@PACKAGE_URL[@]|$(PACKAGE_URL)|g'			\
        -e 's|@PACKAGE_BUGREPORT[@]|$(PACKAGE_BUGREPORT)|g'	\
        -e 's|@PYTHON[@]|$(PYTHON)|g'				\
        -e 's|@SHELL[@]|$(SHELL)|g'

rina-confgen: rina-confgen.in Makefile
	rm -f $@ $@.tmp
	srcdir=''; \
	  test -f ./$@.in || srcdir=$(srcdir)/; \
	  $(edit) $${srcdir}$@.in >$@.tmp
	chmod a-w $@.tmp
	chmod a+x $@.tmp
	mv $@.tmp $@

bin_SCRIPTS    += rina-confgen
DISTCLEANFILES += rina-confgen
EXTRA_DIST     += rina-confgen.in
AM_INSTALLCHECK_STD_OPTIONS_EXEMPT += rina-confgen

EXTRA_DIST += apps.xml ipcps.xml topology.xml
