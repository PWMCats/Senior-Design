//display.h

//run this in main to show a value with precision to the 1/10th

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <util/delay.h>

//function headers
uint8_t disp_ret(uint8_t div_val);
void display_7seg(uint8_t *val);
