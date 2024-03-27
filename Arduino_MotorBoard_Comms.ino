int datafromUser=0;
int enA = 9;
int in1 = 8;
int in2 = 7;
int enB = 3;
int in3 = 5;
int in4 = 4;
// sets variables for the pins on the motorboard 
void setup() {
  
  pinMode( LED_BUILTIN , OUTPUT ); //declares the pins used and what theyll be used for
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  Serial.begin(9600); 
  //opens serial port 9600 for communication

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(enA, 255);
  analogWrite(enB, 255);
  //sets motor board pins to base state as well as declare motor speed
}

void loop() { //infinite loop
  
  if(Serial.available() > 0)
  {
    datafromUser=Serial.read(); 
    // reads data sent to the port
  }

//these two commands used for testing and debugging
  if(datafromUser == '1')
  {
    digitalWrite( LED_BUILTIN , HIGH ); 
    //turns one of the pins on if the arduino is sent '1'
  }
  else if(datafromUser == '0')
  {
    digitalWrite( LED_BUILTIN, LOW);
    //turns one of the pins off if the arduino is sent '0'
  }

  //These two are what is implemented in the main python algorithm
  if(datafromUser == '2')
  {
    
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    //turns the odd pins on if the arduino is sent '2' turning the motor on spinning clockwise
  }
  else if(datafromUser == '3')
  {
    
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    //turns the pins off if the arduino is sent '3'
  }
}
