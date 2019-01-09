mytool?=newtool
MyTool?=NewTool
MYTOOL?=NEWTOOL
dstdir?=/home/UNIXHOME/yli/tmp/newtool
CWD=$(shell pwd)

all:
	@echo copying c++ repo template for ${mytool} to destination ${dstdir}
	@echo Please override mytool and dstdir
	rm -rf ${dstdir} && mkdir ${dstdir} \
	&& cd ${dstdir} && ls ${CWD}/* && cp -r ${CWD}/* . \
	&& cp ${CWD}/.gitignore .  \
	&& mv src/MyToolGitHash.cpp.in src/${MyTool}GitHash.cpp.in \
	&& mv src/MyToolVersion.cpp.in src/${MyTool}Version.cpp \
	&& mv src/MyToolVersion.h src/${MyTool}Version.h \
	&& mv src/tools/mytool src/tools/${mytool}/ \
	&& mv src/tools/${mytool}/mytool.cpp src/tools/${mytool}/${mytool}.cpp \
	&& mv src/tools/${mytool}/MyToolSettings.cpp src/tools/${mytool}/${MyTool}Settings.cpp \
	&& mv src/tools/${mytool}/MyToolSettings.h src/tools/${mytool}/${MyTool}Settings.h \
	&& mv src/tools/${mytool}/MyToolWorkflow.cpp src/tools/${mytool}/${MyTool}Workflow.cpp \
	&& mv src/tools/${mytool}/MyToolWorkflow.h src/tools/${mytool}/${MyTool}Workflow.h \
	&& find . -type f | xargs sed -i 's/MYTOOL/${MYTOOL}/g' \
	&& find . -type f | xargs sed -i 's/MyTool/${MyTool}/g' \
	&& find . -type f | xargs sed -i 's/mytool/${mytool}/g' \
	&& mv mytool.makefile makefile \
	&& sed -i 's/MYTOOL/${MYTOOL}/g' makefile \
	&& sed -i 's/MyTool/${MyTool}/g' makefile \
	&& sed -i 's/mytool/${mytool}/g' makefile \
	&& echo "Set up cpp repo at ${dstdir}" \
	&& cd ${CWD}


usage:
	echo To initialize a new c++ tool repo, named newtool, please
	echo edit makefile and type `make`
