import pygame
import secrets

def randint(l, r):
  return l + secrets.randbelow(r - l + 1)

def write(screen, button_rect, text, font_size, text_color, button_color, border, align="center", multiline=False, char_spacing=0):
  font = pygame.font.Font(None, font_size)
  pygame.draw.rect(screen, button_color, button_rect)
  
  if multiline:
    lines = []
    max_width = button_rect.width - 2 * border
    raw_lines = text.split("\n")
    
    for raw_line in raw_lines:
      current_line = ""
      current_words = raw_line.split(" ") if raw_line else [""]
      
      for word in current_words:
        word_with_space = word + " " if word else ""
        word_width = sum(font.render(char, True, text_color).get_width() + char_spacing for char in word_with_space) - char_spacing if word else 0
        if font.render(current_line, True, text_color).get_width() + word_width <= max_width:
          current_line += word_with_space
        else:
          if current_line:
            lines.append(current_line.strip())
            current_line = ""
          
          temp_line = current_line
          for i, char in enumerate(word):
            char_surface = font.render(char, True, text_color)
            char_width = char_surface.get_width() + char_spacing
            if font.render(temp_line, True, text_color).get_width() + char_width <= max_width:
              temp_line += char
            else:
              if temp_line:
                lines.append(temp_line)
              temp_line = char
          current_line = temp_line
          if word_with_space and word_with_space[-1] == " " and font.render(current_line + " ", True, text_color).get_width() + char_spacing <= max_width:
            current_line += " "
      
      lines.append(current_line.strip() if current_line else "")
      
      for i, line in enumerate(lines):
        if char_spacing == 0:
          text_surface = font.render(line, True, text_color)
          text_rect = text_surface.get_rect()
          if align == "left":
            text_rect.topleft = (button_rect.left + border, button_rect.top + border + i * font_size)
          elif align == "right":
            text_rect.topright = (button_rect.right - border, button_rect.top + border + i * font_size)
          else:
            text_rect.center = (button_rect.centerx, button_rect.top + border + i * font_size)
          screen.blit(text_surface, text_rect)
        else:
          if align == "left":
            x_pos = button_rect.left + border
          elif align == "right":
            x_pos = button_rect.right - border - sum(font.render(c, True, text_color).get_width() + char_spacing for c in line) + char_spacing
          else:
            x_pos = button_rect.centerx - sum(font.render(c, True, text_color).get_width() + char_spacing for c in line) / 2 + char_spacing / 2
          y_pos = button_rect.top + border + i * font_size
          for char in line:
            char_surface = font.render(char, True, text_color)
            screen.blit(char_surface, (x_pos, y_pos))
            x_pos += char_surface.get_width() + char_spacing
  else:
    if char_spacing == 0:
      text_surface = font.render(text, True, text_color)
      text_rect = text_surface.get_rect()
      if align == "left":
        text_rect.topleft = (button_rect.left + border, button_rect.top + border)
      elif align == "right":
        text_rect.topright = (button_rect.right - border, button_rect.top + border)
      else:
        text_rect.center = button_rect.center
      screen.blit(text_surface, text_rect)
    else:
      if align == "left":
        x_pos = button_rect.left + border
      elif align == "right":
        x_pos = button_rect.right - border - sum(font.render(c, True, text_color).get_width() + char_spacing for c in text) + char_spacing
      else:
        x_pos = button_rect.centerx - sum(font.render(c, True, text_color).get_width() + char_spacing for c in text) / 2 + char_spacing / 2
      y_pos = button_rect.top + border if align == "left" or align == "right" else button_rect.centery - font.get_height() / 2
      for char in text:
        char_surface = font.render(char, True, text_color)
        screen.blit(char_surface, (x_pos, y_pos))
        x_pos += char_surface.get_width() + char_spacing