//swew.h
// general purpose header file for macros and constants
#ifndef SWEW_H_
#define SWEW_H_

//slow down clock for low-voltage performance 
#define CPU_PRESCALE(n) (CLKPR = 0x80, CLKPR = (n))
#define CPU_8MHz        0x01

#define set_bit(reg,bit) reg |= (1<<bit)
#define clr_bit(reg,bit) reg &= ~(1<<bit)
#define check_bit(reg,bit) (reg&(1<<bit))


/************MP3 Command bytes**************************/
#define CMD_NEXT_SONG 0X01
#define CMD_PREV_SONG 0X02
#define CMD_PLAY_W_INDEX 0X03
#define CMD_VOLUME_UP 0X04
#define CMD_VOLUME_DOWN 0X05
#define CMD_SET_VOLUME 0X06
#define MAX_VOL 30
#define CMD_SINGLE_CYCLE_PLAY 0X08
#define CMD_SEL_DEV 0X09
  #define DEV_TF 0X02
#define CMD_SLEEP_MODE 0X0A
#define CMD_WAKE_UP 0X0B
#define CMD_RESET 0X0C
#define CMD_PLAY 0X0D
#define CMD_PAUSE 0X0E
#define CMD_PLAY_FOLDER_FILE 0X0F
#define CMD_STOP_PLAY 0X16
#define CMD_FOLDER_CYCLE 0X17
#define CMD_SHUFFLE_PLAY 0X18
#define CMD_SET_SINGLE_CYCLE 0X19
  #define SINGLE_CYCLE_ON 0X00
  #define SINGLE_CYCLE_OFF 0X01
#define CMD_SET_DAC 0X1A
  #define DAC_ON  0X00
  #define DAC_OFF 0X01
#define CMD_PLAY_W_VOL 0X22

//Trevor Love's RGB Lookup Table
                                //   R     G     B
    uint16_t light_val[8][3] ={  {3000,    0,    0}, //red 
                                 {4000,  600,    0}, //yellow
                                 {   0, 3000,    0}, //green
                                 {   0,    0, 3000}, //blue
                                 {1000,    0, 3000}, //purple
                                 {2000,  200,  300},  //pink 
                                 {2000,  100,    0}, //orange
                                 {   0,    0,    0}  }; 
//*****************************

//functions
void light_func(uint8_t state);
void mp3_func(uint8_t cmd, uint8_t dat);

#endif
