#include <Wire.h>
#include <Servo.h>

#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/uart.h"

#include <Adafruit_PWMServoDriver.h>
#include <RPlidar.h>
#include <protocolo_serial.h>

//"C:\\Users\\Eziron\\AppData\\Local\\Arduino15\\packages\\rp2040\\hardware\\rp2040\\1.13.1\\pico-sdk\\src",

//puerto entre la jetson nano y la RPI
#define BAUD_RATE0 1500000
#define UART0_TX_PIN 12
#define UART0_RX_PIN 13

//puerto entre la RPI y el lidar
#define BAUD_RATE1 115200
#define UART1_TX_PIN 8
#define UART1_RX_PIN 9
#define LIDAR_PIN 10
#define LIDAR_SV_PIN 11

#define WIRE1_SDA_PIN 2
#define WIRE1_SCL_PIN 3
#define WIRE1_SDA_CLK 1400000

#define PWM_FREQ 333
#define SV16_PIN 22
#define SV17_PIN 21

#define led_pin 25

PCA9685 pwm = PCA9685(127,Wire1);

ProtocoloSerial jetson; //Serial1 = UART0
RPlidar lidar;       //Serial2 = UART1

Servo lidar_servo;
Servo sv16;
Servo sv17;

uint16_t servo_us = 500;
bool servo_dir = false;
uint32_t servo_time = 0;
uint32_t servo_time_ref = 2500;

uint16_t lidar_angulo1_q6 = 0;
uint16_t lidar_angulo2_q6 = 0;
uint16_t lidar_distancia_q2 = 0;
uint32_t lidar_sample_time = 0;
bool star_scan = false;
uint16_t lidar_tx_buffer[5];

uint16_t analog_val = 0;
uint32_t analog_time_ref = 0; 
uint16_t sample_pot_q6[8000];
uint32_t sample_time_pot[8000];
uint16_t n_write_pot = 0;
uint16_t n_read_pot = 0;

uint8_t jetson_buffer[2048];
uint8_t jetson_cmd;
uint8_t jetson_d_tyte;
uint8_t jetson_d_len;
uint8_t accept_command[] = {5,5};
uint8_t not_accept_command[] = {0,0};
struct repeating_timer timer_pot;

uint16_t duty[] = {869, 1560, 1027, 719, 1580, 1215, 939, 1540, 1570, 2031, 1785, 1500, 2131, 1983, 1500, 2061, 1075, 1855};
uint16_t duty_pca[16];
bool duty_accept = true;

void setup(){
    Serial.begin(2000000);
    uart_init(uart0, BAUD_RATE0);
    gpio_set_function(13, GPIO_FUNC_UART);
    gpio_set_function(12, GPIO_FUNC_UART);
    Serial1.begin(BAUD_RATE0);

    uart_init(uart1, BAUD_RATE1);
    gpio_set_function(UART1_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART1_RX_PIN, GPIO_FUNC_UART);
    lidar.begin(LIDAR_PIN,BAUD_RATE1);

    Wire1.setSDA(WIRE1_SDA_PIN);
    Wire1.setSCL(WIRE1_SCL_PIN);
    Wire1.setClock(WIRE1_SDA_CLK);

    pwm.begin(PWM_FREQ,24943000);
    sv16.attach(SV16_PIN);
    sv17.attach(SV17_PIN);

    pinMode(led_pin,OUTPUT);
    analogReadResolution(12);
    lidar_servo.attach(LIDAR_SV_PIN,500,2500);
    lidar_servo.write(90);
}

void loop(){
    if(jetson.read_command(jetson_buffer, &jetson_cmd, &jetson_d_len, &jetson_d_tyte)){
        digitalWrite(led_pin,1);
        switch (jetson_cmd){
        case 0: //PING
            if(jetson_d_tyte == 'B'){
                for(int i = 0; i<jetson_d_len;i++){
                    jetson_buffer[i]++;
                }
            }
            jetson.send_command(jetson_cmd,jetson_d_len,jetson_buffer);
            break;

        case 1: //escritura de los Servos
            if(jetson_d_tyte == 'H' && jetson_d_len == 18){
                jetson.decode_uint16(jetson_buffer,jetson_d_len,duty);
                duty_accept = true;
                for(int i = 0;i<18;i++){
                    if(duty[i] >= 500 && duty[i] <= 2500){
                        if(i < 16){
                            duty_pca[i] = duty[i];
                        }
                    }
                    else{
                        duty_accept = false;
                    }
                }
                confirm(jetson_cmd,duty_accept);
                if(duty_accept){
                    pwm.writeAllMicroseconds(duty_pca);
                    sv16.writeMicroseconds(duty[16]);
                    sv17.writeMicroseconds(duty[17]);
                }
            }
            break;

        case 2: //lectura de los Servos
            jetson.send_command(2,18,duty);
            break;

        case 3: //LIDAR
            if(jetson_d_tyte == 'B' && jetson_d_len == 3){
                uint8_t lidar_speed = map(jetson_buffer[1],0,255,100,255);
                if(star_scan){
                    if(jetson_buffer[0] == 0){
                        lidar.stop_scan();
                        lidar_servo.write(90);
                        star_scan = false;
                    }
                    else{
                        lidar.set_motor_speed(lidar_speed);
                    }
                }
                else{
                    switch (jetson_buffer[0])
                    {
                    case 1:
                        star_scan = lidar.star_normal_scan(lidar_speed);
                        break;
                    
                    case 2:
                        star_scan = lidar.star_legacy_scan(lidar_speed);
                        break;

                    case 3:
                        star_scan = lidar.star_extended_scan(lidar_speed);
                        break;
                    
                    case 255:
                        star_scan = lidar.star_force_scan(lidar_speed);
                        break;
                    
                    default:
                        break;
                    }
                }

                servo_time_ref = map(jetson_buffer[2],0,255,8000,1600);
                confirm(jetson_cmd,star_scan);
                enable_timer_pot(star_scan);
            }
            break;

        default:
            break;
        }
        digitalWrite(led_pin,0);
    }
    if(star_scan){
        if(uart_is_writable(uart0)){
            if(lidar.get_sample(&lidar_angulo1_q6,&lidar_distancia_q2, &lidar_sample_time)){
                digitalWrite(led_pin,1);
                buscar_por_tiempo(lidar_sample_time);
                lidar_tx_buffer[0] = lidar_distancia_q2;
                lidar_tx_buffer[1] = lidar_angulo1_q6;
                lidar_tx_buffer[2] = lidar_angulo2_q6;
                lidar_tx_buffer[3] = lidar_sample_time>>16;
                lidar_tx_buffer[4] = lidar_sample_time;
                jetson.send_command(127,5,lidar_tx_buffer);
                digitalWrite(led_pin,0);
            }
        }
    }
}

void setup1(){
    delay(3000);
}

void loop1(){
    if(star_scan){
        lidar.read_lidar_scan();
        control_servo();
    }
}
