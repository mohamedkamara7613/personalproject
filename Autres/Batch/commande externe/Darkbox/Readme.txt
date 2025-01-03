 __        __        __   __
|  \  /\  |__) |__/ |__) /  \ \_/
|__/ /~~\ |  \ |  \ |__) \__/ / \

Darkbox fully portable fast I/O server, powerfull graphic command
Fully compatible with Dos9 Project.

Syntaxes:
1) (process, code or "launcher" part) | darkbox
2) darkbox -i[k/m] | (process, code or "launcher" part)
3) darkbox -w t
4) darkbox -h
5) darkbox -k[_]
6) darkbox -[m/y]

1) Start darkbox as output server.
2) Start darkbox as input server.
  k: Keyboard only, m: Mouse only, nothing: both
3) Wait t ms.
4) Return 1 if data is available in stdin,
   should be used for non-blocking input.
5) Returns the keycode of the next key pressed, with '_', don't
   wait and return immediatly with 0 if there is no input.
6) Wait for a mouse event :
    -m : Wait for any non-movement event.
    -y : Wait for any event.
   Then print to stdout the event.
   Event format : x y btn

NOTE: darkbox support both '-' and '/' as command prefixes.

Output commands passing:
  Commands pass to stdin, so any command like type, more, echo,
  <nul set/p "=text" or whatever you can imagine send command to darkbox.

  So, you can store commands to files to reuses them easly, like sprites or
  something else.

  Also, darkbox accept both new syntax ('-') and batbox/tinybg syntax ('/') to
  begin command.

Output command format:
  Commands follow this format

  -(execution_count)<commands as letters>
  REMARK: '-' can be replaced by '/'

  So each <commands as letters> run (execution_count) times (or 1 time if undefined).

  NOTES:
    - You can escape chracters (" or spaces without double quotes) with '\'
    - With double quotes, new lines are considerated as characters like any others.
    - No commands will produce an error (Parsing error: No command specified).
    - Commands should be in litterals ONLY (Parsing error: Invalid litterals)
    - Commands are case-insensitive.

  TRICK:
    You can write your commands througth multiples echoes :
      echo -5dn "This is a"
      echo      "small text"
      echo      "throught"
      echo      "multiples"
      echo      "lines"

Launcher (and working variations) :
  Official launchers:
    Original (first):
      @Echo off
      call game.bat | darkbox

    Original with Input server:
      @Echo off
      darkbox -i | call game.bat | darkbox

    Enhanced (only in one file) :
      @Echo off
      if defined __ goto :(code)
      set __=.
      call %0 %* | darkbox
      set __=
      pause>NUL
      goto :eof

      "call" is facultative

    Enhanced with Input server
      @Echo off
      if defined __ goto :(code)
      set __=.
      darkbox -i | call %0 %* | darkbox
      set __=
      pause>NUL
      goto :eof

      "call" is facultative.

  Unofficial launcher (variants) :
    @echo off
    if not defined $ (
        set "$=1"
        (
          call "%~f0" %*
        ) | darkbox
        exit/b
    )

Output commands reference :
  ASCII :
    -a Integer

    Usage: Print the character corresponding to the integer.

  Newline :
    -n

    Usage: Go to the next line.

  Color :
    -c color
    'color' is in hexadecimal format.

    Usage: Change the current color.
      - 0xF0: Background
      - 0x0F: Foreground

  Goto :
    -g x y

    Usage: Move cursor to (x;y).

  Jump :
    -j x y

    Usage : Move cursor to offset (x;y) from current position.

    NOTE : Ignores origin.

  Hide/Show cursor :
    -h 0/1

    Usage: Hide or show cursor.

  Clear Screen :
    -s

    Usage: Clear console.

  Origin :
    -o x y

    Usage: Change goto origin.

  Reset :
    -r

    Usage: Reset foreground and background colors.

  Quit :
    -q

    Usage: Properly stop darkbox.

  Wait :
    -w t

    Usage : Wait t miliseconds.

    NOTE : Wait is internal to darkbox, it
           do not interrupt batch execution.

    REMARK : Wait flush stdout even if t is null.

  Line :
    -l Ax Ay Bx By

    Usage : Draw a line from A to B.

    NOTE : Uses the console background color as line color.
           Reason : Use spaces as character which is faster and more cross-platform.

  Box :
    -b x y w h hollow

    Usage : Draw a box.
    NOTE : Uses the console background color as line color.

  Circle :
    -i x y r

    Usage : Draw a circle.
    NOTE : Uses the console background color as line color.

Input callback reference :
  Mouse :
    m x y b

    x: Mouse X position
    y: Mouse Y position
    b: Mouse button

  Keyboard press:
    k key

    key: Key code.

List of supported mouse buttons :
  0: NOTHING (mouse movement)
  1: LEFT_BUTTON
  2: RIGHT_BUTTON
  3: DOUBLE LEFT_BUTTON
  4: DOUBLE RIGHT_BUTTON
  5: MIDDLE_BUTTON
  6: SCROLL_UP (portability issues known (Win32))
  7: SCROLL_DOWN (portability issues known (Win32))
  8: RELEASE

Build defines :
  Note : All CORE_* build defines can also be used in others
         core-based projects such as cbatbox_core and ctcs_o_core.

  CORE_NO_CONSOLE :
    Use a dummy core implementation, which have functions that do nothing.

  CORE_USE_ANSI :
    (default on non-Windows platforms)
    Use standard ANSI sequences to implement the console API.

  CORE_USE_WINAPI :
    (default on Windows platforms)
    Use Windows Win32 API to implement the console API.

  CORE_WIN_HYBRID : (Windows only)
    Use ANSI backend if Windows 10 Virtual Terminal Sequences feature is
    supported, fallback to WinAPI if not supported.

  CORE_W10_ANSI : (Windows only)
    (implies CORE_USE_ANSI)
    Enable Windows 10 Virtual Terminal Sequences feature in
    darkbox and use ANSI sequences to implement the console API.

See also :
  Official post : http://batch.xoo.it/t5526-Dev-Darkbox-TSnake41.htm
  Snake game : http://batch.xoo.it/t5614-Batch-Snake-IK-DC.htm
  Exquation : http://batch.xoo.it/t5654-Batch-Exquation-IK-DC.htm

  tests for examples of uses

  C library core and core_i in "lib" directory (part of darkbox project)

  Dos9 project : dos9.org
