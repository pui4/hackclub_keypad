import board # type: ignore
import busio # type: ignore
import digitalio # type: ignore
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.digitalio import MatrixScanner
from kmk.extensions.rgb import RGB
from kmk.modules.encoder import EncoderHandler
from mcp23017 import MCP23017  # type: ignore
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)
driver = SSD1306(i2c=i2c)

cols = []
for i in range(4):
    pin = mcp.get_pin(i)
    pin.switch_to_input(pull=1)
    cols.append(pin)

rows = []
for i in range (8, 13):
    pin = mcp.get_pin(i)
    pin.switch_to_input(pull=1)
    rows.append(pin)

class MegaPad(KMKKeyboard):
    def __init__(self) -> None:
        super().__init__()

        self.matrix = MatrixScanner(
            cols=cols,
            rows=rows,
            diode_orientation=self.diode_orientation, # type: ignore
            pull=digitalio.Pull.DOWN
        )
keyboard = MegaPad()

keyboard.keymap = [
    [
        KC.H, KC.E, KC.L ,KC.L, 
        KC.O ,KC.W, KC.O, KC.R, 
        KC.L, KC.D, KC.F, KC.R, 
        KC.O, KC.M, KC.M, KC.E, 
        KC.D, KC.P
    ]
]

encoder_handler = EncoderHandler()
encoder_handler.pins = ( # type: ignore
    (board.GP27, board.GP28, None,),
    (board.GP29, board.GP0, None,),
)

keyboard.modules.append(encoder_handler)

display = Display(display=driver)
display.entries = [
    TextEntry('Hello, World!')
]

keyboard.extensions.append(display)

rgb = RGB(pixel_pin=board.GP3, num_pixels=16)
keyboard.extensions.append(rgb)

if __name__ == "__main__":
    keyboard.go()