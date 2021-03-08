
//Motor Driver Pins are named after the chip pins
int MOTOR_ENABLE_PIN = 8; //HIGH allows for motor operation, LOW prevents it
int PWMA_PIN = 5, AI1_PIN = 6, AI2_PIN = 7;
int PWMB_PIN = 11, BI1_PIN = 10, BI2_PIN = 9;
int motor_a_speed = 0, motor_b_speed = 0;
bool motor_a_forward = true, motor_b_forward = true;

void setup() {
      //Establish a serial connection
      Serial.begin(9600);

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

  driveMotorA(100);
  driveMotorB(100);
  delay(1000);
  driveMotorA(-100);
  driveMotorB(-100);
  delay(1000);
  
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
        
        if(s >= 0){
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
