#include <avr/io.h>
#include <stdint.h>
#include "./nrf24L01_plus-master/nrf24.h"
#include <util/delay.h>
#include "../swew.h" //general purpose header
#include "../uart.h" // Uses Spencer Kresge's uart_funtions



//*****************************
void latch(uint8_t light_pin){
  uint8_t i;

  set_bit(PORTD, light_pin);
  for(i=0; i<100; i++){
	_delay_ms(2); //200ms pulse
  }
  clr_bit(PORTD, light_pin); //toggles latch
}
//*****************************


//MAIN
//*****************************//*****************************
int main()
{
    DDRD |= 0xF0;
    DDRF |= 0x00;
    CPU_PRESCALE(CPU_8MHz);
    while(1){
      if(
