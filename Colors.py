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
    
    def color_message(self, message: str, color: str = None, gradient: bool = False, 
                      gradient_colors: list = None, gradient_bgcolors: list = None) -> str:
        if gradient:
            if not gradient_colors and not gradient_bgcolors:
                raise ValueError("Для градиента необходимо указать gradient_colors или gradient_bgcolors")
            
            if gradient_colors is not None:
                if not isinstance(gradient_colors, list) or len(gradient_colors) < 1:
                    raise ValueError("gradient_colors должен быть списком с хотя бы одним цветом")
                for c in gradient_colors:
                    if not isinstance(c, str):
                        raise TypeError("Все цвета в gradient_colors должны быть строками")
            
            if gradient_bgcolors is not None:
                if not isinstance(gradient_bgcolors, list) or len(gradient_bgcolors) < 1:
                    raise ValueError("gradient_bgcolors должен быть списком с хотя бы одним цветом")
                for c in gradient_bgcolors:
                    if not isinstance(c, str):
                        raise TypeError("Все цвета в gradient_bgcolors должны быть строками")

            fg_colors = gradient_colors if gradient_colors else []
            bg_colors = gradient_bgcolors if gradient_bgcolors else []

            message_len = len(message)
            if message_len == 0:
                return ''
            
            result = []
            for i, char in enumerate(message):
                p = i / (message_len - 1) if message_len > 1 else 0.0
                
                fg_esc = None
                if fg_colors:
                    try:
                        fg_rgb_list = [self._parse_esc_code(c) for c in fg_colors]
                        interpolated_rgb = self._interpolate_rgb(fg_rgb_list, p)
                        fg_esc = self.rgb_color(*interpolated_rgb)
                    except ValueError as e:
                        raise e
                
                bg_esc = None
                if bg_colors:
                    try:
                        bg_rgb_list = [self._parse_esc_code(c) for c in bg_colors]
                        interpolated_rgb = self._interpolate_rgb(bg_rgb_list, p)
                        bg_esc = self.rgb_bgcolor(*interpolated_rgb)
                    except ValueError as e:
                        raise e
                
                parts = []
                if fg_esc:
                    parts.append(fg_esc)
                if bg_esc:
                    parts.append(bg_esc)
                
                if parts:
                    result.append(''.join(parts) + char)
                else:
                    result.append(char)
            
            result.append(self.reset)
            return ''.join(result)
        else:
            if color is None:
                return message
            return f'{color}{message}{self.reset}'
    
    def _parse_esc_code(self, esc_code: str) -> tuple:
        import re
        numbers = list(map(int, re.findall(r'\d+', esc_code)))
        
        if esc_code.startswith(f'{self.esc_type}[38;2;'):
            if len(numbers) >= 5 and numbers[0] == 38 and numbers[1] == 2:
                return (numbers[2], numbers[3], numbers[4])
        elif esc_code.startswith(f'{self.esc_type}[48;2;'):
            if len(numbers) >= 5 and numbers[0] == 48 and numbers[1] == 2:
                return (numbers[2], numbers[3], numbers[4])
        else:
            raise ValueError(f"Цвет {esc_code} не является RGB цветом (используйте rgb_color или rgb_bgcolor)")
        
        raise ValueError(f"Неверный формат ESC-кода: {esc_code}")
    
    def _interpolate_rgb(self, rgb_list: list, p: float) -> tuple:
        n = len(rgb_list)
        if n == 0:
            raise ValueError("Список цветов для интерполяции пуст")
        if n == 1:
            return rgb_list[0]
        
        segment_length = 1.0 / (n - 1)
        segment_index = int(p / segment_length)
        
        if segment_index >= n - 1:
            segment_index = n - 2
            t = 1.0
        else:
            t = (p - segment_index * segment_length) / segment_length
        
        color1 = rgb_list[segment_index]
        color2 = rgb_list[segment_index + 1]
        
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        
        return (r, g, b)
