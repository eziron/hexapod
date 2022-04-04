void confirm(uint8_t CMD,bool accept){
  if(accept){
    jetson.send_command(CMD,2,accept_command);
  }
  else{
    jetson.send_command(CMD,2,not_accept_command);
  }
}

void enable_timer_pot(bool state){
  if(state){
    n_write_pot = 0;
    n_read_pot = 0;
    add_repeating_timer_us(60, leer_pot, NULL, &timer_pot);
  }
  else{
    cancel_repeating_timer(&timer_pot);
  }
}

void control_servo() {
  if (micros() - servo_time >= servo_time_ref) {
    servo_time = micros();

    if (servo_us >= 2500 || servo_us <= 500) {
      servo_dir = !servo_dir;
    }

    if (servo_dir) {
      servo_us++;
    }
    else {
      servo_us--;
    }

    lidar_servo.writeMicroseconds(servo_us);
  }
}

bool leer_pot(struct repeating_timer *t){
  if(star_scan){
    analog_time_ref = micros();
    analog_val = round(map(analogRead(A0),0,4096,0,17280));
    sample_pot_q6[n_write_pot] = analog_val;
    sample_time_pot[n_write_pot] = analog_time_ref;

    n_write_pot = constrain_circ(n_write_pot+1,0,8000);
    if(n_write_pot == n_read_pot){
      n_read_pot = constrain_circ(n_read_pot+1,0,8000);
    }

    return true;
  }
  return false;
}

bool buscar_por_tiempo(uint32_t time_ref){
  if(calc_cola_dist(n_write_pot,n_read_pot,8000) > 0){
    if(sample_time_pot[n_read_pot] == time_ref){
      lidar_angulo2_q6 = sample_pot_q6[n_read_pot];
      return true;
    }
    else{
      if(sample_time_pot[n_read_pot] < time_ref){
        while (sample_time_pot[n_read_pot] < time_ref){
          if(calc_cola_dist(n_write_pot,n_read_pot,8000) == 0){
            return false;
          }
          n_read_pot = constrain_circ(n_read_pot+1,0,8000);
        }
        n_read_pot = constrain_circ(n_read_pot-1,0,8000);

        lidar_angulo2_q6 = sample_pot_q6[n_read_pot];
        return true;
      }
      else{
        return false;
      }
    }
  }
  else{
    return false;
  }
}

uint16_t constrain_circ(uint16_t val, uint16_t min_val, uint16_t max_val){
    if(val >= max_val){
        return min_val;
    }
    else if (val <= min_val){
        return max_val-1;
    }
    else{
        return val;
    }
}

uint16_t calc_cola_dist(uint16_t n_write,uint16_t n_read,uint16_t n_max){
    if(n_write == n_read){
        return 0;
    }
    else{
        if(n_write > n_read){
            return n_write-n_read;
        }
        //n_read > n_write
        else{
            return n_max-n_read+n_write;
        }
    }
}