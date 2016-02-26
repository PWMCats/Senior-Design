//light routine
// test lights are on PORTD P.5,6,7

#include<avr/io.h>
#include<util/delay.h>

int main(){
 uint8_t l = 5;
 uint16_t i, ii; 
 //Init PORTD to turn on lights
 DDRD |= (1<<PD7)|(1<<PD6)|(1<<PD5); //set light pins to output
//while(1){//spin forever
 for(ii=0; ii<20; ii++){
  l++; 
  for(i=0;i<500; i++){
   PORTD |= (1<<l);
   _delay_ms(2);
   PORTD = 0;
  }
  if(l>6){l = 4;};
 }//for

}//main
