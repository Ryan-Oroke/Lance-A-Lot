
//Libraries
#include <Wire.h>

// CONSTANTS
static bool PRINT_I2C_INPUTS = true;
static int I2C_COMMAND_LENGTH = 5;

//Motor Driver Pins are named after the chip pins
int MOTOR_ENABLE_PIN = 8; //HIGH allows for motor operation, LOW prevents it
int PWMA_PIN = 5, AI1_PIN = 6, AI2_PIN = 7;
int PWMB_PIN = 11, BI1_PIN = 10, BI2_PIN = 9;
int motor_a_speed = 0, motor_b_speed = 0;
bool motor_a_forward = true, motor_b_forward = true;

void setup() {
      //Establish a connections
      Serial.begin(9600);
      Wire.begin(54);               //Give Arduino Address 54 (0x36)
      Wire.onReceive(receiveEvent); //Register Event Reception Function

      //Set all of the pins to outputs and low
      pinMode(MOTOR_ENABLE_PIN, OUTPUT);  digitalWrite(MOTOR_ENABLE_PIN, LOW);
      pinMode(PWMA_PIN, OUTPUT);          analogWrite(PWMA_PIN, 0);
      pinMode(AI1_PIN, OUTPUT);           digitalWrite(AI1_PIN, LOW);
      pinMode(AI2_PIN, OUTPUT);           digitalWrite(AI2_PIN, LOW);
      pinMode(PWMB_PIN, OUTPUT);          analogWrite(PWMB_PIN, 0);
      pinMode(BI1_PIN, OUTPUT);           digitalWrite(BI1_PIN, LOW);
      pinMode(BI2_PIN, OUTPUT);           digitalWrite(BI2_PIN, LOW);

      //Enable the motor outputs
      digitalWrite(MOTOR_ENABLE_PIN, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Run the motors

  delay(100);
}

void receiveEvent(int howMany)
{
  char c;
  String input = ""; // Variable to collect message
  while(1 < Wire.available()) // loop through all but the last
  {
    c = Wire.read(); // receive byte as a character
    input = input + c;
  }
  c = Wire.read();    // receive last byte
  input = String(input + c);
  if(PRINT_I2C_INPUTS){
    Serial.println(input);
  }

  if(input.length() == I2C_COMMAND_LENGTH){
  
    //Act on the String Input
    int motorForward = 0;
    int motorSpeed = 0;
    
    //Check Direction
    if(input[2] == "F"){
      //Move Motor A Forward
      motorForward = 1;
    }else if(input[2] == "B"){
      //Move Motor A Backward
      motorForward = -1;
    }
  
    //Get Speed (convert chars to string to int)
    motorSpeed = String(input[3]+input[4]+input[5]).toInt();
  
    
    if(input[1] == "A"){
      //Motor A
      driveMotorA(motorForward*motorSpeed);
    }else if(input[1] == "B"){
      driveMotorB(motorForward*motorSpeed);
    }else{
      Serial.println("ERROR PICKING MOTOR");
    }
  }else{
    //I2C Message was too short or too long. 
    Serial.print("ERROR: The I2C Message ('");
    Serial.print(input);
    Serial.print(") was not the correct length (");
    Serial.print(I2C_COMMAND_LENGTH);
    Serial.println(")");
  }
}

void driveMotorA(int s){
        Serial.print("Motor A: ");
        Serial.println(s);
        
        if(s >= 0){
          //Drive the motor forward (CW)
          digitalWrite(AI1_PIN, HIGH);
          digitalWrite(AI2_PIN, LOW);
          analogWrite(PWMA_PIN, s);
        }else{
          //Drive the motor backwards (CCW)
          digitalWrite(AI1_PIN, LOW);
          digitalWrite(AI2_PIN, HIGH);
          analogWrite(PWMA_PIN, -1*s);
        }
}

void driveMotorB(int s){
        Serial.print("Motor B: ");
        Serial.println(s);
        
        if(s <= 0){
          //Drive the motor forward (CW)
          digitalWrite(BI1_PIN, HIGH);
          digitalWrite(BI2_PIN, LOW);
          analogWrite(PWMB_PIN, s);
        }else{
          //Drive the motor backwards (CCW)
          digitalWrite(BI1_PIN, LOW);
          digitalWrite(BI2_PIN, HIGH);
          analogWrite(PWMB_PIN, -1*s);
        }
}
