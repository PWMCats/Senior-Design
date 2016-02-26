//Severe Weather Warning Nodal Control Code
// Features:
//   Snow Pack detector 
//   Radio Communication - TODO
//   Aural Warning System Activation Sequence - TODO
//   Visual Warning System Activation Sequence - TODO

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
//#include "display.h"
#include "./nrf24L01_plus-master/nrf24.h"


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

/* ------------------------------------------------------------------------- */
uint8_t temp;
uint8_t q = 0;
uint8_t data_array[4];
uint8_t tx_address[5] = {0xE7,0xE7,0xE7,0xE7,0xE7};
uint8_t rx_address[5] = {0xD7,0xD7,0xD7,0xD7,0xD7};
/* ------------------------------------------------------------------------- */

//*****************************


//*****************************
// ADC Initialization
void adc_init(void){

  ADCSRA  |= (1<< ADEN); //| (1<< ADPS2) | (1<< ADPS1) | (1<< ADPS0);  //adc enabled, prescaled 
  ADMUX |= (1<< ADLAR) | (1<<REFS0);//left justify, use 5v reference
  ADCSRB |= (1<<MUX5); // use ADC8 on PD4, free running mode
}
//*****************************


//*****************************
// AVR Port Initialization
void port_init(void){
  DDRB = 0xFF; //Port B all outputs
  DDRF |= 0xF0;//upper nibble of F outputs
}
//*****************************



//*****************************
// Timer/Counter Initialization
void tcnt_init(void){
  //ASSR   |=  (1<<AS0);     //ext osc TOSC
  TIMSK0  |=  (1<<TOIE0);  //enable timer/counter0 overflow interrupt
  TCCR0B  |=  (1<<CS01) | (1<<CS00);  //normal mode, clock source, no prescale
}
//*****************************


//*****************************
// Interrupt Service Routine
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

//slow down clock for low-voltage performance 
#define CPU_PRESCALE(n) (CLKPR = 0x80, CLKPR = (n))
#define CPU_8MHz        0x01

int main(void){
 CPU_PRESCALE(CPU_8MHz);

 port_init();
 adc_init();
 tcnt_init();
 nrf24_init();
 nrf24_config(21,4); //channel #21, payload length 4

 nrf24_tx_address(tx_address);
 nrf24_rx_address(rx_address);

 sei();

 while(1){  
 // display_7seg(val); //display value

	//*****************************
        // Radio Operation
        /* Fill the data buffer */
        data_array[0] = 0x00;
        data_array[1] = 0xAA;
        data_array[2] = 0x55;
        data_array[3] = q++;                                    

        /* Automatically goes to TX mode */
        nrf24_send(data_array);        
        
        /* Wait for transmission to end */
        while(nrf24_isSending());

        /* Make analysis on last tranmission attempt */
        temp = nrf24_lastMessageStatus();	      
        
        if(temp == NRF24_TRANSMISSON_OK)
        {                    
            //xprintf("> Tranmission went OK\r\n");
            // TODO
        }
        else if(temp == NRF24_MESSAGE_LOST)
        {                    
            //xprintf("> Message is lost ...\r\n");    
				// TODO
        }

		/* Retranmission count indicates the tranmission quality */
		temp = nrf24_retransmissionCount();
	//	xprintf("> Retranmission count: %d\r\n",temp);

		/* Optionally, go back to RX mode ... */
	//	nrf24_powerUpRx();

		/* Or you might want to power down after TX */
		// nrf24_powerDown();            

		/* Wait 5000 seconds ... */
		_delay_ms(5000);
 }//while
}//main

