import shutil
from typing import List

class Color:
    def __init__(self, esc_type='\033'):
        self.esc_type = esc_type
        
        # Basic text colors
        self.black = f'{self.esc_type}[30m'
        self.red = f'{self.esc_type}[31m'
        self.green = f'{self.esc_type}[32m'
        self.yellow = f'{self.esc_type}[33m'
        self.blue = f'{self.esc_type}[34m'
        self.white = f'{self.esc_type}[97m'
        
        # Text styles
        self.bold = f'{self.esc_type}[1m'
        self.italic = f'{self.esc_type}[3m'
        self.underline = f'{self.esc_type}[4m'
        self.strike = f'{self.esc_type}[9m'
        
        # Reset code
        self.reset = f'{self.esc_type}[0m'

    def rgb_color(self, r: int, g: int, b: int) -> str:
        """Генерирует RGB цвет для текста"""
        return f'{self.esc_type}[38;2;{r};{g};{b}m'
    
    def rgb_bgcolor(self, r: int, g: int, b: int) -> str:
        """Генерирует RGB цвет для фона"""
        return f'{self.esc_type}[48;2;{r};{g};{b}m'
    
    def color_message(self, message: str, color: str = None, 
                     gradient: bool = False, 
                     gradient_colors: list = None,
                     gradient_bgcolors: list = None,
                     style: str = None) -> str:
        """
        Форматирует сообщение с цветами, стилями и градиентами.
        """
        # Валидация стиля
        if style is not None and not isinstance(style, str):
            raise TypeError("Параметр 'style' должен быть строкой")

        if gradient:
            return self._apply_gradient(
                message, 
                style,
                gradient_colors if gradient_colors else [],
                gradient_bgcolors if gradient_bgcolors else []
            )
        else:
            return self._apply_simple_format(message, color, style)

    def _apply_gradient(self, message: str, style: str,
                       fg_colors: list, bg_colors: list) -> str:
        """Применяет градиент к сообщению"""
        # Проверка наличия цветов для градиента
        if not fg_colors and not bg_colors:
            raise ValueError("Нужно указать gradient_colors или gradient_bgcolors")

        # Проверка типов цветов
        for colors, name in [(fg_colors, 'gradient_colors'), 
                           (bg_colors, 'gradient_bgcolors')]:
            for c in colors:
                if not self._is_rgb_color(c, foreground=(name == 'gradient_colors')):
                    raise ValueError(f"Цвет {c} не является RGB-цветом. Используйте методы rgb_color() или rgb_bgcolor()")

        # Парсинг цветов
        fg_sequences = [self._parse_rgb(c) for c in fg_colors]
        bg_sequences = [self._parse_rgb(c) for c in bg_colors]

        # Генерация градиента
        styled_message = []
        if style:
            styled_message.append(style)
            
        for i, char in enumerate(message):
            parts = []
            progress = i / (len(message) - 1) if len(message) > 1 else 0.0
            
            # Градиент для текста
            if fg_sequences:
                r, g, b = self._interpolate_color(fg_sequences, progress)
                parts.append(self.rgb_color(r, g, b))
                
            # Градиент для фона
            if bg_sequences:
                r, g, b = self._interpolate_color(bg_sequences, progress)
                parts.append(self.rgb_bgcolor(r, g, b))
                
            styled_message.append(''.join(parts) + char)

        styled_message.append(self.reset)
        return ''.join(styled_message)

    def _apply_simple_format(self, message: str, color: str, style: str) -> str:
        """Простое форматирование без градиента"""
        parts = []
        if style:
            parts.append(style)
        if color:
            if not self._is_rgb_color(color) and not self._is_basic_color(color):
                raise ValueError("Используйте методы класса для задания цвета")
            parts.append(color)
        return f'{"".join(parts)}{message}{self.reset}' if parts else message

    def _is_rgb_color(self, esc_code: str, foreground: bool = True) -> bool:
        """Проверяет, является ли ESC-код RGB цветом"""
        prefix = '38;2;' if foreground else '48;2;'
        return esc_code.startswith(f'{self.esc_type}[{prefix}')

    def _is_basic_color(self, esc_code: str) -> bool:
        """Проверяет базовые цвета (30-37, 90-97, 40-47, 100-107)"""
        return esc_code in {
            self.black, self.red, self.green, self.yellow,
            self.blue, self.white, self.reset
        }

    def _parse_rgb(self, esc_code: str) -> tuple:
        """Извлекает RGB значения из ESC-кода"""
        parts = esc_code[2:-1].split(';')  # Убираем \033[ и m
        if len(parts) < 5 or (parts[0] != '38' and parts[0] != '48') or parts[1] != '2':
            raise ValueError(f"Некорректный RGB-формат: {esc_code}")
        return tuple(map(int, parts[2:5]))

    def _interpolate_color(self, color_sequence: list, progress: float) -> tuple:
        """Интерполяция между цветами"""
        n = len(color_sequence)
        if n == 0:
            raise ValueError("Пустая последовательность цветов")
        if n == 1:
            return color_sequence[0]
        
        position = progress * (n - 1)
        idx = int(position)
        t = position - idx
        
        if idx >= n - 1:
            return color_sequence[-1]
            
        return tuple(round(color_sequence[idx][i] + (color_sequence[idx+1][i] - color_sequence[idx][i]) * t)
                   for i in range(3))
    def format_message_block(
        self,
        message: str,
        width: int = None,
        height: int = 5,
        bg_colors: List[str] = None,
        text_color: str = None
    ) -> str:
        """Форматирует текст в блок с градиентным фоном"""
        # Получаем размеры терминала
        console_width = shutil.get_terminal_size().columns
        console_height = shutil.get_terminal_size().lines
        
        # Рассчитываем ширину блока
        block_width = min(width or console_width, console_width)
        left_padding = (console_width - block_width) // 2
        
        # Парсим цвета фона
        bg_rgb = [self._parse_bg_color(c) for c in bg_colors]
        
        # Генерируем градиент
        gradient = self._generate_gradient(bg_rgb, height)
        
        # Разбиваем сообщение на строки
        text_lines = self._wrap_text(message, block_width)
        
        # Центрируем текст вертикально
        text_block = self._vertical_center(text_lines, height)
        
        # Собираем финальный блок
        result = []
        for i in range(height):
            # Градиентный фон
            bg = gradient[i]
            line = f"{' ' * left_padding}{bg}{' ' * block_width}{self.reset}"
            
            # Добавляем текст если есть
            if i < len(text_block) and text_block[i]:
                text = text_block[i]
                text_pos = left_padding + (block_width - len(text)) // 2
                # УБИРАЕМ reset из цветного текста
                colored_text = f"{text_color or ''}{text}"
                line = f"{line[:text_pos]}{colored_text}{line[text_pos + len(text):]}"
                
            result.append(line)
            
        return '\n'.join(result)
    
    def _parse_bg_color(self, esc_code: str) -> tuple:
        """Извлекает RGB из ESC-кода фона"""
        parts = esc_code[2:-1].split(';')
        if parts[:2] != ['48', '2']:
            raise ValueError("Используйте только RGB цвета фона (rgb_bgcolor)")
        return tuple(map(int, parts[2:5]))
    
    def _generate_gradient(self, colors: List[tuple], steps: int) -> List[str]:
        """Генерирует градиент между цветами"""
        if len(colors) == 1:
            return [self.rgb_bgcolor(*colors[0])] * steps
            
        gradient = []
        segment = (steps - 1) / (len(colors) - 1)
        
        for i in range(steps):
            pos = i / segment
            idx = int(pos)
            t = pos - idx
            
            if idx >= len(colors)-1:
                r, g, b = colors[-1]
            else:
                r = int(colors[idx][0] + (colors[idx+1][0] - colors[idx][0]) * t)
                g = int(colors[idx][1] + (colors[idx+1][1] - colors[idx][1]) * t)
                b = int(colors[idx][2] + (colors[idx+1][2] - colors[idx][2]) * t)
                
            gradient.append(self.rgb_bgcolor(r, g, b))
            
        return gradient
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """Переносит текст по словам"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
    
    def _vertical_center(self, lines: List[str], height: int) -> List[str]:
        """Центрирует текст по вертикали"""
        if len(lines) > height:
            return lines[:height]
            
        padding_top = (height - len(lines)) // 2
        padding_bottom = height - len(lines) - padding_top
        
        return [''] * padding_top + lines + [''] * padding_bottom
