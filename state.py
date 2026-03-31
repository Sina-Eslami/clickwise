class Action():
    def __init__(self, mode, delay, image, image_pos, click_pos):
        """
        mode: str either 'Time' or 'Screenshot'
        delay: a positive integer
        image: PIL Image Obj
        image_pos: (x, y) of the screenshot
        click_pos: (x, y) of where to be clicked
        """
        self.mode = mode
        self.delay = delay
        self.image = image
        self.image_pos = image_pos
        self.click_pos = click_pos
