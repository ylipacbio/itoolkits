mytool_cram_test_data = files([
  'noop.t'
])

test(
  'regression',
  mytool_cram_script,
  args : [
    '--xunit-file=cram.xml',
    '--verbose'] +
    mytool_cram_test_data,
  env : [
    '__PBTEST_mytool_EXE=' + mytool_main.full_path(),
    'TESTDIR=' + meson.current_source_dir()],
  timeout : 1800)
