import RPi.GPIO as GPIO

team_switch = 24 # used random GPIO pin. can change to empty one later
GPIO.setmode(GPIO.BCM)
GPIO.setup(team_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def which_team():
  if GPIO.input(team_switch) == 1:
    team = 'Blue'
  else:
    team = 'Red'
  return team
  
