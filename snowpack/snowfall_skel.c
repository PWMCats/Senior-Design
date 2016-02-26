//Snowfall Detector 
//Initial Submission

//The snowfall dectector will provide an electronic warning of when there is 2"
//or more of snow on the ground. The device will have accuracy to the tenth of an inch. 


#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <util/delay.h>
#include "display.h"

#define MAX_READ 0xFF //adc max
#define IPV  2.52//found experimentally
#define V_REF 5       
#define HR_whole 8
#define HR_dec 3


 div_t d; //global division structure
 uint16_t counter;
 uint8_t dec;
 static uint8_t val[2];
 uint8_t reading;

void adc_init(void){

  ADCSRA  |= (1<< ADEN); //| (1<< ADPS2) | (1<< ADPS1) | (1<< ADPS0);  //adc enabled, prescaled 
  ADMUX |= (1<< ADLAR) | (1<<REFS0);//left justify, use 5v reference
  ADCSRB |= (1<<MUX5); // use ADC8 on PD4, free running mode
}

void port_init(void){
  DDRB = 0xFF; //Port B all outputs
  DDRF |= 0xF0;//upper nibble of F outputs
}

void tcnt_init(void){
  //ASSR   |=  (1<<AS0);     //ext osc TOSC
  TIMSK0  |=  (1<<TOIE0);  //enable timer/counter0 overflow interrupt
  TCCR0B  |=  (1<<CS01) | (1<<CS00);  //normal mode, clock source, no prescale

  //TIMSK0  |=  1<<OCIE0;//enable timer/counter0 overflow interrupt
  //TCCR0A  |=  (1<<WGM01)
  //TCCR0B  |=  (1<<CS00); // | (1<<CS01) | (1<<CS00); //CTC mode, no prescale
 // OCR0 = 32;	//timer compare register value

}

ISR(TIMER0_OVF_vect){
 uint8_t counter = 0;
 d = div(counter, 128);
 if(d.rem == 0){
  counter = 0;
  ADCSRA |= 1<<ADSC;
  while (bit_is_clear(ADCSRA, ADIF)){} //compute time allows LED to display
  reading = 168-ADCH; 
  if(reading>168){}//noise do nothing
  else{
	  d = div((V_REF*IPV*reading),MAX_READ); //Vin * inches/volt = inches
	  dec = 0;
	  if(d.rem > 26){dec = 1;}
	  if(d.rem > 51){dec = 2;}
	  if(d.rem > 77){dec = 3;}
	  if(d.rem > 102){dec = 4;}
	  if(d.rem > 128){dec = 5;}
	  if(d.rem > 153){dec = 6;}
	  if(d.rem > 179){dec = 7;}
	  if(d.rem > 204){dec = 8;}
	  if(d.rem > 230){dec = 9;}
     
	  //place new display value

	  val[1] = d.quot%10;
	  val[0] = dec; 
   }//else
  }//if 

}//ISR

int main(void){
 //get things started
 port_init();
 adc_init();
 tcnt_init();
 sei();

 while(1){   display_7seg(val); } //display value

}//main

