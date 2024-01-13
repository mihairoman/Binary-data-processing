import sys
import tty
import time

def beep():
    sys.stdout.buffer.write(b'\x07')

def is_number(char):
  if 47 < ord(char) < 58:
    return True
  return False

if __name__ == '__main__':
  # save old terminal settings from stdin
  old_settings = tty.tcgetattr(0)

  try:
    # set to cbreak mode (doesn't require enter press from user but allows ctrl+c & ctrl+z) 
    tty.setcbreak(0) 

    while True:
      char = sys.stdin.read(1)
      if is_number(char):
        for _ in range(int(char)):
          beep()
          time.sleep(0.25)
        sys.stdout.buffer.flush()
  finally:
    tty.tcsetattr(0, tty.TCSADRAIN, old_settings)