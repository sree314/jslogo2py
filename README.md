# jslogo2py

This is a fork of [jslogo](https://github.com/inexorabletash/jslogo/) that is modified for use in a Logo workshop where students wrote Logo programs and ran it on the [Open Source Turtle Robot](https://github.com/aspro648/OSTR/). To achieve this, I wrote `turtlerecord.js` which interposes between `logo.js` and `turtle.js` to record all turtle [graphics] commands as a trace. These turtle commands are converted to CircuitPython and executed using a special runtime (`jslogort.py`) that interfaces to the OSTR libraries.

To use this, write a Logo program as usual and use the `Save to
Turtle` link to save `turtlecode.py` to the `CIRCUITPYTHON` drive. The
turtle should give two beeps and wait for a button press before
executing the Logo program.

Since this captures a trace, some control flow (e.g. `repeat forever`)
will not work as expected. For the same reason, some features of the
turtle robot: the IR emitters, the button, and the piezo speaker are
not exposed to the Logo interpreter. The LEDs are available as two
boolean variables `led1` and `led2`.

Like the original code, the modifications are licensed under the
Apache License, version 2.0. The copyright is owned by the University
of Rochester.

Original README contents below:

jslogo - Logo in JavaScript
===========================

This is hosted at https://inexorabletash.github.io/jslogo/ for playing with live.

[Language Reference](https://htmlpreview.github.com/?https://github.com/inexorabletash/jslogo/blob/master/language.html) -
this attempts to implement a subset of [UCBLogo](https://www.cs.berkeley.edu/~bh/v2ch14/manual.html)
defined in in *Brian Harvey's Computer Science Logo Style*

Logo Examples
-------------
    to star repeat 5 [ fd 100 rt 144 ] end
    star
    to square :length repeat 4 [ fd :length rt 90 ] end
    repeat 36 [ square 50 rt 10 ]
    to randomcolor setcolor pick [ red orange yellow green blue violet ] end
    repeat 36 [ randomcolor square random 200 rt 10 ]
    window pu repeat 72 [ setlabelheight repcount fd repcount * 2.5 label "Logo bk repcount * 2.5 rt 10 ]

Logo Links
----------
* [Logo](https://en.wikipedia.org/wiki/Logo_%28programming_language%29) on Wikipedia
* Other Logo implementations that run in a Web browser:
  * [papert - logo in your browser](http://logo.twentygototen.org/) ([source code](https://code.google.com/p/papert/))
  * [Curly Logo](https://github.com/drj11/curlylogo)
* [The Logo Foundation](http://el.media.mit.edu/logo-foundation/)
* [Berkeley Logo (UCBLogo)](https://www.cs.berkeley.edu/~bh/logo.html)
* [The Logo Tree Project](http://elica.net/download/papers/LogoTreeProject.pdf)
* [Ian Bicking on Logo](http://blog.ianbicking.org/2007/10/19/logo/)
* [PyLogo](http://pylogo.sourceforge.net/)
* [Introduction to Computer Programming](http://www.bfoit.org/itp/itp.html)

To Do
-----
* Document deviations from UCB Logo standard
* Make these examples all work: [Logo 15-word challenge](http://www.mathcats.com/gallery/15wordcontest.html)
* Tail-call optimization
* Make execution async so you can watch the turtle move
