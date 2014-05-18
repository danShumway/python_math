Python Math: Adder's Garden Adventure
===========

A puzzle game designed to teach early math concepts about addition, subtraction, and order of operation.

Guides to code submission
===========

- Overcomenting is better than undercommenting
  - within reason of course, it's better to assume someone won't understand what's going on.
- Use detailed commits/pull requests: 
  - explain what changes you made and why they were made.
- Don't break anything when you commit.
  - The game should still run when you commit, double check to make sure.

Other good things to do
=============

- Use the issue tracker.
  - Log bugs.
  - Comment on the issues/features that you're working on.
  - If you are working on something and there isn't an issue for it, create one.
    - this helps us see what's being done
    - keeps us from duplicating work
    - makes a wonderful, busy, pretty looking repository for inclusion on resumes.
  - If you're working on an issue, assign it to yourself
    - That way, if you want to work on something and you're not sure what to do, you can just claim any issue that looks fun and isn't already assigned.

Running on Windows
============

- Open up source/dev_launcher.py in an editor (we recommend IDLE) and run it.

Compiling for the XO
============

- From a command line, run source/init.py.
- The command line will ask for some input, use the name PythonMath, the unique name PythonMath, and the version number 1.0.
- Drag in setup.py then add a space, then "dist_xo" (without quotes).  This will generate a MANIFEST file in the same directory, as well as a dist folder with a .xo file.
- Start up the OLPC and plug in the flash drive. Then head to the terminal activity. Check to see if your flash drive is registered by moving the mouse to the top left corner. This will minimize the activity window and reveal some options on the top left and bottom right of the screen. Look for the USB icon on the bottom right corner of the screen and move your mouse over it. It should display the USB drive’s name and its file path. The one I use is named “USB20FD” and the path is “/run/media/olpc/USB20FD/” yours should be something similar. In the terminal window type “sugar-install-bundle”, then a space, then the path to the .xo file. Mine is always like this: "sugar-install-bundle /run/media/olpc/USB20FD/PythonMath.xo"

