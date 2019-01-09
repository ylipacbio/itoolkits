project(
  'mytool',
  ['c', 'cpp'],
  version : '0.1.0',
  default_options : [
    'buildtype=debug',
    'warning_level=3',
    'cpp_std=c++14',
    'c_std=gnu11',
    'b_ndebug=if-release'],
  license : 'BSD-3',
  meson_version : '>= 0.46.0')

# compile flags
mytool_flags = ['-g', '-ggdb']
cpp = meson.get_compiler('cpp')
foreach cflag: [
  '-Wno-unused-command-line-argument',
  '-Wno-missing-field-initializers',
  '-Wno-unused-parameter',
  '-Wno-unused-variable',
  '-Wno-unused-const-variable']
    if cpp.has_argument(cflag)
      mytool_flags += cflag
    endif
endforeach

if cpp.get_id() == 'clang'
  foreach cflag: [
    '-Wno-unused-local-typedef',
    '-Wno-c99-extensions']
      if cpp.has_argument(cflag)
        mytool_flags += cflag
      endif
  endforeach
endif

if get_option('sse41')
  if cpp.has_argument('-msse4.1')
    mytool_flags += '-msse4.1'
  else
    error('Requested SSE4.1, but the C++ compiler does not support -msse4.1')
  endif
endif

# dependencies #
## threads
mytool_thread_dep = dependency('threads', required : true)
## boost
mytool_boost_dep = dependency('boost', required : true)
## zlib
mytool_zlib_dep = dependency('zlib', fallback : ['zlib', 'zlib_dep'])
## pbbam
mytool_pbbam_dep = dependency('pbbam', fallback : ['pbbam', 'pbbam_dep'])
## pbcopper
mytool_pbcopper_dep = dependency('pbcopper', fallback : ['pbcopper', 'pbcopper_dep'])
## parasail
#mytool_parasail_dep = dependency('parasail-1', fallback : ['parasail', 'parasail_dep'])
## minimap2
#mytool_minimap2_dep = dependency('minimap2', fallback : ['minimap2', 'mm2_dep'])
## unanimity
#mytool_unanimity_dep = dependency('unanimity', fallback : ['unanimity', 'uny_dep'])
## gcpp
#mytool_gcpp_dep = dependency('gcpp', fallback : ['gcpp', 'gcpp_dep'])

mytool_lib_deps = [
#  mytool_thread_dep,
  mytool_boost_dep,
  mytool_zlib_dep,
  mytool_pbbam_dep,
  mytool_pbcopper_dep,
#  mytool_minimap2_dep,
#  mytool_parasail_dep,
#  mytool_unanimity_dep,
#  mytool_gcpp_dep
  ]

# sources + library
subdir('src')

# tests
if get_option('tests')
  mytool_cram_script = find_program('cram', required : true)
  subdir('tests')
endif
