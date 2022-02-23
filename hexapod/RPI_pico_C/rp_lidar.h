#include "hardware/uart.h"

#define lidar_synq_byte1 0xA
#define lidar_synq_byte2 0x5
#define command_time_out 2000000
#define scan_time_out 500000

#define scan_mode_normal 1
#define scan_mode_legacy 2
#define scan_mode_extended 3


#define normal_stan_len 5
#define legacy_stan_len 84
#define extended_stan_len 132

#define lidar_uart uart0
#define lidar_out_uart uart1

bool lidar_rx_finished = true;

void lidar_core1_entry();
void lidar_on_uart_rx();
void wait_lidar_response(uint64_t time_out);
void stop_scan();
void reset_lidar();
void star_normal_scan();
void star_force_scan();
void star_legacy_scan();
void star_extended_scan();
void decode_normal_scan();
void decode_legacy_scan();
void decode_extended_scan();
void send_measure(uint16_t angulo1_q6,uint16_t angulo2_q6,uint16_t distancia_q2);