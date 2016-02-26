//testing serial for Severe Weather Warning System
//T Love 2/18/16

#include<avr/io.h>
#include <stdio.h>
#include<util/delay.h>
#include <stdlib.h>
#include"uart_functions.h" // Uses Roger Traylor's uart_funtions
#include <string.h>
#include <avr/interrupt.h>

//sorry Rog, i did not write this in vim...

int main(){

 uart_init();
 char c; //for uart

 //Init PORTD to turn on lights
 DDRD |= (1<<PD7)|(1<<PD6)|(1<<PD5); //set light pins to output
 int i = 0;

 while(1){ //serial forever

   c = uart_getc();

	switch(c){
     
     case 'b' : 
      for(i=0;i<500; i++){
       PORTD |= (1<<5);
       _delay_ms(2);
       PORTD &= (0<<5);
      }

     case 'y' : 
      for(i=0;i<500; i++){
       PORTD |= (1<<5);
       _delay_ms(2);
       PORTD &= (0<<5);
      }

     case 'r' : 
      for(i=0;i<500; i++){
       PORTD |= (1<<5);
       _delay_ms(2);
       PORTD &= (0<<5);
      }

  }//switch
 }//while
}//main




