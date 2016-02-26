//Severe Weather Warning Nodal Control Code
// Features:
//   User Interface communication - UART PORTD 2,3
//   Radio Communication - SPI on PORTB0,1,2,3 


//Initial Submission

//The snowfall dectector will provide an electronic warning of when there is 2"
//or more of snow on the ground. The device will have accuracy to the tenth of an inch. 

//Radio communication will be performed with nRF24L01 wireless modules 
//and the nrf24L01_plus-master AVR library

//Aural and Visual warnings will be activated with a custom designed power management system 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <util/delay.h>
#include "./nrf24L01_plus-master/nrf24.h" //AVRfreaks nrf 
#include "../uart.h" // Uses Spencer Kresge's uart_funtions

/* nrf variables ------------------------------------------------------------------------- */
uint8_t temp;
uint8_t q = 0;
uint8_t data_array[4];
uint8_t tx_address[5] = {0xE7,0xE7,0xE7,0xE7,0xE7};
uint8_t rx_address[5] = {0xD7,0xD7,0xD7,0xD7,0xD7};
/* ------------------------------------------------------------------------- */


//*****************************
// AVR Port Initialization
void port_init(void){
  DDRB |= (1<<PB5)|(1<<PB6)|(1<<PB7); //turn on pwm
  DDRF |= 0xF0;//upper nibble of F outputs
}
//*****************************


//*****************************
// Timer/Counter Initialization
void tcnt_init(void){

  TIMSK0  |=  (1<<TOIE0);  //enable timer/counter0 overflow interrupt
  TCCR0B  |=  (1<<CS01) | (1<<CS00);  //normal mode, clock source, no prescale

  //Configure TIMER1 for PWM output
  TCCR1A|=(1<<COM1A1)|(1<<COM1B1)|(1<<COM1C1)|(1<<WGM11); //NON Inverted PWM
  TCCR1B|=(1<<WGM13)|(1<<WGM12)|(1<<CS10); //PRESCALER=64 MODE 14(FAST PWM)

  ICR1=4999;  //fPWM=423.6Hz (Period = 2.4ms Standard). 
}
//*****************************

//Assigns PWM bottom to vary wavelength
void light_em_up(uint8_t i){
   OCR1A= light_val[i][2]; 
   OCR1B= light_val[i][1];
   OCR1C= light_val[i][0];
}

//slow down clock for low-voltage performance 
#define CPU_PRESCALE(n) (CLKPR = 0x80, CLKPR = (n))
#define CPU_8MHz        0x01

int main(void){
 CPU_PRESCALE(CPU_8MHz);

 port_init();
 tcnt_init();
 uart_init();
 light_em_up(7);
 nrf24_init();
 nrf24_config(21,4); //channel #21, payload length 4

 nrf24_tx_address(tx_address);
 nrf24_rx_address(rx_address);

 uint8_t light, track, snow; //for uart

 while(1){ //serial forever

  while(uart_getc() != 0xFF){} //wait for start byte
  light = uart_getc();
  track = uart_getc();
  snow = uart_getc();

	//*****************************
        // Radio Operation
        /* Fill the data buffer */
        data_array[0] = 0xFF;
        data_array[1] = light;
        data_array[2] = track;
        data_array[3] = snow;                                    

 /* Automatically goes to TX mode */
        nrf24_send(data_array);        
        
        /* Wait for transmission to end */
        while(nrf24_isSending());
        
        /* Make analysis on last tranmission attempt */
        temp = nrf24_lastMessageStatus();	      
        
        if(temp == NRF24_TRANSMISSON_OK)
        {                    
            uart_putc('O'); //O for ok
        }
        else if(temp == NRF24_MESSAGE_LOST)
        {                    
            uart_putc('L'); //L for lost
        }
        else{uart_putc('N');} //N for no response

		/* Retranmission count indicates the tranmission quality */
		temp = nrf24_retransmissionCount();
      uart_putc(temp); //send the quality

      nrf24_powerUpRx();
   
      if(nrf24_dataReady()){nrf24_getData(data_array);} //loads data array

     //check if correct data came back
     snow = data_array[3];
     uart_putc(snow);
     _delay_ms(100); //wait a little while before repeat

 }//while
}//main

