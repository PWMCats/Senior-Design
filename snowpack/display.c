//TekBots 4-digit 7seg LED Display Drive
//T.Love 12/9

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <util/delay.h>

uint8_t disp_ret(uint8_t div_val){//return display value
 switch(div_val){         //grounded pins make blinky blinky
  case 0: //dgfedcba
   return 0b11000000;
  case 1:
   return 0b11111001;
  case 2: 
   return 0b10100100;
  case 3:
   return 0b10110000;
  case 4:
   return 0b10011001;
  case 5: 
   return 0b10010010;
  case 6:
   return 0b10000010;
  case 7:
   return 0b11111000;
  case 8:
   return 0b10000000;
  case 9: 
   return 0b10010000;  
  default: //never happens, light em up
   return 0x00;
 }//switch
}//disp_ret


void display_7seg(uint8_t *val){
	//these are given, use appropriate port_init
   uint8_t i;
   uint8_t display[4] = {0, 1, 3, 4};

   for(i=0;i<sizeof(val); i++){
    if(i!=1){PORTB = disp_ret(val[i]);}
    else{PORTB = (disp_ret(val[i]) & 0x7F);}
    //PORTB = disp_ret(val[i]);
    PORTF = display[i]<<4;
    _delay_ms(2);
   }//for
}

    
	  
