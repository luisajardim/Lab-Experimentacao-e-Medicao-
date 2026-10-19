# love2d/love

Repositório: https://github.com/love2d/love

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/love2d/love/releases/tag/0.6.2
- Tag: `0.6.2`
- Nome: LÖVE 0.6.2 [Jiggly Juice]
- Publicada em: 2020-01-12
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/love2d/love/releases/tag/0.7.0
- Tag: `0.7.0`
- Nome: LÖVE 0.7.0 [Game Slave]
- Publicada em: 2020-01-12
- Release anterior (cronológica): `0.6.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 178

-  Added tag 0.6.2 for changeset db7cd0682883
-  Welcome back, love.thread.
-  added Source:play(), Source:pause(), etc.
-  I'm stupid and forgot to add return statements to the new functions
-  should fix gcc warning about passing a const char * to SDL_putenv
-  replaced a hardcoded radian conversion with the appropriate macro
-  being a genius, forgot to include the header file that defines said macro. fixed now.
-  Added source:isStatic()
-  Updated the OS X version to use Apple's UTI stuff for .love files
-  fixed a typo in the comments of three love.physics functions (I'm being very useful)
-  I'm not entirely sure why ModPlugDecoder.cpp was #including set.h, but it certainly doesn't need to be...
-  Source::pause (and resume, and rewind) was acting on every Source, not just itself. Fixed.
-  Warning fix as in bug #188
-  Fixed setFixedRotation enabling other flags (bug #190)
-  added get/setGroupIndex to CircleShape and PolygonShape
-  Added sound input and recording functionality.
-  We now return nil instead of a null SoundData when getting recorded data fails.
-  EncodedImageData was implemented really stupidly. Now it's less stupid.
-  Cleaned up getting wrap and filter modes for Images.
-  love.audio is now smarter about finding a microphone for input; this should hopefully unbreak ALSA.
-  Switched to 8000Hz for recording, because 44.1KHz is way overkill
-  replaced a few hardcoded radian->degree conversions with LOVE_TODEG
-  Added FontData class, preparing for overhauling love.graphics' Font class
-  Overhauled ImageRasterizer, fixed a bunch of other crap, getting ready to poke around in love.graphics
-  Made font module officially properly exposed to Lua
-  added varargs version of luax_convobj (for making Rasterizers)
-  did a bunch of other stuff, sorry about the monolithic changeset but the diffs should be understandable enough
-  fonts now work (seemingly) as well as they used to
-  Removed the last vestiges of the old, bad font code
-  some final changes to make it work better, and to fix how printf displayed
-  Changed message of error_printer and made it local, also made the debug table an upvalue, so people can use the debug variable in their programs
-  heh whoops accidentally reverted to lower-left origin, fixed
-  Modified output of error_printer to no longer show the error handlers or the 'main chunk'
-  Modified output of error_printer to no longer show the error handlers or the 'main chunk'
-  Accidental commit before, this one works, and produces correct output on a direct call to error_printer
-  merged in bartbes' error-handling changes
-  Prevent error when setting an incompatible FSAA value (warning is displayed)
-  merged in bartbes' FSAA checking
-  Fixed bug/epic fail in loader
-  Should now fall back to no FSAA when it is not available at all
- ... e mais 138 commits

### Release 3

Link: https://github.com/love2d/love/releases/tag/0.8.0
- Tag: `0.8.0`
- Nome: LÖVE 0.8.0 [Rubber Piggy]
- Publicada em: 2020-01-12
- Release anterior (cronológica): `0.7.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 477

-  First draft of release error screen.
-  Make love.joystick 1-indexed
-  Threads get/set instead of send/receive (issue #166)
-  Merge 'default' into 'minor'
-  Handle invalid index in love.joystick, but then 1-indexed (bug #172)
-  Revert that last commit, the wrappers already handle the offset
-  merge default into minor
-  start new font stuff branch
-  trashed old unnecessary font stuff - compiles, but obviously will not work yet
-  the merge screwed up the new thread API, fixed
-  brutally murdered padding and predefined glyph loading
-  New font engine is implemented and appears to work perfectly. Bugs may be discovered and the internals can certainly be optimized and improved (at some point, perhaps, a less naive packing algorithm would be nice) but for now, it's good to go.
-  merged in new font engine
-  closing newfont, its purpose has been served
-  and cutting off its head
-  Allow selection of modules
-  Fixed a couple of compiler warnings in minor branch
-  added the UTF8-CPP library for unicode support, and added unicode printing support.
-  windows.h #defines min/max by default, causing problems with std::[min, max].
-  Updated MSVC2010 project files with changes from 'newfont' branch.
-  Merge default into minor.
-  Merge Framebuffer:set/getWrap to minor
-  fixing font-related segfault bug, thanks to itsnotabigtruck
-  Merge...
-  Change love.graphics.setBackgroundColor() to accept alpha values.
-  Turn of auto color clearing in Framebuffer::startGrab().
-  Add framebuffer:clear(r,g,b,a) (issue #134).
-  merge default into minor
-  fixed framebuffers being filled with garbage when created
-  start box2d update branch
-  bring in new version of Box2D and update #include paths
-  add new joint enums (no implementation yet)
-  making a stab at updating Shapes
-  some more Shape fixes
-  updating the Joints
-  Move luaopen_love_image from love.image to love.image.devil
-  Move luaopen_love_sound to love.sound.lullaby
-  Move luaopen_love_audio to love.audio.openal
-  Rename loaders to fit their locations
-  Added love.audio.null loader
- ... e mais 437 commits

### Release 4

Link: https://github.com/love2d/love/releases/tag/0.10.0
- Tag: `0.10.0`
- Nome: LÖVE 0.10.0 [Super Toast]
- Publicada em: 2020-01-12
- Release anterior (cronológica): `0.9.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 521

-  Merged default into minor
-  Removed love.graphics.get/setPointStyle. ‘rough’ points are now the only possibility (resolves issue #581).
-  Added Source:getType, removed Source:isStatic (resolves issue #776)
-  Removed spaces from love.audio enum strings (resolves issue #733)
-  Merged default into minor
-  Removed functions that were deprecated in 0.9.1
-  OpenGL 2.1 is now required to use love.graphics (resolves issue #779.)
-  Merged default into minor
-  Renamed blend modes "additive", "subtractive", and "multiplicative" to "add", "subtract", and "multiply" (resolves issue #864)
-  Changed the screen_coords parameter of the effect function in pixel shaders so y+ is down instead of up (resolves issue #435.)
-  Merged default into minor
-  Removed love.window.getWidth/getHeight. Use love.graphics.getWidth/getHeight or love.window.getMode instead.
-  Merged default into minor
-  Removed the 'wu' and 'wd' constants for love.mousepressed, added new love.wheelmoved(x, y) event callback.
-  Removed the DevIL backend from love.image. Replaced it with PNG and JPEG encoders/decoders via LodePNG, zlib, and libjpeg-turbo.
-  Aesthete: Bug #829: Refactored all spatial stereo exception messages to static
-  Aesthete: Bug #829: Adding missing exception guards to audio source wrapper.
-  Backed out changeset: 6efefad30fe1
-  Backed out changeset: a0191140525e
-  Aesthete: Bug #829: Added exceptions for all spatial audio calls on stereo
-  Removed love.filesystem.exists (resolves issue #641.)
-  Fix some pointer type conversion errors in MSVC.
-  Merged default into minor
-  Merged default into minor
-  Changed SpriteBatch:add/set to do an internal bind, and love.graphics.draw(SpriteBatch) to do an internal unbind. Removed SpriteBatch:bind/unbind, and added SpriteBatch:flush.
-  Removed some OSX-specific code
-  Don't accidentally enable point smoothing on setMode
-  Fixed ImageData:encode
-  Fixed the no-game screen
-  Added support for loading TGA and BMP images (via stb_image.) Added support for encoding ImageData to TGA.
-  SpriteBatches are a little more intelligent about how much data they upload to the GPU when they're flushed or drawn, now
-  Merged default into minor
-  Changed love.graphics.newImage's optional second argument to be a table of flags. Current flags are 'mipmaps' and 'srgb'.
-  Merged default into minor
-  Merged default into minor
-  Merged default into minor
-  Replaced love.graphics.isSupported and love.graphics.getSystemLimit with love.graphics.getSupported and love.graphics.getSystemLimits, which return tables with graphics feature / system limit enum names as keys, and support status / limit numbers as values.
-  Error when the second argument to love.graphics.newImage isn't a table.
-  Merged default into minor
-  Merged default into minor
- ... e mais 481 commits

### Release 5

Link: https://github.com/love2d/love/releases/tag/11.2
- Tag: `11.2`
- Nome: LÖVE 11.2 [Mysterious Mysteries]
- Publicada em: 2020-01-12
- Release anterior (cronológica): `11.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 36

-  Fix building with non-mega CMake
-  Restore lua 5.2/5.3 compatibility (fixes #1408)
-  Export luax_resume for windows
-  Fix the explicit format + Data argument variant of love.data.decompress.
-  CMake: Also look for headers in include/luajit-2.1.
-  Always link against pthread when using autotools (resolves #1410)
-  Merged in coffeecat/love (pull request #103)
-  Fix cmake policy warning
-  fixed not being able to remap gamepads by resolving problem with re-initializing joysticks as gamepads
-  Added tag 11.1 for changeset 0ab246b5045d
-  Added body:getTransform method
-  Added body:setTransform method
-  Renamed arguments in setTransform method. Merge setters in to one lamba
-  Fix link error in Mac OS X build (Xcode)
-  Merged in elemel/love/elemel/fix-freetype-link-error-on-xcode-macosx (pull request #109)
-  Merged in daviel/love/bodygettransform (pull request #107)
-  Add a hard version dependency between the love and liblove debian packages
-  Fix an uninitialized variable causing (harmless) OpenGL errors. Resolves issue #1434.
-  setCanvas: rephrase confusing error message.
-  Keep a reference to the SDL video subsystem in the mouse module, since cursors need it. Potentially resolves issue #1388.
-  Optimize StreamBuffer::getUsableSize to not be a virtual method.
-  Add an ARM NEON simd implementation of matrix multiplication.
-  Remove extern declaration of std::vector<std::string>::emplace_back to fix compliation with MSVC
-  Fix Windows version of __PHYSFS_platformCalcUserDir after Update 1809
-  Add Source:setAirAbsorption() and Source:getAirAbsorption()
-  Update Xcode project with the latest changes from Xcode 10.
-  Update changelog
-  Update version to 11.2
-  Place Android Java codes to platform
-  Modify openURL to return boolean from Java side
-  Request external storage
-  Rationale confusion
-  Move java files to love-android repo
-  Copy the data size of old uniforms to the new uniform when reinitializing shader uniforms after love.window.setMode.
-  Merged in AuahDark/love/android-fix (pull request #116)
-  Add release date for 11.2.
