# VirusTotal/yara

Repositório: https://github.com/VirusTotal/yara

## Metadados

- Linguagem: C

## Releases sorteadas

### Release 1

Link: https://github.com/VirusTotal/yara/releases/tag/v3.3.0
- Tag: `v3.3.0`
- Nome: YARA v3.3.0
- Publicada em: 2015-02-10
- Release anterior (cronológica): `v3.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 192

-  Fix segfault with some syntax errors and improve error reporting
-  Fix a problem with ord_lookup.
-  Merge pull request #199 from wxsBSD/ord_lookup_fix
-  Fix issues when using dmalloc
-  Fix memory and handle leaks
-  Avoid segfault when yr_re_finalize is called before yr_re_initialize
-  Use argparse library to parse command line arguments and some other improvements
-  Fix incorrect initialization of thread_storage_key in Windows
-  Fix warnings
-  Use integer arithmetic instead of floating point operations and fix problems in C++
-  Update Visual Studio project
-  Implement --pring-namespace commad-line argument
-  Replace argparse with my own argument parsing code
-  Fix segfault in PE module
-  Fix --timeout argument to work with directories
-  Initialize timeout with a large number
-  Avoid hitting a bug in lldb-320.4.152
-  fix: compilation error because of multiple function declarations
-  Merge pull request #203 from pozdnychev/master
-  Accept None for argument "externals"
-  Fix issues while building in some systems
-  Fix warnings
-  Fix warnings
-  Fix issue in Python 2.4
-  fix issue #206
-  internals: use ERROR_SUCCESS and ERROR_INSUFICIENT_MEMORY instead of 0/-1
-  Fix incorrect line number for syntax errors after a regexp declarations
-  Merge pull request #207 from pozdnychev/master
-  Minor style changes
-  fix: data leak in case of error in yr_process_get_memory
-  Merge pull request #209 from pozdnychev/master
-  Minor style changes
-  Update Windows project
-  Fix some issues while compiling in Windows
-  Fix compile error due to undefined identifier
-  Fixed command to install yara-python extension
-  Fix issue #213
-  Improve resource handling and add entropy.
-  Merge branch 'master' into resource_name_and_entropy
-  Merge pull request #214 from ortizmj12/patch-1
- ... e mais 152 commits

### Release 2

Link: https://github.com/VirusTotal/yara/releases/tag/v3.4.0
- Tag: `v3.4.0`
- Nome: YARA v3.4.0
- Publicada em: 2015-06-18
- Release anterior (cronológica): `v3.3.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 160

-  Adding examples specs for yara/yara-python rpm's.
-  Fix issue #253
-  Add a simple read-only stream abstraction that supports a fread(3)-like interface
-  Add yr_arena_load_stream function
-  Add yr_rules_load_stream API
-  python: Add simple test for yara.load(FILE-LIKE-OBJECT)
-  python: Add reader for file-like objects
-  PE module: Fix unchecked access to version info buffers
-  PE module: Corrected size of strings in checks
-  strutils: Made strcmp_w more exact (don't ignore upper byte of wide chars)
-  Merge pull request #256 from moritzkroll/pe-versioninfo-fix
-  Minor indentation changes
-  Merge pull request #252 from hillu/stream
-  Improve streams
-  Performance improvement. Write a large chunk of data instead of many individual bytes.
-  Don't try to memset() the allocated memory, if the allocation failed.
-  Merge pull request #257 from cognet/master
-  Fix issue #258
-  Avoid infinite loop with certain PE files
-  Fix wrong parsing of PE version info
-  Fix issue with "save" function not accepting unicode strings in Python 2.x
-  Add Websense to "Who's using YARA"
-  Implement short-circuit evaluation
-  Put a link to yextend
-  Fix grammar error
-  Put reference to yextend in a separate paragraph
-  Add workaround for link failure (undefined reference to '_time32') when cross-compiling with MinGW
-  Fix for running 'configure' in another folder
-  Merge pull request #268 from axqd/patch-1
-  Merge pull request #263 from hillu/mingw-workaround
-  Use GCC's -fvisibility feature together with YR_API definition instead
-  Remove execution permission from some source files
-  fixed build on freebsd 10 with a conditional #define so that warnings are not introduced in other builds
-  Do not recompute match chain lengths
-  Merge pull request #276 from cblichmann-google/no-recompute-chain-lengths
-  Initialize new_match->chain_length
-  Fix memory leaks found using pe module.
-  Increase limits and dynamically allocate stack.
-  Merge pull request #278 from shanehuntley/leakfix
-  Merge pull request #279 from shanehuntley/newlimits
- ... e mais 120 commits

### Release 3

Link: https://github.com/VirusTotal/yara/releases/tag/v3.8.0
- Tag: `v3.8.0`
- Nome: YARA v3.8.0
- Publicada em: 2018-08-06
- Release anterior (cronológica): `v3.7.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 198

-  Mach-O file format support (#617)
-  Add fuzzer for "macho" module.
-  Re-introduce changes reverted by 0c57f0bd66a118c62e43c0a7da57a3d8134fe168
-  Fix issue #796.
-  Include "macho" module only if --enable-macho is passed to ./configure script.
-  Fix edge case in PE checksum calculation.
-  Add "module_data" variable to "tests" module. The variable is populated with the data passed for the module at runtime.
-  Add missing typecast.
-  compiler: Open included files to parse in binary mode (Windows) (#811)
-  Make build.sh executable (chmod +x build.sh)
-  Fix regression in regexp engine. Close #817.
-  Fix regression in profiling logic.
-  Fix typo s/now/not/.
-  Fix another issue introduced in #760.
-  Implement scanner API.
-  Fix warnings.
-  semaphore_init: use sem_init on FreeBSD (#815)
-  Document set_config class function in yara-python (#814)
-  modules/pe: Fixed possible invalid memory read when parsing certificates (#804)
-  Don't access directory entries past SizeOfOptionalHeader. (#802)
-  Fix whitespace. (#800)
-  Added parsing of unoptimized metadata stream in dotnet module (#798)
-  Add explicit support for DragonFly BSD, kFreeBSD to Linux process scan module (#790)
-  add Joe Security to "who's using yara" (#794)
-  Add Avast to "Who's using YARA". (#805)
-  Add ESTsecurity to "Who's using YARA". (#820)
-  Raise warning when .+ is used in a regular expression (#713)
-  Minor re-styling.
-  Implement callback for allowing clients of the library inspecting the AST for regular expressions.
-  Small optimization in yr_re_ast_extract_literal.
-  Make yr_scanner_define_boolean_variable receive an int instead of an int64_t. This keep the coherency with yr_compiler_define_boolean_variable and yr_rules_define_boolean_variable.
-  Allow building with jemalloc library.
-  Dump jemalloc profile in yr_finalize if built with --enable-jemalloc.
-  Do not use thread local storage for storing fiber pools in regexp eng… (#823)
-  Fix issue when compiling YARA with MAX_ATOM_SIZE larger than 4.
-  Add DEX module (#822)
-  Some re-styling in dex module. Add adesnos to CONTRIBUTORS.
-  Add dex module to Visual Studio project.
-  Fix wrong placeholder while calling set_integer in dex module.
-  Fix dex test case.
- ... e mais 158 commits

### Release 4

Link: https://github.com/VirusTotal/yara/releases/tag/v4.0.1
- Tag: `v4.0.1`
- Nome: YARA v4.0.1
- Publicada em: 2020-05-15
- Release anterior (cronológica): `v4.0.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 22

-  codemirror - add yara 4.0 keywords
-  Fix unaligned data accesses on ARM
-  Minor style fixes.
-  Fix regression in export parsing.
-  Add Forcepoint to README.md
-  Remove mach-o macros from fat file parsing
-  Remove mach-o macros from LC_MAIN parsing
-  Remove mach-o macros from LC_UNIXTHREAD parsing
-  Remove mach-o macros from LC_SEGMENT parsing
-  Remove mach-o macros from main file parsing
-  Declare macho helper functions as static
-  Minor re-styling.
-  Create test case for uninitialized number_of_segments
-  Parse number_of_segments completely before other CMDs
-  Add `copts` option to `yara_library`
-  Update Bazel dependencies
-  Update YARA Sandboxed API sandbox
-  Merge branch 'master' into master
-  Merge branch 'cblichmann-master'
-  Add missing data files to Bazel tests.
-  Fix issue in logic expression.
-  Bump version number to 4.0.1

### Release 5

Link: https://github.com/VirusTotal/yara/releases/tag/v4.2.0
- Tag: `v4.2.0`
- Nome: YARA v4.2.0
- Publicada em: 2022-03-10
- Release anterior (cronológica): `v4.2.0-rc1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 30

-  Define operator precedence in grammar.y exactly as documented.
-  Enable "dotnet" module by default.
-  Increment YR_ARENA_FILE_VERSION.
-  Increment ABI version.
-  Implement test cases for issue #1631
-  Remove test file.
-  Fixes issue #1631. (#1632)
-  Fix issue with dotnet build. (#1642)
-  remove duplicate include for args.h (#1641)
-  Fix issue with argument handling. (#1640)
-  Remove old LibreSSL glue preventing compilation of pe module (#1636)
-  remove the '\n' in the map_path variable (#1638)
-  add missing semicolon (#1645)
-  Fix mistake in console docs. (#1644)
-  Fix cuckoosandbox url (#1648)
-  Fix for MSVC builds (#1653)
-  Improve atom extraction logic (#1656)
-  Update users list (#1650)
-  Add function pe.is_dotnet() for .NET file detection (#1568)
-  Apply linter to dotnet.c
-  Convert is_dotnet() function back to a field.
-  Run test cases for dotnet module with Bazel.
-  Do not create hash table in dotnet module, as it is not used.
-  Prevent large memory consumption when scanning malformed files. (#1658)
-  Fix buffer overrun in dotnet module.
-  Fix type conversion warnings.
-  Fix warnings and replace `long long` with `int64_t`
-  Fix docs for console callback with python. (#1659)
-  Fix issue #1635
-  Fix #1660. (#1661)
