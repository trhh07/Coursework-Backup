int datafromUser=0;
void setup() {
  
  pinMode( LED_BUILTIN , OUTPUT ); //declares the pins used and what they'll be used for
  pinMode( 7, OUTPUT);
  Serial.begin(9600); //opens serial port 9600 for communication
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
  if(datafromUser == 'fireOn')
  {
    digitalWrite( 7, HIGH);
    //turns one of the pins on if the arduino is sent 'fireOn'
  }
  else if(datafromUser == 'fireOff')
  {
    digitalWrite( 7, LOW);
    //turns one of the pins off if the arduino is sent 'fireOff'
  }
}
