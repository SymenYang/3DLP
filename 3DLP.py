import cv2 
import sys
import getopt as opt
import pathlib as Path

def main(argv):
    inputJson = ''
    outputImg = ''
    try:
        opts, args = opt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except opt.GetoptError:
        print('TODO: finish error notification')
        sys.exit(2)
    for anOpt, arg in opts:
      if anOpt == '-h':
         print('TODO: finish error notification')
         sys.exit()
      elif anOpt in ("-i", "--ifile"):
         inputJson = arg
      elif anOpt in ("-o", "--ofile"):
         outputImg = arg
    print(inputJson,outputImg)

if __name__ == '__main__':
    main(sys.argv[1:])