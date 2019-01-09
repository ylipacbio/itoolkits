subdir('unit')
subdir('cram')

mytool_gtest_main_dep = dependency('gtest_main', fallback : ['gtest', 'gtest_main_dep'])

mytool_test = executable(
  'mytool_test',
  mytool_test_cpp_sources,
  dependencies : [mytool_lib_deps, mytool_gtest_main_dep],
  include_directories : mytool_src_include_directories,
  link_with : mytool_lib_impl,
  cpp_args : mytool_flags,
  install : false)

test(
  'mytool testsuite',
  mytool_test,
  args : [
    '--gtest_output=xml:' + join_paths(meson.build_root(), 'mytool-unit-tests.xml')],
  env : [
    'ARGS=-V',
    'VERBOSE=1'])
