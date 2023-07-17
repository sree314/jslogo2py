//
// Wrapper/Recorder for Turtle Graphics in Javascript
//

// Copyright (C) 2011 Joshua Bell
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

(function(global) {
  'use strict';

  //function deg2rad(d) { return d / 180 * Math.PI; }
  //function rad2deg(r) { return r * 180 / Math.PI; }

  // function font(px, name) {
  //   px = Number(px);
  //   name = String(name).toLowerCase();
  //   if (['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'].indexOf(name) === -1)
  //     name = JSON.stringify(name);
  //   return String(px) + 'px ' + name;
  // }

  // function mod(a, b) {
  //   var r = a % b;
  //   return r < 0 ? r + b : r;
  // }

  function CanvasTurtleRecorder(canvas_ctx, turtle_ctx, w, h, events) {
      this._turtle = new CanvasTurtle(canvas_ctx, turtle_ctx, w, h, events);
      this._cmds = Array();
      this._globals = ["led1", "led2", "emitter", "ir1", "ir2"];
      this._code = null;
  }

  Object.defineProperties(CanvasTurtleRecorder.prototype, {

    // Internal methods

    // _init: {value: function() {
    // }},

    // _tick: {value: function() {

    // }},

    // _moveto: {value: function(x, y, setpos) {
    // }},

    // _mousemove: {value: function(x, y, b) {
    // }},

    // _mouseclick: {value: function(x, y, b) {
    // }},

    // API methods

      is_global_var: { value: function(varname) {
          //console.log(varname + (this._globals.indexOf(varname) != -1));
          return this._globals.indexOf(varname) != -1;
      }},

    add_command: { value: function(cmd) {
      if(cmd[0] == "setvar") {
        if(cmd[1] == "led1") {
          this._turtle.led1 = cmd[2];
        } else if (cmd[1] == "led2") {
          this._turtle.led2 = cmd[2];
        }
      }
          this._cmds.push(cmd);
      }},

      resize: {value: function(w, h) {
          this._turtle.resize(w, h);
    }},

      move: {value: function(distance) {
          this._cmds.push(["move", distance]);
          this._turtle.move(distance);
    }},

      turn: {value: function(angle) {
          this._cmds.push(["turn", angle]);
          this._turtle.turn(angle);
    }},

      towards: {value: function(x, y) {
          //this._cmds.push(["towards", x, y]);
          return this._turtle.towards(x, y);
    }},

      clearscreen: {value: function() {
          this._cmds.push(["clearscreen"]);
          this._cmds = Array();
          this._turtle.clearscreen();
    }},

      clear: {value: function() {
          this._cmds.push(["clear"]);
          this._turtle.clear();
    }},

      home: {value: function() {
          this._cmds.push(["home"]);
          this._turtle.home();
    }},

      drawtext: {value: function(text) {
          this._cmds.push(["drawtext", text]);
          this._turtle.drawtext(text);
    }},

      beginpath: {value: function() {
          this._cmds.push(["beginpath"]);
          this._turtle.beginpath();
    }},

      fillpath: {value: function(fillcolor) {
          this._cmds.push(["fillpath", fillcolor]);
          this._turtle.fillpath(fillcolor);
    }},

      fill: {value: function() {
          this._cmds.push(["fill"]);
          this._turtle.fill();
    }},

      arc: {value: function(angle, radius) {
          this._cmds.push(["arc", angle, radius]);
          this._turtle.arc(angle, radius);
    }},

      getstate: {value: function() {
          this._cmds.push(["getstate"]);
          return this._turtle.getstate();
    }},

      setstate: {value: function(state) {
          this._cmds.push(["setstate"]);
          this._turtle.setstate(state);
    }},

      setcode: {value: function(code) {
	  this._code = code;
      }},

      showcmds2: {value: function() {
          function array2str(a) {
              if(Array.isArray(a)) {
                  return "[" + a.map(x => array2str(x)).join() + "]";
              } else if (typeof a == 'string') {
                  return "'" + a + "'";
              } else {
                  return String(a);
              }
          }

	  var header = ["from jslogort import *\n", /* leave a blank line */
			"jst = JSTurtle()",
			"true = True",
			"false = False",
			"jst.init()",
			"jst.pendown(True)",
			"code = " + array2str(this._code),
			"jst.run(code)"];

          return header.join('\n') + '\n';
      }},

      showcmds: {value: function() {
          //console.log(this._cmds);

          function array2str(a) {
              if(Array.isArray(a)) {
                  return "[" + a.map(x => array2str(x)).join() + "]";
              } else if (typeof a == 'string') {
                  return "'" + a + "'";
              } else {
                  return String(a);
              }
          }

          var code = this._cmds.map(e => "jst." + e[0] + "(" + e.slice(1).map(x => array2str(x)).join() + ")").join('\n')
          console.log(code);
	  var header = ["from jslogort import *\n", /* leave a blank line */
			"jst = JSTurtle()",
			"true = True",
			"false = False",
			"jst.init()",
			"jst.pendown(True)"];

          return header.join('\n') + '\n' + code;
      }},
    // Properties

    pendown: {
        set: function(down) {
            this._cmds.push(["pendown", down])
            this._turtle.pendown = down;
        },
        get: function() { return this._turtle.pendown; }
    },

    penmode: {
        get: function() { return this._turtle.penmode; },
        set: function(penmode) {
            this._cmds.push(["penmode", penmode])
            this._turtle.penmode = penmode;
      }
    },

    turtlemode: {
        set: function(turtlemode) {
            this._cmds.push(["turtlemode", turtlemode])
            this._turtle.turtlemode = turtlemode;
        },
      get: function() { return this._turtle.turtlemode }
    },

    color: {
        get: function() { return this._turtle.color;},
        set: function(color) {
            this._cmds.push(["color", color])
            this._turtle.color = color;
        }
    },

    bgcolor: {
        get: function() { return this._turtle.bgcolor; },
        set: function(color) {
            this._cmds.push(["bgcolor", color])
            this._turtle.bgcolor = color;
      }
    },

    penwidth: {
        set: function(width) {
            this._cmds.push(["penwidth", width])
            this._turtle.penwidth = width;
      },
      get: function() { return this._turtle.penwidth; }
    },


    fontsize: {
        set: function(size) {
            this._cmds.push(["fontsize", size])
            this._turtle.fontsize = size;
      },
        get: function() { return this._turtle.fontsize; }
    },

    fontname: {
        set: function(name) {
            this._cmds.push(["fontname", name])
            this._turtle.fontname = fontname;
      },
      get: function() { return this._turtle.fontname; }
    },

    position: {
        set: function(coords) {
            this._cmds.push(["position", coords])
            this._turtle.position = coords;
      },
      get: function() {
          return this._turtle.position;
      }
    },

    heading: {
      get: function() {
          return this._turtle.heading;
      },
        set: function(angle) {
            this._cmds.push(["setheading", angle])
            this._turtle.heading = angle;
      }
    },

    visible: {
        set: function(visible) {
            this._cmds.push(["visible", visible])
            this._turtle.visible = visible; },
      get: function() { return this._turtle.visible; }
    },

    scrunch: {
        set: function(sc) {
            this._cmds.push(["scrunch", sc])
            this._turtle.scrunch = sc;
      },
      get: function() {
          return this._turtle.scrunch;
      }
    },

    mousepos: {
        get: function() { return this._turtle.mousepos; }
    },

    clickpos: {
        get: function() { return this._turtle.clickpos; }
    },

    button: {
      get: function() { return this._turtle.button; }
    }

  });

  global.CanvasTurtleRecorder = CanvasTurtleRecorder;
}(self));
