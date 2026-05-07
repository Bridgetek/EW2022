"""Random Hello text demo screen for the IDM2040 board."""

import random
import time

from brteve.brt_eve_bt817_8 import BrtEve


class hello_demo:
    """Draw many Hello labels in random colors and positions."""

    def __init__(self, eve: BrtEve):
        """Store the active EVE instance."""
        self.eve = eve
        self.tag_back = 1
        self.tick = 0
        self.text_count = 42
        self.items = []
        self.randomize_items()

    def random_color(self):
        """Return a readable random RGB color."""
        return (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255),
        )

    def randomize_items(self):
        """Create random text positions, colors, and font sizes."""
        self.items = []
        for _ in range(self.text_count):
            self.items.append(
                {
                    "x": random.randint(10, 720),
                    "y": random.randint(55, 435),
                    "font": random.randint(22, 31),
                    "color": self.random_color(),
                }
            )

    def draw_hello_texts(self):
        """Draw every Hello label for the current frame."""
        eve = self.eve

        for item in self.items:
            color = item["color"]
            eve.ColorRGB(color[0], color[1], color[2])
            eve.cmd_text(item["x"], item["y"], item["font"], 0, "Hello")

    def draw_background(self):
        """Draw a low-glare background for the text field."""
        eve = self.eve
        bar_width = 80 + ((self.tick * 5) % 640)

        eve.ColorRGB(0x11, 0x16, 0x20)
        eve.Begin(eve.RECTS)
        eve.LineWidth(4)
        eve.Vertex2f(0, 48)
        eve.Vertex2f(800, 480)

        eve.ColorRGB(0x00, 0x66, 0x58)
        eve.Begin(eve.RECTS)
        eve.LineWidth(2)
        eve.Vertex2f(0, 48)
        eve.Vertex2f(bar_width, 54)

        eve.ColorRGB(0xFF, 0xFF, 0xFF)
        eve.cmd_text(20, 10, 30, 0, "Hello Text Demo")

    def draw_frame(self):
        """Draw one frame and return the current touch tag."""
        eve = self.eve

        eve.cmd_dlstart()
        eve.VertexFormat(2)
        eve.ClearColorRGB(0x05, 0x07, 0x0A)
        eve.Clear(1, 1, 1)

        self.draw_background()

        eve.Tag(self.tag_back)
        eve.cmd_button(700, 5, 85, 35, 30, 0, "Back")
        eve.Tag(0)

        self.draw_hello_texts()

        tag = eve.rd32(eve.REG_TOUCH_TAG) & 0xFF
        eve.Display()
        eve.cmd_swap()
        eve.flush()
        return tag

    def clear_screen(self):
        """Clear the display before returning to the main menu."""
        eve = self.eve
        eve.cmd_dlstart()
        eve.VertexFormat(2)
        eve.ClearColorRGB(0, 0, 0)
        eve.Clear(1, 1, 1)
        eve.Display()
        eve.cmd_swap()
        eve.flush()

    def loop(self):
        """Run the demo until the user presses Back."""
        while True:
            if self.tick % 20 == 0:
                self.randomize_items()
            tag = self.draw_frame()
            if tag == self.tag_back:
                break
            self.tick += 1
            time.sleep(0.02)

        self.clear_screen()
