import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    framect = 1
    basenm = 'img'

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light =[[0.5,
              0.75,
              1],
             [255,
              255,
              255]]
    # [[0.5,
    #           0.75,
    #           1],
    #          [255,
    #           255,
    #           255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    b = parseAnimation(commands, symbols)

    if b:
        return

    for command in commands:
        print(command)
        c = command['op']
        args = command['args']

        if c == 'box':
            if command['constants']:
                reflect = command['constants']
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
            reflect = '.white'
        elif c == 'sphere':
            if command['constants']:
                reflect = command['constants']
            add_sphere(tmp,
                       args[0], args[1], args[2], args[3], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
            reflect = '.white'


        elif c == 'icosahedron':
            # print(args)
            if command['constants']:
                reflect = command['constants']
            add_icosahedron(tmp, args[0], args[1], args[2], args[3])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []


        elif c == 'torus':
            if command['constants']:
                reflect = command['constants']
            add_torus(tmp,
                      args[0], args[1], args[2], args[3], args[4], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
            reflect = '.white'
        elif c == 'line':
            add_edge(tmp,
                     args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        elif c == 'move':
            tmp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'scale':
            tmp = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'rotate':
            theta = args[1] * (math.pi/180)
            if args[0] == 'x':
                tmp = make_rotX(theta)
            elif args[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
            tmp = []
        elif c == 'push':
            stack.append([x[:] for x in stack[-1]] )
        elif c == 'pop':
            stack.pop()
        elif c == 'display':
            if framect == 1:
                display(screen)

        elif c == 'light':
            if command['light']:
                tmp = symbols[command['light']][1]['color']
                light.append(tmp)
                tmp = symbols[command['light']][1]['location']
                light.append(tmp)
                tmp = []
            # light.append([l[0], l[1], l[2]])
            # light.append([l[3], l[4], l[5]])

        elif c == 'frames':
            pass

        elif c == 'basename':
            pass

        elif c == 'vary':
            pass


        elif c == 'save':
            if framect == 1:
                save_extension(screen, args[0])

def parseAnimation(commands, symbols):
    framect = 1
    basenm = 'img'
    framect_ = False
    basenm_ = False
    vary_ = False
    KNOBS = []

    for command in commands:
        c = command['op']
        args = command['args']
        if c == 'frames':
            framect = int(args[0])
            framect_ = True
        elif c == 'basename':
            basenm = args[0]
            basenm_ = True
        elif c == 'vary':
            vary_ = True

    if (framect == 1):
        return False

    if (framect_ and (not basenm_ )):
        print("WARNING: basename not defined, set to 'img'")
    if (vary_ and (not framect_)):
        print("ERROR: vary with no frame count")
    
    for i in range (0, int(framect)):
        KNOBS.append( [] )

    for command in commands:
        c = command['op']
        args = command['args']

        if c == 'vary':
            # print("################")
            # print(command)
            # print("################")

            #check length args
            change = float(args[3])-float(args[2])
            frames = int(args[1])-int(args[0])
            val = int(args[2])
            incr = 0

            x1 = float(args[0])
            y1 = float(args[2])
            x2 = float(args[1])
            y2 = float(args[3])
            a = 0
            b = 0
            d = 0

            if len(args) == 4:
                incr = change / (int(args[1])-int(args[0]))
            else:
                if float(args[4]) > 0:
                    a = (y2-y1)/((x2-x1)*(x2-x1))
                else:
                    a = (y1-y2)/((x2-x1)*(x2-x1))
                # a = float(args[4])/10000
                # b = ((y1-y2)-a*(x1*x1-x2*x2))/(x1-x2)
                # d = (x1*y2-x2*y1-a*(x1*x2*x2-x1*x1*x2))/(x1-x2)

            for i in range(0, int(args[0])):
                KNOBS[i].append( [command['knob'], float(args[2])] )

            for i in range(int(args[0]), int(args[1])+1):
                if len(args) == 4:
                    KNOBS[i].append( [command['knob'], val] )
                    val += incr
                else:
                    # val = a*i*i+b*i+d
                    if float(args[4]) > 0:
                        val = a*(i-x1)*(i-x1)+y1
                    else:
                        val = a*(i-x2)*(i-x2)+y2
                    KNOBS[i].append( [command['knob'], val] )
                    #print(val)
            
            for i in range(int(args[1])+1, len(KNOBS)):
                KNOBS[i].append( [command['knob'], float(args[3])] )
            
            #print(KNOBS)
    



    for frame in range(0, framect):
        view = [0,
                0,
                1];
        ambient = [50,
                50,
                50]
        light = [[0.5,
                0.75,
                1],
                [255,
                255,
                255]]

        color = [0, 0, 0]
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        consts = ''
        coords = []
        coords1 = []
        symbols['.white'] = ['constants',
                            {'red': [0.2, 0.5, 0.5],
                            'green': [0.2, 0.5, 0.5],
                            'blue': [0.2, 0.5, 0.5]}]
        reflect = '.white'
        for command in commands:
            #print(command)
            c = command['op']
            args = command['args']

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                        args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'


            elif c == 'icosahedron':
                if command['constants']:
                    reflect = command['constants']
                add_icosahedron(tmp, args[0], args[1], args[2], args[3])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []


            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                        args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                        args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                if command['knob']:
                    tknob = -1
                    for i in range (0, len(KNOBS[frame])):
                        if KNOBS[frame][i][0] == command['knob']:
                            tknob = KNOBS[frame][i][1]
                    tmp = make_translate(tknob*args[0], tknob*args[1], tknob*args[2])
                else:
                    tmp = make_translate(args[0], args[1], args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                if command['knob']:
                    tknob = -1
                    for i in range (0, len(KNOBS[frame])):
                        if KNOBS[frame][i][0] == command['knob']:
                            tknob = KNOBS[frame][i][1]
                    tmp = make_scale(tknob*args[0], tknob*args[1], tknob*args[2])
                else:
                    tmp = make_scale(args[0], args[1], args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':

                if command['knob']:
                    tknob = -1
                    for i in range (0, len(KNOBS[frame])):
                        if KNOBS[frame][i][0] == command['knob']:
                            tknob = KNOBS[frame][i][1]
                    theta = args[1] * (math.pi/180) * tknob
                else:
                    theta = args[1] * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                if framect == 1:
                    display(screen)

            elif c == 'light':
                if command['light']:
                    tmp = symbols[command['light']][1]['color']
                    light.append(tmp)
                    tmp = symbols[command['light']][1]['location']
                    light.append(tmp)
                    tmp = []
                # light.append([l[0], l[1], l[2]])
                # light.append([l[3], l[4], l[5]])

            elif c == 'frames':
                pass

            elif c == 'basename':
                pass

            elif c == 'vary':
                pass


            elif c == 'save':
                if framect == 1:
                    save_extension(screen, args[0])
        strin = "imgs/" + basenm + ("%04d" % (frame)) + ".png"
        save_extension(screen, strin)
    return True


