//Snowfall Detector 
//Initial Submission

//The snowfall dectector will provide an electronic warning of when there is 2"
//or more of snow on the ground. The device will have accuracy to the tenth of an inch. 

//IDEAS
//read 10bit ACD and calculate estimated distance from ground  
//UART data to terminal 

//init ADC
/***********************************************************************/
//                            adc_init                               
//Initalizes the adc on the mega32u4. 
/***********************************************************************/

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




void adc_init(void){

  ADCSRA  |= (1<< ADEN); //| (1<< ADPS2) | (1<< ADPS1) | (1<< ADPS0);  //adc enabled, prescaled 
  ADMUX |= (1<< ADLAR) | (1<<REFS0);//left justify, use 5v reference
  ADCSRB |= (1<<MUX5); // use ADC8 on PD4, free running mode
}

void port_init(void){
  DDRB = 0xFF; //Port B all outputs
  DDRF |= 0xF0;//upper nibble of F outputs
};

int main(void){
 div_t d;
 uint16_t counter;
 uint8_t dec, val[2];
 uint8_t reading;
 sei();
 //get things started
 port_init();
 adc_init();

  while(1){ //convert adc value
 
	  ADCSRA |= 1<<ADSC;
	  while (bit_is_clear(ADCSRA, ADIF)){} //compute time allows LED to display
	  reading = ADCH; 
     if(reading>168){}//noise do nothing
     else{
		  d = div((V_REF*IPV*reading),MAX_READ); //Vin * inches/volt = inches

		  dec = 0;
        /* 10-bit ladder
		  if(d.rem > 102){dec = 1;}
		  if(d.rem > 205){dec = 2;}
		  if(d.rem > 307){dec = 3;}
		  if(d.rem > 409){dec = 4;}
		  if(d.rem > 511){dec = 5;}
		  if(d.rem > 614){dec = 6;}
		  if(d.rem > 716){dec = 7;}
		  if(d.rem > 818){dec = 8;}
		  if(d.rem > 921){dec = 9;}
        */
		  if(d.rem > 26){dec = 1;}
		  if(d.rem > 51){dec = 2;}
		  if(d.rem > 77){dec = 3;}
		  if(d.rem > 102){dec = 4;}
		  if(d.rem > 128){dec = 5;}
		  if(d.rem > 153){dec = 6;}
		  if(d.rem > 179){dec = 7;}
		  if(d.rem > 204){dec = 8;}
		  if(d.rem > 230){dec = 9;}
	 
      // if(~(counter%10000)){
		  //subtract and multiply to find snowfall
		  if((HR_whole - d.quot) < 0){} //error value
		  else{val[1] = HR_whole - d.quot;} //don't measure that high! 
		  if((HR_dec - dec) < 0){
			 val[1]-=1;
			 val[0] = (10+HR_dec) - dec;
		  }
		  else{ val[0] = d.quot; val[1] = HR_dec - dec;} 
	 // }
 
        
		  //display latest measurement
     
		  val[2] = (d.quot%100)/10;
		  val[1] = d.quot%10;
		  val[0] = dec; 
		 /*
         //ADC Validation
		  val[2] = (reading%1000)/100;
		  val[1] = (reading%100)/10;
		  val[0] = reading%10;
        */
		  display_7seg(val);
     }//else
  //   counter++;
    // if(counter>65000){counter = 0;} 
  }//while
}//main

