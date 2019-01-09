mytool_src_include_directories = include_directories('.')

################
# version info #
################
mytool_ver_arr = meson.project_version().split('.')
mytool_major_version = mytool_ver_arr[0]
mytool_minor_version = mytool_ver_arr[1]
mytool_patch_version = mytool_ver_arr[2]

mytool_config = configuration_data()
mytool_config.set('MYTOOL_VERSION', meson.project_version())
mytool_config.set('MYTOOL_VERSION_MAJOR', mytool_major_version)
mytool_config.set('MYTOOL_VERSION_MINOR', mytool_minor_version)
mytool_config.set('MYTOOL_VERSION_PATCH', mytool_patch_version)

mytool_version_sources = [
  vcs_tag(
    input : 'MyToolGitHash.cpp.in',
    output : 'MyToolGitHash.cpp',
    command : ['git', 'describe', '--always', '--dirty=*'],
    replace_string : '@MyTool_GIT_SHA1@'),
  configure_file(
    input : 'MyToolVersion.cpp.in',
    output : 'MyToolVersion.cpp',
    configuration : mytool_config)]

mytool_cpp_sources = files([
  'tools/MemoryConsumption.cpp',
  'tools/Timer.cpp',

  'tools/mytool/MyToolSettings.cpp',
  'tools/mytool/MyToolWorkflow.cpp',
])

mytool_cpp_sources += mytool_version_sources

mytool_lib_impl = static_library(
  'mytool',
  mytool_cpp_sources,
  install : false,
  dependencies : mytool_lib_deps,
  include_directories : mytool_src_include_directories,
  cpp_args : mytool_flags)

mytool_main = executable(
  'mytool', files([
    'tools/mytool/mytool.cpp']),
  install : true,
  dependencies : mytool_lib_deps,
  include_directories : mytool_src_include_directories,
  link_with: mytool_lib_impl,
  cpp_args : mytool_flags)
