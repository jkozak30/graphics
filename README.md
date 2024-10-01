### Julia Kozak - Graphics Final

Here is a summary of my added features. Each entry gives a sample command format, with parameters (type and name) in brackets ```[]``` and optional parameters in parentheses ```()```.

---

```icosahedron (SYMBOL color) [NUMBER cx] [NUMBER cy] [NUMBER cz] [NUMBER s]```

- This command draws a regular icosahedron centered at (cx, cy, cz) with side length 2s.
- Its reflective constants can be changed using the pre-defined color.

---

```light [SYMBOL name] [NUMBER r] [NUMBER g] [NUMBER b] [NUMBER x] [NUMBER y] [NUMBER z]```

- This command allows the addition of multiple light sources. This creates a light with color (r, g, b) and location vector (x, y, z), and it is stored in the symbol table as name.
- Each light will be applied only to objects listed after it in the script.

---

```frames [NUMBER f]```

```basename [TEXT name]```

```vary [SYMBOL knob] [NUMBER start_frame] [NUMBER end_frame] [NUMBER start_value] [NUMBER end_value] (NUMBER vertex)```

- These commands allow for the creation of individual frames for an animation. 
- ```frames``` defines the total number of frames created in the animation, and these will be 0-indexed. 
- ```basename``` specifies a prefix to each filename when frames are generated. For example, a basename of ```cat``` with 20 frames will generate ```cat0000.png, cat0001.png, ... , cat0019.png```.
- ```vary``` allows you to specify the duration and scale of your transformation. If you want to animate a given transformation, a knob name should be placed at the end of it. 
  - If the last parameter is not present, then the transformation will be scaled linearly from start_value to end_value over the duration.
  - The last parameter allows for quadratic scaling with two options. If the value is positive, it will scale as if your start_value/start_frame are the vertex of the parabola (velocity starts at 0). If it is negative, the end_value/end_frame are the vertex of the parabola (velocity ends at 0).
- The frames can be converted to a gif format using ```make convert```, and old frames can be deleted using ```make clean```.

---

