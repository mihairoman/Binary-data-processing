import sys
import re

def hex_to_dec(hex_value):
  return int(hex_value, 16)

def hex_to_rgb(hex_1, hex_2):
    return hex_to_dec(hex_1) * 16 + hex_to_dec(hex_2)

if __name__ == '__main__':
  for line in sys.stdin:
    # possible formats: (#fff, #fff8, #ffffff, #ffffffC0)
    hex_match = re.search(r'#[0-9a-fA-F]{3,8}', line, re.IGNORECASE)
    res = line

    if hex_match:
      match = hex_match.group(0)
      hex_value = match.lower()[1:] # remove the # from the hex value
      len_hex_value = len(hex_value)

      if len_hex_value <= 4:
        hex_r, hex_g, hex_b = hex_value[0], hex_value[1], hex_value[2]
        dec_r = hex_to_rgb(hex_r, hex_r)
        dec_g = hex_to_rgb(hex_g, hex_g)
        dec_b = hex_to_rgb(hex_b, hex_b)
        res = 'rgb({} {} {})'.format(dec_r, dec_g, dec_b)
        
        if (len_hex_value == 4):
          alpha = hex_value[3:4]
          dec_alpha = round(hex_to_rgb(alpha[0], alpha[0]) / 255, 5)
          res = 'rgba({} {} {} / {})'.format(dec_r, dec_g, dec_b, dec_alpha)

      else:
        hex_r, hex_g, hex_b = hex_value[0:2], hex_value[2:4], hex_value[4:6]
        dec_r = hex_to_rgb(hex_r[0], hex_r[1])
        dec_g = hex_to_rgb(hex_g[0], hex_g[1])
        dec_b = hex_to_rgb(hex_b[0], hex_b[1])
        res = 'rgb({} {} {})'.format(dec_r, dec_g, dec_b)
        
        if (len_hex_value == 8):
          alpha = hex_value[6:8]
          dec_alpha = round(hex_to_rgb(alpha[0], alpha[1]) / 255, 5)
          res = 'rgba({} {} {} / {})'.format(dec_r, dec_g, dec_b, dec_alpha)
      
      line = line.replace(match, res)

    sys.stdout.write(line)

    
      