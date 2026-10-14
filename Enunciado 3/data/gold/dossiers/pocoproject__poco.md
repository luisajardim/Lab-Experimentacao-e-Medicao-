# pocoproject/poco

Repositório: https://github.com/pocoproject/poco

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/pocoproject/poco/releases/tag/poco-1.11.0-release
- Tag: `poco-1.11.0-release`
- Nome: Release 1.11.0
- Publicada em: 2021-06-28
- Release anterior (cronológica): `poco-1.10.1-release`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 203

-  create 1.10.2 branch
-  remove unnecessary escaping in JSONString
-  remove unnecessary space in JSON object serialization
-  add support for typed enums and deleted functions
-  fix JSON object formatting and tests
-  #3153: Poco::Data::ODBC [N]VARCHAR(MAX) wrong maxDataSize() result
-  Removed
-  scripts to build Poco modules as Nuget packages
-  #3202: JWT: ESxxx signature must include padding for ECDSA R and S values
-  PocoDoc - merge changes from macchina.io to allow for insertion of custom HTML into generated pages
-  Merge branches 'master' and 'poco-1.10.2' of github.com:pocoproject/poco into poco-1.10.2
-  add AbstractCache::forEach()
-  add Application::windowSize()
-  formatting
-  RemoteSyslogChannel/RemoteSyslogListener: add buffer size configuration property
-  TypeHandler: move instead of copy
-  Postgres: fix extractor
-  Postgres: set connector name
-  #2932: Poco::Net::NTLMContext is missing dllexport/dllimport symbols
-  #2783: fix Invalid condition [ICMPv4PacketImpl.cpp:234]
-  #2945: Iterating over Var containing empty container throws "Out of range" exception
-  #2970: Poco::Data::TypeHandler<Poco::Nullable<T>>::prepare() must prepare with underlying type, not Poco::Data::Keywords::null
-  #3076: Avoid access to already freed memory in JSON code
-  make URI::getPathSegments() const
-  merge WebSocket fixes from devel
-  #3183: fix setPadding
-  #2993: The Sec-WebSocket-Key of WebSocket is always the same one
-  #2989: setting priorityNames property on PatternFormatter has no effect
-  #2927: Fix assigned value to wrong pointer
-  merge fix from devel
-  remove HowToGetHelp page due to outdated information
-  #3027
-  PatternFormatter: add %O format specifier
-  #3044: Upgrade PCRE to 8.44
-  #3086: Use POCO_IOS_INIT_HACK for Linux in combination with libc++
-  #3095: Digest proxy authentication does not work in 1.10.1
-  #3136: Fixed null character issue when parsing a JSON
-  #3114: Added JSON Array::empty() method
-  #3230: ECDSADigestEngine: include missing header
-  #3242: RemoteSyslogListener: add reusePort option
- ... e mais 163 commits

### Release 2

Link: https://github.com/pocoproject/poco/releases/tag/poco-1.12.1-release
- Tag: `poco-1.12.1-release`
- Nome: Release 1.12.1
- Publicada em: 2022-07-16
- Release anterior (cronológica): `poco-1.12.0-release`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Enable unit test in cmake build
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  add BLOB SQLite test
-  accept notifications by name (if they have one)
-  catch std::exception on parsing
-  fix a leak, add some table features
-  few PostgreSQL fixes
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  GH #2351: WebSocket docs
-  Merge branch 'poco-1.10.0' of github.com:pocoproject/poco into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'poco-1.10.0' into devel
-  Merge branch 'devel' of github.com:pocoproject/poco into devel
-  Merge branch 'master' into devel
-  Merge branch 'poco-1.10.1' into devel
-  Merge branch 'poco-1.10.1' into devel
-  Merge branch 'poco-1.10.1' into devel
-  Merge branch 'poco-1.10.1' into devel
-  Merge branch 'poco-1.10.1' into devel
-  Merge branch 'poco-1.10.1' into devel
- ... e mais 210 commits

### Release 3

Link: https://github.com/pocoproject/poco/releases/tag/poco-1.11.8-release
- Tag: `poco-1.11.8-release`
- Nome: Release 1.11.8
- Publicada em: 2023-10-27
- Release anterior (cronológica): `poco-1.12.5-release`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 74

-  created 1.11.4 branch
-  #3846: Upgrade bundled zlib to 1.2.13 [fixes CVE]
-  #3805: Upgrade expat to 2.4.9
-  #3847: Upgrade bundled SQLite to 3.39.4
-  updated changelog
-  update README.md
-  add publish_release.yml workflow
-  branch off poco-1.11.5
-  #3849: Upgrade bundled libexpat to 2.5.0 [fixes CVE]
-  create poco-1.11.6 branch
-  #3859: zlib headers not updated
-  #3147: Reading from request stream hangs when "Transfer-Encoding: chunked" is used
-  updated changelog
-  GH #3876: Replace sprintf with snprintf in Environment and NumberFormatter to avoid deprecation warnings
-  add header/library search paths for Homebrew on Apple Silicon
-  fix incorrect condition
-  upgrade bundled SQLite to 3.40.0
-  updated changelog
-  add Function::isStatic(), Variable::isConst() and Variable::isStatic()
-  added Command::keys()
-  bump version
-  #4077: OpenSSL 3: Don't throw if legacy provider is not available
-  #4078: Upgrade bundled SQLite to 3.42 (latest)
-  #4079: SocketConnector: constructor should take SocketAddress by const reference
-  #4071: PageCompiler: add referrerPolicy to page directive
-  updated changelog
-  updated copyright year
-  #4014: wrong string offset in HTTPCredentials::isNTLMCredentials
-  updated release notes
-  #4031: Classes with virtual functions missing virtual destructors (compilation issues)
-  updated changelog
-  #4082: Logger performance improvement with formatting
-  changelog
-  fix haveLegacyProvider for OpenSSL < 3
-  CppParser: fix lookup in base classes
-  merge changes from devel
-  updated changelog
-  branched off poco-1.11.8
-  #4169: Upgrade bundled zlib to 1.3
-  #4171: Poco::FileStream is always opened with std::ios::in | std::ios::out
- ... e mais 34 commits

### Release 4

Link: https://github.com/pocoproject/poco/releases/tag/poco-1.13.1-release
- Tag: `poco-1.13.1-release`
- Nome: Release 1.13.1
- Publicada em: 2024-02-07
- Release anterior (cronológica): `poco-1.13.0-release`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1

-  Release 1.13.1 (#4373)

### Release 5

Link: https://github.com/pocoproject/poco/releases/tag/poco-1.13.2-release
- Tag: `poco-1.13.2-release`
- Nome: Release 1.13.2
- Publicada em: 2024-02-19
- Release anterior (cronológica): `poco-1.13.1-release`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 70

-  doc(ReleaseNotes): fix formatting, add PR links
-  Incorporated Debian patches (#4380)
-  fix(UUID): UUID parser silently ignores too long strings #4375 (#4384)
-  fix(Crypto): EVP_CIPHER_CTX_init is incorrectly defined in Envelope.cpp if it is not defined already by OpenSSL. Fixed to properly use EVP_CIPHER_CTX_reset.
-  enh(ci): Add macos sanitizers job (#4313)
-  enh(ci): macOS thread sanitizer
-  enh(ci): macOS sanitize jobs for undefined and address.
-  fix(test): lock std:cerr to prevent data race in TCP server tests (reported by clang thread sanitizer) #4313
-  fix(test): Use 96-bit IV with aes-256-gcm to fix (#4347):
-  mingw compile and link improvements (#4019) (#4391)
-  enh(DateTimeParser): option to cleanup input string before parsing (#569).
-  fix(CppUnit): do not install #4398
-  fix(DataTest): do not install #4398
-  chore(SingleSocketPoller): spelling
-  fix(MailMessage): Compare lowercase content disposition headers when reading parts (#3650).
-  chore(cmake): CppUnit Foundation dependency documentation; fix indentation
-  fix(SocketReactorTest): deadlock test intermittently hangs #4400
-  gcc/clang (-fvisibility=hidden): corrections to compile and work properly (#4394)
-  Implemented automated network library initialization for Windows MinGW targets (#4402)
-  fix(Thread_POSIX): qnx build error: 'prctl' was not declared in this scope #4404
-  fix: NULL pointer strategy when setting rotation never #4411
-  fix(progen): add LanguageStandard (stdcpp17, stdc11); regenerate vs170 projects
-  Implement GetAdaptersAddresses API (#4419)
-  test(ThreadPool): unit test for thread pool shutdown when no worker is running. (#2450)
-  enh: #4216: use std::string literals
-  enh: #3890: Get rid of SingletonHolder
-  enh(File): Linux, macOS: microsecond precision for file times (create and modification time).
-  enh(tests): Ability to enable/disable testing of deprecated functionality. (#4425)
-  fix(SSLManager): Fixed regression introduced in PR #4103, fixes #4421
-  fix(LogFile): Unify flushing behaviour of WIN32 and STD implementation (#2443)
-  chore(buildwin): remove old vs versions from build and progen scripts; update documentation
-  chore(buildwin): remove leftover closing curly
-  enh(SQLite): SQLite FTS5 #4367
-  Release 1.13.1: Update release notes, changelog, contributors, version files. (#4440)
-  Update CONTRIBUTORS
-  fix(CppParser): Documentation generation (some minor fixes, WiP) #4441
-  feat(CppParser): C++11 attributes support
-  feat(PocoDoc): C++11 attributes support
-  chore(doc): Changelog and release notes formatting
-  fix(CppParser): parsing of function template parameters and namespace imports
- ... e mais 30 commits
