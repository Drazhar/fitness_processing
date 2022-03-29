from src.bcolors import bcolors

def bar_plot(width, data):
  sum = 0
  for prop in data:
    sum += prop[0]

  for prop in data:
    print(prop[1],"█" * round(prop[0] / sum * width), end=bcolors.ENDC, sep="")
  print()