class FSM(object):
   def __init__(self, state="frozen"):
      self._state = state


   def manageState(self, seen, tState):
      if seen == False and self._state == "frozen":
         self._setState("moving")

      elif seen == False and self._state == "moving" and tState == True:
         self._setState("chasing")
         
      elif seen == True and self._state == "moving":
         self._setState("frozen")
      
   
   def _setState(self, state):
      self._state = state
      
   
   def __eq__(self, state):
      return self._state == state
   
