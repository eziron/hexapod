
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/clocks.h"
#include "hardware/irq.h"
#include "pico/multicore.h"
#include "hardware/pwm.h"
#include "rp_lidar.h"


#define BAUD_RATE0 115200
#define UART0_TX_PIN 0
#define UART0_RX_PIN 1

#define BAUD_RATE1 2000000
#define UART1_TX_PIN 8
#define UART1_RX_PIN 9

#define led_pin 25

uint8_t RX_buffer[132];

int main() {
    set_sys_clock_khz(240000,true);
    
    uart_init(uart0, BAUD_RATE0);
    gpio_set_function(UART0_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART0_RX_PIN, GPIO_FUNC_UART);
    uart_set_fifo_enabled(uart0,true);
    

    uart_init(uart1, BAUD_RATE1);
    gpio_set_function(UART1_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART1_RX_PIN, GPIO_FUNC_UART);
    uart_set_fifo_enabled(uart1,true);

    // Initialize LED pin
    gpio_init(led_pin);
    gpio_set_dir(led_pin, GPIO_OUT);

    // Initialize chosen serial port
    stdio_init_all();

    // Habilito la interrupcion en el puerto serial del lidar
    irq_set_exclusive_handler(UART0_IRQ, lidar_on_uart_rx);
    irq_set_enabled(UART0_IRQ, true);

    // ejecuto en el core1 el codigo encargado de decodificar 
    // los valores enviados por el lidar y re enviarlos en RAW a la PC
    multicore_launch_core1(lidar_core1_entry);
   
    while (true) {

    }
}