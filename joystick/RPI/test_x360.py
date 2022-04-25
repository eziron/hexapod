from xbox360controller import Xbox360Controller
import signal

def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, 
        round(dead_val_axis(axis.x,30)*256),
        round(dead_val_axis(axis.y,30)*256)))

def a_map(x:float, in_min:float, in_max:float, out_min:float, out_max:float):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def dead_val_axis(axis_val,dead_val):
    dead_min = -(dead_val/100)
    dead_max =  (dead_val/100)

    if(axis_val >= dead_min and axis_val <= dead_max):
        return 0.0
    elif(axis_val > dead_max):
        return a_map(axis_val,dead_max,1,0,1)
    elif(axis_val < dead_min):
        return a_map(axis_val,-1,dead_min,-1,0)
    else:
        return 0.0

try:
    with Xbox360Controller(0, axis_threshold=0) as controller:
        controller.button_a.when_pressed = on_button_pressed
        controller.button_a.when_released = on_button_released

        controller.axis_l.when_moved = on_axis_moved
        controller.axis_r.when_moved = on_axis_moved
        signal.pause()
        """while True:
            print(
                round(dead_val_axis(controller.axis_l.x,30)*256),
                round(dead_val_axis(controller.axis_l.y,30)*256),

                round(dead_val_axis(controller.axis_r.x,30)*256),
                round(dead_val_axis(controller.axis_r.y,30)*256),

                controller.hat._value_x,
                controller.hat.y,

                round(controller.trigger_l.value*256),
                round(controller.trigger_r.value*256),

                controller.button_a._value
            )"""
except KeyboardInterrupt:
    pass