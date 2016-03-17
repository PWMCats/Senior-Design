#include <avr/io.h>
#include <stdint.h>
#include <util/delay.h>
#include "swew.h" //general purpose header
#include "uart.h" // Uses Spencer Kresge's uart_funtions

//*****************************
// SWWS Data Structures and variables

//MP3 control variables
#define PLAY  1
#define OFF 0
unsigned char playmode = 1; 
static int8_t Send_buf[8] = {0};

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
  DDRB |= 0xFF;
  DDRD |= (1<<PD7)|(1<<PD6)|(1<<PD5); //set light pins to output
  DDRF |= (1<<PF7); //set pin 7 to output for snowfall

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


//MAIN
//*****************************//*****************************
int main()
{
    CPU_PRESCALE(CPU_8MHz);
    port_init();
    //deactivate relay (it's active low)
    PORTD |= 0xE0;
    adc_init(); 
    uart_init();
    mp3_func(CMD_SET_VOLUME, MAX_VOL);
    tcnt_init();

    uint8_t start,light, track, snow; //for uart
    static uint8_t timeout;

   while(1)
   {    
	  start = uart_getc();//wait for start byte
	  light = uart_getc();
	  if(light == 5){light_em_up(BLUE);}
	  else if(light == 6){light_em_up(YELLOW);}
	  else if(light == 7){light_em_up(RED);}
	  else{light_em_up(7);}

	  track = uart_getc();
	  snow = uart_getc();

	    if(start == 0xFF) //warning system control
	    {
	     light_func(light);
	      mp3_func(CMD_PLAY_W_INDEX, track);
            }
  	    if(snow) //snow check is set
	    { 
	     ADCSRA |= 1<<ADSC; //request value
	     while (bit_is_clear(ADCSRA, ADIF)){} //shouldn't take long
	     reading = ADCH;
  	     snow = reading;
	    }
        
        uart_putc('O');
        uart_putc(snow); 
	_delay_ms(500); //wait a little while longer before repeat
    }//while
}//main
/* ------------------------------------------------------------------------- */

void light_func(uint8_t new_light) //latches Federal Signal circuit
{  //toggles based on state
   static uint8_t old_light;         
   if((new_light == 0) && (old_light !=0)){
    set_bit(DDRD, old_light); 
    set_bit(PORTD, old_light); 
    old_light = 0;
   } //turn light off
   else{
    if(old_light != new_light){
     set_bit(DDRD,  old_light);
     set_bit(PORTD, old_light); 
     set_bit(DDRD,  new_light); 
     clr_bit(PORTD, new_light); 
     old_light = new_light;
    } //record which light is on
   } 
}

void mp3_func(uint8_t cmd, uint8_t dat) 
{
  clr_bit(PORTB, (dat-1));

  /*uint8_t i; //operates CATALEX MP3 Serial Board
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
  }*/
}
