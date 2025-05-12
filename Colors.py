class Color:
    def __init__(self, esc_type='\033'):
        self.esc_type = esc_type
        self.black = f'{self.esc_type}[30m'
        self.red = f'{self.esc_type}[31m'
        self.green = f'{self.esc_type}[32m'
        self.yellow = f'{self.esc_type}[33m'
        self.blue = f'{self.esc_type}[34m'
        self.white = f'{self.esc_type}[97m'
        self.reset = f'{self.esc_type}[0m'


    def rgb_color(self, r: int, g: int, b: int) -> str:
        return f'{self.esc_type}[38;2;{r};{g};{b}m'
    

    def rgb_bgcolor(self, r: int, g: int, b: int) -> str:
        return f'{self.esc_type}[48;2;{r};{g};{b}m'
    

    def color_message(self, message: str, color: str) -> str:
        return f'{color}{message}{self.reset}'