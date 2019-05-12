import cv2 
import sys
import getopt as opt
import pathlib as Path
from Render.render import render

def main(argv):
    inputJson = ''
    try:
        opts, args = opt.getopt(argv,"hi:",["ifile="])
    except opt.GetoptError:
        print('TODO: finish error notification')
        sys.exit(2)
    for anOpt, arg in opts:
      if anOpt == '-h':
         print('TODO: finish error notification')
         sys.exit()
      elif anOpt in ("-i", "--ifile"):
         inputJson = arg
    print(inputJson)
    rd = render(inputJson)
    rd.renderAll()

if __name__ == '__main__':
    main(sys.argv[1:])