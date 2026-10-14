# pollen-robotics/microduck

Repositório: https://github.com/pollen-robotics/microduck

## Metadados

- Linguagem: Rust

## Releases sorteadas

### Release 1

Link: https://github.com/pollen-robotics/microduck/releases/tag/daemon-v0.3.0
- Tag: `daemon-v0.3.0`
- Nome: daemon 0.3.0
- Publicada em: 2026-08-07
- Release anterior (cronológica): `daemon-v0.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 87

-  btd: the transport-independent half, with no radio
-  btd: the BLE service, end to end but for the radio
-  configd: wifi and the robot's identity
-  btctl: a BLE client for a laptop
-  robotctl net/system, and a PIN-based pairing process
-  Make the new daemons actually run on a board
-  board-test: cover configd's authorisation, and name failed units
-  The app may update the robot, and pairing is the PIN alone
-  docs: the app path, and three claims the board disproved
-  Merge main: slice 2's intents, and BLE refuses all of them
-  README: drop the slice-1 status bullet the merge kept alive
-  cargo fmt
-  configd: two clippy lints my toolchain was too old to see
-  Package the new units, and a test so this cannot happen again
-  monitor: joints, and a frame instead of a scroll
-  updater: restart units one at a time, and skip one this board lacks
-  Merge remote-tracking branch 'origin/main' into btd-ble-service
-  Merge main: the health field that made the branch un-installable
-  Stage configd and btd, and derive that from the units
-  robotctl: configd is not behind just because the release is a prerelease
-  btd: use bluer's callback model, because the IO model never receives anything
-  monitor: say what every number is
-  docs: record the API_VERSION skew between robotctl and updaterd
-  monitor: name the policy, not just its mode
-  provisioning: make a fresh board's own advice runnable
-  robotctl: a refused socket is not a stopped daemon
-  install: close the group gap with one command, and document DUCK_DEV_KEY
-  deploy: one variable to set, and every command self-contained
-  deploy: keep DUCK_TOKEN across the two provisioning reboots
-  deploy: put the two commands-only paths first
-  deploy: cut the section the quickstart replaced
-  provision: one script over the three, and no newgrp
-  Install the release's units from a postinstall hook
-  btd: a write must not await, or chunks swap places
-  provision: account for the token that is meant to stay
-  btd: make the queue-depth invariant a compile-time assertion
-  provision: take the reboot, resume unattended, keep a log
-  btd: a read forces the bond, because a subscribe cannot
-  provision: the dev key belongs in the command, not a footnote
-  provision-board: one command, from your own machine
- ... e mais 47 commits

### Release 2

Link: https://github.com/pollen-robotics/microduck/releases/tag/daemon-v0.11.0
- Tag: `daemon-v0.11.0`
- Nome: daemon 0.11.0
- Publicada em: 2026-09-07
- Release anterior (cronológica): `daemon-dev-relay-session`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 18

-  btd, mediad: a restarted daemon gets the next request, not the one after
-  padd: Start once stands the robot up, Start again drives
-  padd: Select press = robot.relax (torque off)
-  robot.rebootMotors: reboot servos in place, `robotctl robot reboot-motors`, D-pad right on the pad
-  robotd: claim the IPC socket before starting control
-  robotd: cover concurrent startup and saturated listeners
-  Merge pull request #219 from pollen-robotics/relay-session
-  Merge pull request #203 from pollen-robotics/reboot-motors
-  Merge main: Start's two presses and DPad-Right's reboot in one pad
-  Merge main: DPad-Right reboots the servos, Select drops torque
-  robotd: hold the endpoint lock throughout standalone init
-  Merge pull request #212 from pollen-robotics/select-relax
-  Merge main: Select's torque off and Start's two presses in one pad
-  Merge pull request #218 from tianrking/fix/robotd-single-instance
-  Merge pull request #210 from pollen-robotics/start-twice
-  Merge pull request #207 from Nixxx19/a-restarted-daemon-gets-the-next-request
-  Prepare release 0.11.0
-  Merge pull request #222 from pollen-robotics/prepare-release-0.11.0

### Release 3

Link: https://github.com/pollen-robotics/microduck/releases/tag/daemon-v0.13.0
- Tag: `daemon-v0.13.0`
- Nome: daemon 0.13.0
- Publicada em: 2026-09-15
- Release anterior (cronológica): `daemon-dev-slam-bench-truth`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 133

-  robotd: refuse a non-socket path before bind, on every platform
-  Support explicit-state LSTM ONNX policies in the robot runtime
-  A Space that puts a policy from the Hub onto a duck in one click
-  A second way in, because the click needs a candidate pair and TURN has none
-  The camera was streamed and unchecked, which is not the same as working
-  The 401 was Gradio's mock token, and the log now says so without asking me
-  A venv beside the Space, so `uv run app.py` is the command it looked like
-  The page says which tab a Space can serve, because that is not guessable
-  The robot dials a Space and pushes H.264, because a relay candidate is what §6 has not got
-  Two Spaces speak one protocol, so there is one copy of the client
-  vision-demo receives the frames instead of pulling them, and six findings about Spaces
-  policy-shop: an empty picture box says why, and the geometry is asked for
-  rustfmt and clippy over this branch's files
-  Take the mount angle from where `main` resolves it, not from the flag
-  The linux-only encoders go before the test module, not after it
-  robotd: drop non-finite command targets instead of poisoning the command filters
-  kinematics: an empty band is no hand even when min_zones is 0
-  The valve is the valve, not the queue in front of it
-  The frame poll follows the stream, so an idle page costs the Space nothing
-  `duckctl logs`: a daemon's last words, over the radio
-  mediad: answer one raw frame on a local socket (media.frame)
-  Adopt a factory-fresh servo as the one joint that stopped answering
-  btd: size a reply for the link, and stop calling a full queue a disconnect
-  Take the Hugging Face login from hf-robot-account rather than carrying it
-  Merge pull request #243 from pollen-robotics/motor-replacement
-  robotd: one line a minute for an ordinary dropped bus read, not one a second
-  Depend on hf-robot-account from crates.io rather than from a commit
-  system.logs: say where the daemon restarted
-  Merge pull request #240 from pollen-robotics/duckctl-logs
-  Merge pull request #244 from pollen-robotics/use-hf-robot-account
-  Merge main: the account token now comes from `hf-robot-account`
-  configd: a classic (BR/EDR) pad is paired before it is connected
-  Merge pull request #236 from pollen-robotics/policy-space
-  Merge pull request #238 from hadelan/fix/nonfinite-command-targets
-  Merge pull request #239 from hadelan/fix/empty-band-min-zones
-  configd: a pad that presents as two devices is one candidate, and the classic face wins
-  The theremin ships off, like the chorale
-  configd: a name-only gamepad match never ends the search early
-  configd: the classic pairing path has now run on hardware, and the docs say so
-  Spec: the head sensors when nobody is looking
- ... e mais 93 commits

### Release 4

Link: https://github.com/pollen-robotics/microduck/releases/tag/daemon-v0.14.3
- Tag: `daemon-v0.14.3`
- Nome: daemon 0.14.3
- Publicada em: 2026-09-21
- Release anterior (cronológica): `daemon-v0.14.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 16

-  playground: sign in the way telepresence does, and stop trusting a dead token
-  Merge pull request #310 from pollen-robotics/oauth-like-telepresence
-  console: sign in the way telepresence does, and stop trusting a dead token
-  Merge pull request #311 from pollen-robotics/console-oauth-like-telepresence
-  console: make the page say what is available and what went wrong
-  console: the alert box was visible from page load, empty and red
-  Merge pull request #312 from pollen-robotics/console-ui
-  btd: stay discoverable while a central is being served
-  btd: the chorale beacon is a broadcast, not a peripheral
-  docs: what a busy robot advertises, and what duckctl says about it
-  Merge pull request #313 from pollen-robotics/btd-advertise-while-connected
-  policy search: say what each policy is, and show it
-  duckctl: render a search the way robotctl does
-  Prepare release 0.14.3
-  Merge pull request #314 from pollen-robotics/policy-search-descriptions
-  Merge pull request #315 from pollen-robotics/prepare-release-0.14.3

### Release 5

Link: https://github.com/pollen-robotics/microduck/releases/tag/daemon-v0.15.2
- Tag: `daemon-v0.15.2`
- Nome: daemon 0.15.2
- Publicada em: 2026-10-05
- Release anterior (cronológica): `daemon-dev-midi-instrument`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 12

-  expose control max vx/vy/vtheta etc in robotctl configure
-  Merge pull request #345 from pollen-robotics/configure-controller-limits
-  robotd: pause the policy while the robot is held ([pickup], off by default)
-  robotd: ease into a recorded rest pose before the shutdown cuts torque
-  Merge pull request #347 from pollen-robotics/shutdown-rest-pose
-  pickup: v2 model — head grips, any orientation, 180° turns; a third the size
-  Merge remote-tracking branch 'origin/main' into pickup-detector
-  pickup: on by default
-  pickup: report being picked up as a state, not a policy
-  Merge pull request #349 from pollen-robotics/pickup-detector
-  Prepare release 0.15.2
-  Merge pull request #356 from pollen-robotics/prepare-release-0.15.2
