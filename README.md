# PY-BASIC
Py-Basic is a transpiler that converts simple Python code to TI-Basic (the programming language built into the TI-84 Plus CE Graphing Calculator). I may add additional compatibility later but the TI-84 Plus CE is the current target.

The name is a combination of the name "Python" and "TI-Basic" put together. It sounds cool enough to me and it conveniently happens to be 8 characters long (the max program name size on TI Graphing Calculators).

I haven't led any coding projects before so this is all very new to me haha.

So far, there isn't much functionality and it will probably take a while to implement enough for this to actually be useful.

Note: Some parts of the program may refer to compilation, but in reality, Py-Basic is more like a transpiler. The biggest part is converting Python to TI-BASIC code. Converting that to a binary that can be uploaded to the TI-84 is actually the easiest part.

Legal Note: NOT affiliated with Texas Instruments. No violation of trademarks or copyright intended. Please do not hunt me down.

# Writing & Testing Programs
The TI-84 runs programs from top to bottom, has a limited list of variables (a-z and θ), and many functions that don't have a direct equivalent in Python.

To help you out, a boilerplate program has been made with all variables initialized, an import statement for the compatibility file, and "start" and "init" sections. The TI-84 calculator reads files from top to bottom and runs functions as they are defined, a feature not native to Python. To address this, define your starting function after the comment "# \_\_START__ " and call it after the comment "# \_\_INIT__ ". Refer to the "sample.py" program to see a demonstration of various capabilities of Py-Basic.

The "libTIcompatibility.py" file adds some helpful functions that allow you to test your program as you code it while remaining assured that it will work on the calculator. Oftentimes, these functions have an easier time transpiling because they are closer to actual TI-BASIC code.

Programs should still work in Python. If a feature has not been implemented yet and the transpiler cannot convert it, the file "pybasic.py" will show you the error if you change the target_name variable to your file's name and run.

# Transpiling
Py-Basic breaks transpilation down into a few simple steps in the "main.py" file:
1. Convert the Python program into TI-BASIC (or something very closely ressembling it) --> pybasic.py
2. Convert the TI-BASIC into hex that is compatible with the TI-84 --> pybasic.py
3. Put it all together into a .8xp file that can be uploaded directly to your calculator! --> lib8xp.py

# Thanks
A huge thanks to TI-Basic Developer Wiki:
http://tibasicdev.wikidot.com/homescreen

For .8xp file structure:
https://gist.github.com/SimonEast/244a0fd04526ea1acbec2e2ceb2e7924

For token decoding:
https://gist.github.com/SimonEast/78e8ee29b2bf6c8c9bb34b0cbda00fd0
