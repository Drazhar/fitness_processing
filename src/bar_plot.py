from src.bcolors import bcolors


def bar_plot(width, data):
  summed = sum(prop[0] for prop in data)

  for prop in data:
    print(prop[1], "█" * round(prop[0] / summed * width), end=bcolors.ENDC, sep="")
  print()