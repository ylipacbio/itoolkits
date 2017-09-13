mytool?=newtool
dstdir?=/home/UNIXHOME/yli/tmp/newtool
CWD=$(shell pwd)

all:
	@echo copying python repo template for ${mytool} to destination ${dstdir}
	@echo Please override mytool and dstdir
	rm -rf ${dstdir} && mkdir ${dstdir} && \
	cd ${dstdir} && cp -r ${CWD}/* . && \
	find . -type f | xargs sed -i 's/mytool/${mytool}/g' && \
	echo `pwd` && ls && mv mytool ${mytool} && mv mytool.makefile makefile && \
	cd ${CWD}

usage:
	echo To initialize a new python tool repo, named newtool, please
	echo edit makefile and type `make`
