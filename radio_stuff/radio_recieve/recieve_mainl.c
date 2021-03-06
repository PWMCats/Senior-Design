/* nrf license
* ----------------------------------------------------------------------------
* “THE COFFEEWARE LICENSE” (Revision 1):
* <ihsan@kehribar.me> wrote this file. As long as you retain this notice you
* can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a coffee in return.
* -----------------------------------------------------------------------------
*/

#include <avr/io.h>
#include <stdint.h>
#include "./nrf24L01_plus-master/nrf24.h"
#include <util/delay.h>

// swew.h
uint8_t temp;
uint8_t q = 0;
uint8_t data_array[4];
uint8_t tx_address[5] = {0xD7,0xD7,0xD7,0xD7,0xD7};
uint8_t rx_address[5] = {0xE7,0xE7,0xE7,0xE7,0xE7};
/* ------------------------------------------------------------------------- */
#define MAX_READ 0xFF //adc max
#define IPV  2.52//found experimentally
#define V_REF 5       
#define HR_whole 8
#define HR_dec 3

//*****************************
// SWWS Data Structures and variables

 div_t d; //global division structure
 uint16_t counter;
 uint8_t dec;
 static uint8_t val[2];
 uint8_t reading;

//*****************************
// ADC Initialization
void adc_init(void){

  ADCSRA  |= (1<< ADEN);//adc enabled
  ADMUX |= (1<< ADLAR) | (1<<REFS0);//left justify, use 5v reference
  ADCSRB |= (1<<MUX5); // use ADC8 on PD4, free running mode
}
//*****************************

//*****************************
void latch(uint8_t light_pin){

	  set_bit(PORTD, light_pin);
	  for(i=0; i<100; i++){
		_delay_ms(2); //200ms pulse
	  }
	  clr_bit(PORTD, light_pin); //toggles latch
}
//*****************************

//*****************************
// for testing
void light_test_routine(void){

 uint8_t l = 5;
 uint16_t i, ii; 

 for(ii=0; ii<6; ii++){
  l++; 
  for(i=0;i<250; i++){
   PORTD |= (1<<l);
   _delay_ms(2);
   PORTD = 0;
  }
  if(l>6){l = 4;};
 }//for
}//light routine
//*****************************


//MAIN
//*****************************//*****************************
int main()
{

    /* init hardware pins */
    nrf24_init();
    
    /* Channel #21 , payload length: 4 */
    nrf24_config(21,4);
 
    /* Set the device addresses */
    nrf24_tx_address(tx_address);
    nrf24_rx_address(rx_address);

    //Init PORTD to turn on lights
    DDRD |= (1<<PD7)|(1<<PD6)|(1<<PD5); //set light pins to output
    DDRF |= (1<<PF7); //set pin 7 to output

    //uart_init();
    //set_vol(LOUD); mp3 stuff

//             Acknowledgement Bit Map
//bit 0          1         2        3        4       5      6
//    lightning, wind_25 , wind_35, wind_50, manual, snowy, test; 
static uint8_t last_ack = 0xFF; //full dummy byte
uint8_t ack; //from master

    while(1)
    {    
        if(nrf24_dataReady())
        {
            nrf24_getData(data_array); //loads data array

			 //acknowledgement byte
			 switch(data_array[0]){
           case 'N' : 
             ack = 0;
           case 'L' : //lightning lightning lighting
             set_bit(ack,LIGHTNING); //acknowledge lightning 
				 break;
           case 0x25 : //windspeeds exceeding 25mph
             set_bit(ack,WIND_25);
             break;
           case 0x35 : //windspeeds exceeding 35mph
             set_bit(ack,WIND_35);  
             break;
           case 0x50 : //windspeeds exceeding 50mph
             set_bit(ack,WIND_50); 
             break;
           case 'M' : //manual input
 		 		set_bit(ack,MAN); 
	 	     case 'S' : //snowy triggered by temperature

           case 'T' : //testing
 				set_bit(ack,TEST); 
          }

		  if (last_ack == ack){};//already acknowledged and task is completed
		  else{ //take action

         manl = data_array[1];

			//control node
			switch(ack){
          case 0: //returns system to neutral state
           switch(last_ack){
            case 0x01 : 
             latch(LIGHTNING); //turn off red light
				break;

            case 0x02 : 
             latch(WIND_25); //turn off blue light
				break;

            case 0x04  :
             latch(WIND_35); //turn off yellow light
				break;

            case 0x08  :
             latch(WIND_50); //turn off red light
				break;

            case 0x10  :
             latch(last_manl); //turn off whatever light was on
				break;
           }

          case 0x01 : //set lightning
           //play_track(LIGHTNING);
           latch(LIGHTNING); //turn on red light
           break;

          case 0x02 : //set wind
           //play_track(WIND_25);
             latch(WIND_25); //turn on blue light
				break;

          case 0x04  :
           //play_track(WIND_25);
             latch(WIND_35); //turn on yellow light
				break;

          case 0x08  :
           //play_track(WIND_25);
             latch(WIND_50); //turn on red light
				break;

          case 0x10  :       //set manual
             latch(manl); //turn on whatever light 
				break;

          case 0x20  :      //do the test
             light_test_routine();
            break;
          }//control switch
        data_array[0] = ack;
        last_ack = ack;
        ack = 0; //ack reset
        last_manl = manl;
        
            if(data_array[2] == 0x55){
              light_test_routine();
            }  

		  ADCSRA |= 1<<ADSC; //request value
		  while (bit_is_clear(ADCSRA, ADIF)){} //shouldn't take long
		  reading = 168-ADCH; 
	
		  data_array[1] = reading;

        //check if correct data came back
        if(data_array[2] != 'S'){/*error*/});
        data_array[2] =     'O';
        if(data_array[2] != '!'){/*error*/});
        data_array[3] =     'U'; 
      

    }
}
/* ------------------------------------------------------------------------- */
