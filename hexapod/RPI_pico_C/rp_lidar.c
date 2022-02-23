#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/irq.h"
#include "pico/multicore.h"
#include "hardware/pwm.h"
#include "rp_lidar.h"


const uint8_t stop_scan_bytes[] = {0xA5,0x25};
const uint8_t reset_lidar_bytes[] = {0xA5,0x40};

const uint8_t star_normal_scan_bytes[] = {0xA5,0x20};
const uint8_t star_force_scan_bytes[] = {0xA5,0x21};
const uint8_t star_legacy_scan_bytes[] = {0xA5,0x82,0x05,0x00,0x00,0x00,0x00,0x00,0x22};
const uint8_t star_extended_scan_bytes[] = {0xA5,0x82,0x05,0x02,0x00,0x00,0x00,0x00,0x20};

uint8_t scan_mode = 0;



uint8_t rx_C = 0;
uint8_t rx_buffer[132];
uint rx_count = 0;
uint rx_lim = 0;
bool synq_byte_en = true;

void lidar_core1_entry() {
    while (1) {
        int32_t g = multicore_fifo_pop_blocking();
        //codigo de decodificacion de los datos del lidar
        multicore_fifo_push_blocking(1);
    }
}

void lidar_on_uart_rx() {
    if(!lidar_rx_finished){
        while (uart_is_readable(lidar_uart)) {
            rx_C = uart_getc(lidar_uart);
            if(synq_byte_en){
                if(
                    (rx_count == 0 && (rx_C >> 4) == lidar_synq_byte1) ||
                    (rx_count == 1 && (rx_C >> 4) == lidar_synq_byte2) ||
                    (rx_count > 1)
                ){
                    rx_buffer[rx_count] = rx_C;
                    rx_count++;
                }
                else{
                    rx_count = 0;
                }             
            }
            else{
                rx_buffer[rx_count] = rx_C;
                rx_count++;
            }
            if(rx_count == rx_lim){
                lidar_rx_finished = true;
            }
        }
    }
    
}

uint64_t us_ref;
void wait_lidar_response(uint64_t time_out){
    us_ref = time_us_64();
    while (lidar_rx_finished == false && time_us_64() - us_ref < time_out)
    {
        sleep_ms(1);
    }
}


void stop_scan(){
    uart_write_blocking(lidar_uart,stop_scan_bytes,2);
    scan_mode = 0;
    rx_count = 0;
    rx_lim = 0;
    synq_byte_en = true;
    lidar_rx_finished = true;
}

void reset_lidar(){
    uart_write_blocking(lidar_uart,reset_lidar_bytes,2);
    scan_mode = 0;
    rx_count = 0;
    rx_lim = 0;
    synq_byte_en = true;
    lidar_rx_finished = true;
}

void star_normal_scan(){
    uart_write_blocking(lidar_uart,star_normal_scan_bytes,2);
    rx_count = 0;
    rx_lim = 7;
    synq_byte_en = true;
    lidar_rx_finished = false;

    wait_lidar_response(command_time_out);
    
    if(lidar_rx_finished && rx_buffer[2] == 0x05 && rx_buffer[5] == 0x40 && rx_buffer[6] == 0x81){
        scan_mode = scan_mode_normal;
        rx_count = 0;
        rx_lim = 5;
        synq_byte_en = false;
        lidar_rx_finished = false;
    }
}

void star_force_scan(){
    uart_write_blocking(lidar_uart,star_force_scan_bytes,2);

    rx_count = 0;
    rx_lim = 7;
    synq_byte_en = true;
    lidar_rx_finished = false;

    wait_lidar_response(command_time_out);
    
    if(lidar_rx_finished && rx_buffer[2] == 0x05 && rx_buffer[5] == 0x40 && rx_buffer[6] == 0x81){
        scan_mode = scan_mode_normal;
        rx_count = 0;
        rx_lim = normal_stan_len;
        synq_byte_en = false;
        lidar_rx_finished = false;
    }
}

void star_legacy_scan(){
    uart_write_blocking(lidar_uart,star_legacy_scan_bytes,9);

    rx_count = 0;
    rx_lim = 7;
    synq_byte_en = true;
    lidar_rx_finished = false;

    wait_lidar_response(command_time_out);
    
    if(lidar_rx_finished && rx_buffer[2] == 0x54 && rx_buffer[5] == 0x40 && rx_buffer[6] == 0x82){
        scan_mode = scan_mode_legacy;
        rx_count = 0;
        rx_lim = legacy_stan_len;
        synq_byte_en = true;
        lidar_rx_finished = false;
    }
}

void star_extended_scan(){
    uart_write_blocking(lidar_uart,star_extended_scan_bytes,9);
    
    rx_count = 0;
    rx_lim = 7;
    synq_byte_en = true;
    lidar_rx_finished = false;

    wait_lidar_response(command_time_out);
    
    if(lidar_rx_finished && rx_buffer[2] == 0x84 && rx_buffer[5] == 0x40 && rx_buffer[6] == 0x84){
        scan_mode = scan_mode_extended;
        rx_count = 0;
        rx_lim = extended_stan_len;
        synq_byte_en = true;
        lidar_rx_finished = false;
    }
}

void decode_normal_scan(){
    uint16_t angulo_q6 = (uint16_t)(rx_buffer[1]>>1) || (rx_buffer[2]<<7);
    uint16_t distancia_q2 = (uint16_t) rx_buffer[3] || (rx_buffer[4]<<8);
}

void decode_legacy_scan(){

}

void decode_extended_scan(){

}

void send_measure(uint16_t angulo1_q6,uint16_t angulo2_q6,uint16_t distancia_q2){

}


