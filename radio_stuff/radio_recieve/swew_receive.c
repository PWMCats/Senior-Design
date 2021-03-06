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
#include "../swew.h" //general purpose header
#include "../uart.h" // Uses Spencer Kresge's uart_funtions

//*****************************
// SWWS Data Structures and variables

//MP3 control variables
#define PLAY  1
#define OFF 0
unsigned char playmode = 1; 
static int8_t Send_buf[8] = {0};

//nrf control variables
uint8_t temp;
uint8_t q = 0;
uint8_t data_array[4];
uint8_t tx_address[5] = {0xD7,0xD7,0xD7,0xD7,0xD7};
uint8_t rx_address[5] = {0xE7,0xE7,0xE7,0xE7,0xE7};

//snowfall variables
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
// PORT Initialization
void port_init(void){

  //Init PORTD to turn on lights
  DDRD |= (1<<PD7)|(1<<PD6)|(1<<PD5); //set light pins to output
  DDRF |= (1<<PF7); //set pin 7 to output for snowfall

}
//*****************************

//*****************************
// for testing
void light_test_routine(void){
 uint16_t i, ii; 

 for(ii=5; ii<8; ii++){
  for(i=0;i<250; i++){
   PORTD |= (1<<ii);
   _delay_ms(2);
   PORTD = 0;
  }
 }//for
}//light routine
//*****************************


//MAIN
//*****************************//*****************************
int main()
{
    CPU_PRESCALE(CPU_8MHz);
    port_init();
    adc_init(); //son of a bitch
    uart_init();
    mp3_func(CMD_SET_VOLUME, MAX_VOL);

    //deactivate relay (it's active low)
    PORTD |= 0x00;
 
    static uint8_t timeout;
    /* init hardware pins */
 //   nrf24_init();
    
    /* Channel #21 , payload length: 4 */
 //   nrf24_config(21,4);
 
    /* Set the device addresses */
 //   nrf24_tx_address(tx_address);
 //   nrf24_rx_address(rx_address);

   while(1)
   {    
        //if(playmode==PLAY){q++; if(q>50){playmode = OFF;q=0;}}

    //  while(!nrf24_dataReady()){if(timeout>1000){break;} timeout++;} //wait for transmission
    //  if(nrf24_dataReady())
      {
    //        nrf24_getData(data_array); 	
	    if(data_array[0] == 0xFF) //warning system control
	    {
	     light_func(data_array[1]);
	      mp3_func(CMD_PLAY_W_INDEX, data_array[2]);
          //    light_test_routine();
            }
  	    if(data_array[3]) //snow check is set
	    { 
	     ADCSRA |= 1<<ADSC; //request value
	     while (bit_is_clear(ADCSRA, ADIF)){} //shouldn't take long
	     reading = ADCH;
  	     data_array[3] = reading;
	    }
        }  
       
        	//*****************************
        // Radio Operation - send snow data back
	 /* Automatically goes to TX mode */
	//	  nrf24_send(data_array);        
			  
	 /* Wait for transmission to end */
 	//	  while(nrf24_isSending());

       // nrf24_powerUpRx();
	_delay_ms(500); //wait a little while longer before repeat
    }//while
}//main
/* ------------------------------------------------------------------------- */

void light_func(uint8_t new_light) //latches Federal Signal circuit
{  //toggles based on state
   static uint8_t old_light;         
   if((new_light == 0) && (old_light !=0)){set_bit(PORTD, old_light); old_light = 0;} //turn light off
   else{
    if(old_light != new_light){set_bit(PORTD, old_light); clr_bit(PORTD, new_light); old_light = new_light;} //record which light is on
   } 
}

void mp3_func(uint8_t cmd, uint8_t dat) //operates CATALEX MP3 Serial Board
{
  uint8_t i;
  if(dat > 0){
	  Send_buf[0] = 0x7e; // start byte
	  Send_buf[1] = 0xff; // version
	  Send_buf[2] = 0x06; //
	  Send_buf[3] = cmd; //
	  Send_buf[4] = 0x00;//
	  Send_buf[5] = 0x00;//datah
	  Send_buf[6] = dat; //datal
	  Send_buf[7] = 0xef; //
	  for(i=0; i<8; i++)//
	  {
		 uart_putc(Send_buf[i]) ;
	  }
	  playmode = PLAY;
  }
}
