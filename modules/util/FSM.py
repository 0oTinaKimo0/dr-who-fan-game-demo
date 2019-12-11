# FSM for the angels' behavior
class FSM(object):
   def __init__(self, state="frozen"):
      self._state = state


   def manageState(self, seen, tState):
      if not seen and self._state == "frozen":
         self._setState("moving")

      elif not seen and self._state == "moving" and tState:
         self._setState("chasing")

      elif not seen and self._state == "frozen" and tState:
         self._setState("chasing")
         
      elif seen and self._state == "moving":
         self._setState("frozen")

      elif seen and self._state == "chasing":
         self._setState("frozen")
      
   
   def _setState(self, state):
      self._state = state
      
   
   def __eq__(self, state):
      return self._state == state
   
