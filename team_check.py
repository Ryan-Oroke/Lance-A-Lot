import RPi.GPIO as GPIO

team_switch = 30 # used random GPIO pin. can change to empty one later
GPIO.setmode(GPIO.BCM)
GPIO.setup(team_switch, GPIO.IN)

def which_team():
  if team_switch == True:
    team = 'Blue'
  else
    team = 'Red'
  return team
  
