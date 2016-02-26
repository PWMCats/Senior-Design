/*
* ----------------------------------------------------------------------------
* “THE COFFEEWARE LICENSE” (Revision 1):
* <ihsan@kehribar.me> wrote this file. As long as you retain this notice you
* can do whatever you want with this stuff. If we meet some day, and you think
* this stuff is worth it, you can buy me a coffee in return.
* -----------------------------------------------------------------------------
*/

#include <avr/io.h>
#include <stdint.h>
#include "./nrf24L01_plus-master/nrf24.h"
#include <util/delay.h>

uint8_t temp;
uint8_t q = 0;
uint8_t data_array[4];
uint8_t tx_address[5] = {0xD7,0xD7,0xD7,0xD7,0xD7};
uint8_t rx_address[5] = {0xE7,0xE7,0xE7,0xE7,0xE7};
/* ------------------------------------------------------------------------- */
void light_routine(void){
 uint8_t l = 5;
 uint16_t i, ii; 
 //Init PORTD to turn on lights
 DDRD |= (1<<PD7)|(1<<PD6)|(1<<PD5); //set light pins to output
//while(1){//spin forever
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

//slow down clock for low-voltage performance 
#define CPU_PRESCALE(n) (CLKPR = 0x80, CLKPR = (n))
#define CPU_8MHz        0x01

int main(void){
 CPU_PRESCALE(CPU_8MHz);

    /* init hardware pins */
    nrf24_init();
    
    /* Channel #21 , payload length: 4 */
    nrf24_config(21,4);
 
    /* Set the device addresses */
    nrf24_tx_address(tx_address);
    nrf24_rx_address(rx_address);

    while(1)
    {    
        if(nrf24_dataReady())
        {
            nrf24_getData(data_array);
            if(data_array[2] == 0x55){
              light_routine();
            }        
         /*   xprintf("> ");
            xprintf("%2X ",data_array[0]);
            xprintf("%2X ",data_array[1]);
            xprintf("%2X ",data_array[2]);
            xprintf("%2X\r\n",data_array[3]); */
        }
    }
}
/* ------------------------------------------------------------------------- */
