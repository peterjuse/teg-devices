import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("Hola Coromoto!", 1,0)
mylcd.lcd_display_string("Bienvenida a casa",2,0)

#str_pad = " " * 16
#my_long_string = "Hola Maru! Buen provecho corazon <3!"
#my_long_string = str_pad + my_long_string

#while True:
#    for i in range (0, len(my_long_string)):
#        lcd_text = my_long_string[i:(i+16)]
#        mylcd.lcd_display_string(lcd_text,1)
#        sleep(0.4)
#        mylcd.lcd_display_string(str_pad,1)
