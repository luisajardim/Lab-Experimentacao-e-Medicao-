# aeron-io/aeron

Repositório: https://github.com/aeron-io/aeron

## Metadados

- Linguagem: Java

## Releases sorteadas

### Release 1

Link: https://github.com/aeron-io/aeron/releases/tag/1.8.1
- Tag: `1.8.1`
- Nome: (sem nome)
- Publicada em: 2018-02-28
- Release anterior (cronológica): `1.8.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 63

-  post release bump
-  [Java] Update archive samples so that they are move robust to misuse.
-  [Java] Rework list recording by URI to do a contains match on the stripped channel stored in the archive rather than an equals so the session id based recordings can match.
-  [Java] Script tidy up.
-  [Java] Formatting.
-  [Java] Replay sample to use session specific subscription.
-  [Java] Tidy up archive samples.
-  [Java] Invoke client conductor on slow tick in archive duty cycle.
-  [Java] Only try to send error response when response publication is connected.
-  [Java] Only allow one active listing of recording descriptors per control session at a time.
-  [Java] Break out different control response failure cases.
-  [Java] Don't try to queue errors to a control session that is not accepting responses.
-  [Java] Simplify queued responses as they can only come from the archive conductor thread and not he replay thread anymore.
-  [Java] Reduce call stack with non-concurrent queue usage in session.
-  [Java]: add guard around sessionInterest when removing subscription to handle the case of no traffic having been seen.
-  [Java] Use a reentrant lock on Aeron client when running in dedicated mode.
-  [Java] Only use the aeron client from the conductor thread in the archive.
-  [Java] Clean up error logic in archive replay session.
-  [Java] Remove unused states from recording and replay.
-  [Java] Improve cleanup code for recording sessions.
-  [Java] Set stopped state before sending stopped event in case an error occurs.
-  [Java] Handle case of close failing to send session back from replayer or recorder.
-  [Java] Remove unused method.
-  [Java] Change order of logic to make it easier to read.
-  [Java] Poll for error response from archive in RecordedBasicPublisher.
-  [Java] Reduce allocation in ArchiveTest that was causing large GC pauses.
-  [Java] Replace a number of quietClose operations with close operations so error do not get silently swallowed.
-  [Java] Interrupt background threads on test timeout.
-  [Java] Fix checkstyle rule violation.
-  [Java] Use standard directory for archive tests so they are easier to monitor and debug.
-  [Java] Simpler poll of consuming messages in the archive test.
-  [Java] Close fragment reader with finally block in case of failure.
-  [Java] Have RecordingFragmentReader implement AutoClosable to make test cleanup easy.
-  [C++]: move away from move semantics on Image due to #472.
-  [Java] Be more precise in waiting for recording to have stopped.
-  Merge remote-tracking branch 'origin/master'
-  [C++]: add guard around filling out ADD_COIUNTER command with no key.
-  Merge branch 'master' of https://github.com/real-logic/Aeron
-  [Java] Null check during cleanup of ClusterTest.
-  Merge remote-tracking branch 'origin/master'
- ... e mais 23 commits

### Release 2

Link: https://github.com/aeron-io/aeron/releases/tag/1.33.1
- Tag: `1.33.1`
- Nome: (sem nome)
- Publicada em: 2021-05-14
- Release anterior (cronológica): `1.33.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 47

-  post release bump
-  [Build] Upgrade to Gradle 7.0.1.
-  [Build] Upgrade to Shadow 7.0.0.
-  [Java] Fix setting of socket buffer and receive window lengths from ChannelUri in ChannelUriStringBuilder and use them for ClusterBackup catchup channel default.
-  Revert "[Build] Upgrade to Shadow 7.0.0."
-  Revert "[Build] Upgrade to Gradle 7.0.1."
-  [Java] Only suffix message with exception category when there is a message.
-  [Java] Strip repeated addition of category name suffix for RegistrationException and be consistent with use of InvalidChannelException in Java driver.
-  [C] Remove unused macro.
-  [Java] Error messages.
-  [C] Error messages.
-  [Java] Error messages.
-  [C++] Fix memory leak in shouldNotIgnoreDataAndSetupAfterImageRemovedAndCoolDownRemoved if the test fails.
-  [CI] Retry apt download up to 5 times.
-  [CI] Retry if CMake download fails.
-  [Java] Clarify checking of buffer lengths on channels.
-  [Java] Improve error category stripping from RegistrationException.
-  [C] Clarify validation of buffer lengths on channels and fix warnings.
-  [C] Clarify validation of buffer lengths on channels and fix warnings.
-  [C] Remove unnecessary space.
-  [Java] Avoid send or receive channel leak on invalid configuration.
-  [C] Initialise buffers in terminate test and fix warnings.
-  [C++] Always check for thread being joinable before join to avoid segfault.
-  [CI] Remove Clang 9 while failing.
-  [Java] Add client API for invoking archive with tagged replication and provide the replication channel.
-  [Java] Add missing stop position to replicate calls.
-  [C++] Align Archive replication API with Java.
-  [Java] Try put back Clang 9 and upgrade to Ubuntu 20.04 for Clang to be consistent.
-  Merge remote-tracking branch 'origin/master'
-  [Java] Try put back Clang 9 and upgrade to Ubuntu 20.04 for Clang to be consistent.
-  [CI] Drop older versions of Clang.
-  [CI] Switch to http://apt.llvm.org/focal/ for installing LLVM.
-  [CI] Revert Ubuntu upgrade to Clang and use Clang 10 for debug build.
-  Merge remote-tracking branch 'origin/master'
-  [CI] Try upgrade again to Ubuntu 20.04.
-  [CI] Remove old Clang compilers.
-  [CI] Separate Clang builds.
-  [CI] Naming.
-  [CI] Drop Clang 9 from Matrix.
-  [C++] Add `-fno-omit-frame-pointer -g -O2` to the sanitise build, i.e. improve stacktrace quality and ensure enough optimizations are done to offset the overhead of sanitizers.
- ... e mais 7 commits

### Release 3

Link: https://github.com/aeron-io/aeron/releases/tag/1.45.1
- Tag: `1.45.1`
- Nome: 1.45.1
- Publicada em: 2024-10-24
- Release anterior (cronológica): `1.46.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  [C] Check subscribed sessions before removing a stream interest before removing by stream_id.
-  [Java] Add end-to-end test for session interest fix.
-  Tethering join position (#1672)
-  1.45.1 released

### Release 4

Link: https://github.com/aeron-io/aeron/releases/tag/1.48.5
- Tag: `1.48.5`
- Nome: 1.48.5
- Publicada em: 2025-07-21
- Release anterior (cronológica): `1.44.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  [Java] IngressAdapterTest onFragment before making any changes
-  [Java] IngressAdapter to delegate to ConsensusModuleAgent when schema id is unknown
-  post release bump
-  [C++ Wrapper] Correctly implement tracking of context on the header.
-  [C/C++] Do not compile with `-Ofast` compilation level.
-  [C/C++] Pass custom optimization level to the MSVC compiler.
-  [CI] Fix GCC installation.
-  [Docker] Add missing dependencies + fix user permissions.
-  [Build] Download and install CMake.
-  [C] Build CMake in multiple threads.
-  [C] Fix CMake compilation in CentOS and Rocky.
-  [CI] Cache CMake installation.
-  [CI] Fix MacOS grep peculiarities.
-  [Build] Fix CentOS OpenSSL install.
-  [Build] Update packages before install.
-  [CI] Fix MacOS grep flags.
-  [CI] Use the same grep/cut flags.
-  [Build] Debug libc version.
-  [Build] More debug.
-  [Build] Try CMake 3.26.6 on CentOS.
-  [Build] Use GCC 10 to build on CentOS.
-  [Build] Use openssl-devel.
-  [C/C++] Drop CentOS build.
-  [Java] Fix race when reusing an `Aeron` instance that was created in `ClusterBackup.Context.conclude` and assigned to `AeronArchive.Context`. This instance has no lock and is running in the invoker mode. The net result is sharing non-thread-safe object across the threads.
-  [C] Tidy up aeron_reallocf to work correctly on allocation failure.
-  [C] Expose try_connect_stream method for use from within ATS.
-  [C] Remove unconnected stream message.
-  [C] Fix string format for AERON_SET_ERROR arguments.
-  [Java] Remove unused variable.
-  [Java] When trying to stop consensus modules and services in ConsensusModuleSnapshotPendingServiceMessagesPatchTest stop the leader last to avoid re-election.
-  Add per channel untethered window limit and resting timeouts (#1588)
-  [C++] Add findByTypeIdAndRegistrationId to C++ Wrapper.
-  [Java] Upgrade to ByteBuddy 1.14.14.
-  [Java] Pre-start async task executor threads.
-  [Build] Install CMake binaries instead of building from source.
-  [Build] Fix macOS Cmake installation path.
-  [Build] Fix path on Linux.
-  [Java] Print `serviceId` when throwing "ack out of sequence" exception.
-  Fixed set thread name. (#1594)
-  [C++] Tidy up after merging #1594.
- ... e mais 210 commits

### Release 5

Link: https://github.com/aeron-io/aeron/releases/tag/1.50.1
- Tag: `1.50.1`
- Nome: 1.50.1
- Publicada em: 2026-02-05
- Release anterior (cronológica): `1.50.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 9

-  Fixed aeron_strerror_r (#1930)
-  aeron_driver_agent_log_dissector ipv6 wrong address family (#1926)
-  aeron_alloc_aligned posix_memalign bug (#1927)
-  [Java] Fix Archive CATALOG_RESIZE debug logging.
-  [Cluster] Add alias to follower catchup stream.
-  [Java] Fix single-node cluster leader re-election. (#1932)
-  [Archive] Reject extend recording request if truncation is in progress. Register delete session so that overlapping delete attempts will be rejected.
-  [Java/C] Increase default cycle thresholds to 100ms.
-  1.50.1 released.
