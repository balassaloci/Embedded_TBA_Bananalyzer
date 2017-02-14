def rgb2hsl(r, g, b):
    r = r/255
    g = g/255
    b = b/255

    minimum = min(r, g, b)
    maximum = max(r, g, b)

    l = (minimum + maximum)/2                       #calculate luminance

    if minimum != maximum:
        if l <= 0.5:                                #calculate saturation
            s = (maximum - minimum)/(maximum + minimum)
        else:
            s = (maximum - minimum)/(2 - maximum - minimum) 

        if maximum == r:                            #calculate hue
            h = (g-b)/(maximum - minimum)
        elif maximum == g:
            h = 2 + (b-r)/(maximum - minimum)
        else:
            h = 4 + (r-g)/(maximum - minimum)
    else: 
        s = 0
        h = 0

    h = int(round(h*60, 0))                              #convert to degrees
    s = int(round(s*100, 0))                           #convert to %
    l = int(round(l*100, 0))                             #convert to %

    return h, s, l
