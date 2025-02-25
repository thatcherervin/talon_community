# from https://github.com/talonvoice/examples
# jsc added shift-click, command-click, and voice code compatibility

# import eye
import time
import math
from talon import ctrl, tap, ui
from talon.voice import Context, Key

ctx = Context("mouse")

x, y = ctrl.mouse_pos()
mouse_history = [(x, y, time.time())]
force_move = None


def on_move(typ, e):
    mouse_history.append((e.x, e.y, time.time()))
    if force_move:
        e.x, e.y = force_move
        return True


tap.register(tap.MMOVE, on_move)


def click_pos(m):
    word = m._words[0]
    start = (word.start + min((word.end - word.start) / 2, 0.100)) / 1000.0
    diff, pos = min([(abs(start - pos[2]), pos) for pos in mouse_history])
    return pos[:2]


def delayed_click(m, button=0, times=1):
    # old = eye.config.control_mouse
    # eye.config.control_mouse = False
    # x, y = click_pos(m)
    # ctrl.mouse(x, y)
    ctrl.mouse_click(x, y, button=button, times=times, wait=16000)
    # time.sleep(0.032)
    # eye.config.control_mouse = old


def press_key_and_click(m, key, button=0, times=1):
    ctrl.key_press(key, down=True)
    ctrl.mouse_click(x, y, button=button, times=times, wait=16000)
    ctrl.key_press(key, up=True)


def shift_click(m, button=0, times=1):
    press_key_and_click(m, "shift", button, times)


def command_click(m, button=0, times=1):
    press_key_and_click(m, "cmd", button, times)


def delayed_right_click(m):
    delayed_click(m, button=1)


def delayed_dubclick(m):
    delayed_click(m, button=0, times=2)


def delayed_tripclick(m):
    delayed_click(m, button=0, times=3)


def mouse_scroll(amount):
    def scroll(m):
        ctrl.mouse_scroll(y=amount)

    return scroll

def mouse_smooth_scroll(amount):
    def scroll(m):
        total_time = 0.1
        interval = 0.007
        depth = int(total_time // interval)
        split = amount / depth
        for x in range(depth):
            # split_ret = int((split) * (1 - 0.8 * (((x - (depth / 2)) / float((depth / 2))) ** 2)))
            ctrl.mouse_scroll(y=split)
            time.sleep(interval)

    return scroll


def mouse_drag(m):
    x, y = click_pos(m)
    ctrl.mouse_click(x, y, down=True)


def mouse_release(m):
    x, y = click_pos(m)
    ctrl.mouse_click(x, y, up=True)


def mouse_center(m):
    win = ui.active_window()
    rect = win.rect
    center = (rect.x + rect.width / 2, rect.y + rect.height / 2)
    print(rect, center)
    ctrl.mouse_move(*center)


def press_key_and_click(m, key, button=0, times=1):
    ctrl.key_press(key, down=True)
    ctrl.mouse_click(x, y, button=button, times=times, wait=16000)
    ctrl.key_press(key, up=True)


def shift_click(m, button=0, times=1):
    press_key_and_click(m, "shift", button, times)


def command_click(m, button=0, times=1):
    press_key_and_click(m, "cmd", button, times)


def control_shift_click(m, button=0, times=1):
    ctrl.key_press("shift", ctrl=True, shift=True, down=True)
    ctrl.mouse_click(x, y, button=button, times=times, wait=16000)
    ctrl.key_press("shift", ctrl=True, shift=True, up=True)


keymap = {
    # jsc modified with some voice-code compatibility
    "righty": delayed_right_click,
    "(click | chiff)": delayed_click,
    "(dubclick | duke)": delayed_dubclick,
    "(tripclick | triplick)": delayed_tripclick,
    "drag": mouse_drag,
    "drag release": mouse_release,
    "(shift click | shicks)": shift_click,
    "(command click | chom lick)": command_click,
    "(control shift click | troll shift click)" : control_shift_click,
    "(control shift double click | troll shift double click)" : lambda m: control_shift_click(m, 0, 2),
    "do park": [delayed_dubclick, Key('cmd-v')],
	"do koosh": [delayed_dubclick, Key('cmd-c')],

    "(wheel down | downer)": mouse_smooth_scroll(400),
    "(wheel up | upper)": mouse_smooth_scroll(-400),
    "wheel down here": [mouse_center, mouse_scroll(200)],
    "wheel up here": [mouse_center, mouse_scroll(-200)],
    "mouse center": mouse_center,
}

ctx.keymap(keymap)
