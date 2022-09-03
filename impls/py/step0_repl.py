import readline

def READ(s):
  return s

def EVAL(s):
  return s

def PRINT(s):
  print(s)

def rep(s):
  PRINT(EVAL(READ(s)))

def main():
  readline.read_init_file()
  while(1):
    try:
      inp = input("user> ")
    except EOFError:
      print("\nExiting...")
      return 0
    readline.add_history(inp)
    rep(inp)

if __name__=="__main__":
  main()
