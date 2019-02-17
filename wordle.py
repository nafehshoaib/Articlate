from tkinter import *
from tkinter.font import *
import math
from random import triangular


# class for input words
class WordRecord:
  def __init__(self, text, size, vert):
        self.text = text
        self.size = size
        self.vert = vert 

# a position vector that knows how to move in a spiral
class spiralInc:
  
  def __init__(self,size):
    self.stepSize = size

  def initialize(self,x,y):
    self.x = triangular(x-x/4, x+x/4, x)
    self.y = triangular(y-y/4, y+y/4, y)
    self.initialX = self.x
    self.initialY = self.y

    
  def update(self,w):
    x = self.x-self.initialX
    y = self.y-self.initialY
    length = math.sqrt(x**2 + y**2)
    # very near the origin
    if length < 1:
      self.x += self.stepSize
      return
    # vector pointing out towards current position, gets smaller linearly with length
    outX = x/(length**2)
    outY = y/(length**2)
    # unit vector perpendicular to vector to current position
    dirX = -y/length
    dirY = x/length
    self.x += self.stepSize*(outX + dirX)
    self.y += self.stepSize*(outY + dirY)
    

# takes a word object and a place object as input
# adds the word to the wordle at the given place
def addToWordle(word, place, fonts, w):
        fontObj = fonts[word.size]
        if word.vert:
            ang = 90
        else:
            ang = 0
        # actually draw it
        m = w.create_text(place.x, place.y,
              text=word.text, angle=ang, font=fontObj)
        return m


def makeWordle(wordList):

  # the window
  master = Tk()
  #the canvas
  canvas_width = 500
  canvas_height = 300
  w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
  w.pack()
  w.update()

  # the fonts
  # for now, default font
  # choices are Courier, Helvetica, and Times
  # ought to modify font on fly, instead of making this array...
  # helv36 = Font(family='Helvetica', size=36, weight='bold')
  fonts = [
          Font(family='Times', size=18, weight='bold'),
          Font(family='Times', size=24, weight='bold'),
          Font(family='Times', size=30, weight='bold'),
          Font(family='Times', size=36, weight='bold')
          ]


  # place words!
  # starting near the center, try to place word; if it hits something else,
  # move in a spiral trying to find a free location


  
  # make a new spiralInc object
  place = spiralInc(1)
  
  for word in wordList:
    place.initialize(canvas_width/2, canvas_height/2)
    while True:
      m = addToWordle(word, place, fonts, w)
      bb = w.bbox(m)
      # the * syntax replaces the tuple with its contents
      # find_overlapping returns the objects overlapping the bounding box
      # an item always overlaps its own bounding box, so if there is
      # just one thing, then it's a non-overlapping placement
      if len(w.find_overlapping(*bb)) == 1:
        break
      # overlaps something....
      # maybe move instead of delete and re-add...
      w.delete(m)
      place.update(w)


##def wordleFromFreqs(inputObj):
##  freqList = inputObj.get
##  horizontal = False
##  vertical = True
##  minFreq = freqlist[-1][0]
##  maxFreq = freqlist[0][0]
##  wordlist = []
##  orientation = horizontal 
##  for i in range(len(freqlist)):
##    size = (freqlist[i][0] - minFreq)*4 // (maxFreq+1-minFreq)
##    assert (0 <= size) & (3 >= size)
##    wordlist.append(WordRecord(freqlist[i][1], size, orientation))
##    if alternate:
##      orientation = not orientation
##  makeWordle(wordlist)
##
def wordleFromObject(inputObject, numberOfWords):
  freqlist = inputObject.getTopWords(numberOfWords)
  alternate = True
  horizontal = False
  vertical = True
  minFreq = freqlist[-1][0]
  maxFreq = freqlist[0][0]
  wordlist = []
  orientation = horizontal 
  for i in range(len(freqlist)):
    size = (freqlist[i][0] - minFreq)*4 // (maxFreq+1-minFreq)
    assert (0 <= size) & (3 >= size)
    wordlist.append(WordRecord(freqlist[i][1], size, orientation))
    if alternate:
      orientation = not orientation
  makeWordle(wordlist)
    

# demo function, run only when worldle.py is run from command line
def showDemo():
  # For the demo we define a very simple version of the Counts class,
  # just used to test the wordle code.  The Counts class you will write
  # has to get real data, so it does a lot more than this one does. 
  # This simple version has has one property, a sorted list of words and
  # frequencies, and one method, called getTopWords, which returns the
  # list. 
  class Counts:

    # the object holds a list of words, each one with an integer representing
    # its frequence.
## delete this list and take in the data as an argument
    def __init__(self):
      self.objFreqlist = [
          (20,"Kristian"),
          (20,"Prem"),
          (5,"Nina"),
          (1,"Gabriel"),
          (1, "Minqiang"),
          (1, "Matt"),
          (1, "Shivani"),
          (1, "Jerry"),
          (1, "Michael"),
          (1, "Muwei")
          ]

    # the object has a method which returns the list, if the caller requests
    # a list of 10 words.  Otherwise it returns nothing. 
    def getTopWords(self, numberOfWords):
        if numberOfWords != 10:
          return  # return nothing unless you want my list of 10 words 
        return self.objFreqlist

  # make a new object, of type "Counts" 
  demoObject = Counts()
  
  # Call the wordle function!  The wordle function wants, as input, an object
  # which has a method called getTopWords.  The getTopWords method takes an
  # integer as its input argument, and returns a list of (frequency, word)
  # tuples. 
  wordleFromObject(demoObject, 10)


if __name__ == "__main__":
  showDemo()
