#include <SPI.h>
#include <stdint.h>

#define debounce_time 20000
#define sample_time 50000

#define intervalo 80

#define SPI0_INTERRUPT_NUMBER (IRQn_Type)24
#define BUFFER_SIZE 512
#define SS 10
uint8_t buff_rx [BUFFER_SIZE];
uint8_t buff_tx [BUFFER_SIZE];
volatile uint32_t pos;
volatile uint32_t d_rx;
volatile uint32_t d_tx;

void SPI0_Handler( void );

//digitales[n][0] = lectura directa
//digitales[n][1] = estado previo
//digitales[n][2] = valor de salida
//-----------------------------------------
//digitales[0][i] = boton analogo izquierdo
//digitales[1][i] = boton analogo derecho
//digitales[2][i] = bonones derecha, A
//digitales[3][i] = bonones derecha, B
//digitales[4][i] = bonones derecha, C
//digitales[5][i] = direccional derecha, boton
//digitales[6][i] = cruz izquierda, arriba
//digitales[7][i] = cruz izquierda, abajo
//digitales[8][i] = cruz izquierda, izquierda
//digitales[9][i] = cruz izquierda, derecha
//digitales[10][i] = direccional derecha, arriba
//digitales[11][i] = direccional derecha, abajo
//digitales[12][i] = direccional derecha, izquierda
//digitales[13][i] = direccional derecha, derecha
bool digitales[14][3];
unsigned long ms_digitales[14];


//boton_simple[0] = "but_analog_izq" / boton analogo izquierdo
//boton_simple[1] = "but_analog_der" / boton analogo derecho
//boton_simple[2] = "but_der_a"      / bonones derecha, A
//boton_simple[3] = "but_der_b"      / bonones derecha, B
//boton_simple[4] = "but_der_c"      / bonones derecha, C
//boton_simple[5] = "but_cruz_der"   / direccional derecha, boton
//---------------------------------
//boton_simple[n][0] = "value" / valor salida
//boton_simple[n][1] = "modo"  / modo 0:normal 1:mantenido 2: circular
//boton_simple[n][2] = "min"   / valor minimo
//boton_simple[n][3] = "max"   / valor maximo
int boton_simple[6][4] = {
  {0, 0, 0, 1},
  {0, 0, 0, 1},
  {0, 0, 0, 1},
  {0, 0, 0, 1},
  {0, 0, 0, 1},
  {0, 0, 0, 1},
};


//boton_flecha[0] = "cruz_izq_h" / cruz izquierda horizontal
//boton_flecha[1] = "cruz_izq_v" / cruz izquierda vertical
//boton_flecha[2] = "cruz_der_h" / cruz derecha horizontal
//boton_flecha[3] = "cruz_der_v" / cruz derecha vertical
//----------------------------------------------
//boton_flecha[n][0] = valor de salida
//boton_flecha[n][1] = modo 0:normal 1:incremental 2:circular
//boton_flecha[n][2] = continuo 0: se incrementa por cada pulsacion 1: se incrementa por cada intervalo
//boton_flecha[n][3] = valor minimo
//boton_flecha[n][4] = valor maximo
//boton_flecha[n][5] = 1/PPS en us
//boton_flecha[n][6] = us ref
//boton_flecha[n][7] = EN
//boton_flecha[n][8] = numero digiral suma
//boton_flecha[n][9] = numero digital resta
int boton_flecha[4][10] = {
  {0, 0, 0, 0, 10, 50000, 0, 1, 6, 7}, //cruz izquierda horizontal
  {0, 0, 0, 0, 10, 50000, 0, 1, 9, 8}, //cruz izquierda vertical
  {0, 0, 0, 0, 10, 50000, 0, 1, 10, 11}, //cruz derecha horizontal
  {0, 0, 0, 0, 10, 50000, 0, 1, 13, 12} //cruz derecha vertical
};

//valor_flecha[0] = cruz izquierda
//valor_flecha[1] = cruz derecha
int valor_flecha[2];


//analogos[n][0] = valor acumulativo
//analogos[n][1] = valor promedio
//-------------------------------
//analogos[0][i] = X izquierda
//analogos[1][i] = Y izquierda
//analogos[2][i] = X derecha
//analogos[3][i] = Y derecha
//analogos[4][i] = panel presicion
//analogos[5][i] = panel
int analogos[6][2];

//numero muestras tomadas en los analogos
int samples_count = 0;

//reloj de referencia para muestreo de analogos
unsigned long ms_analogos;

//analogos_simple[n][0] = valor
//analogos_simple[n][1] = valor minimo
//analogos_simple[n][2] = valor maximo
int analogos_simple[2][3] = {
  {0, 0, 255},
  {0, 0, 255},
};



//"value" de {x_izq ,y_izq, x_der, y_der}
//sticks[0] = valor de salida analogo x derecha
//sticks[1] = valor de salida analogo y derecha
//sticks[2] = valor de salida analogo x izquierda
//sticks[3] = valor de salida analogo y izquierda
int sticks[4];

//sticks_conf[0][i] = "x_izq" / analogo X izquierda
//sticks_conf[1][i] = "y_izq" / analogo Y izquierda
//sticks_conf[2][i] = "x_der" / analogo X derecha
//sticks_conf[3][i] = "y_der" / analogo Y derecha
//-------------------------------
//sticks_conf[n][0] = valor centro en bruto
//sticks_conf[n][1] = "modo" / modo de funcionamiento 0:normal 1:incremental 2:circular
//sticks_conf[n][2] = "centro" / valor centro en salida lineal
//sticks_conf[n][3] = "min" / valor minimo
//sticks_conf[n][4] = "max" / valor valor maximo
//sticks_conf[n][5] = "PPS" / valor pps maximo
//sticks_conf[n][6] = periodo en us de imcrementacion de 1 punto
//sticks_conf[n][7] = us ref
int sticks_conf[4][8] = {
  {2088, 0, 0, -10000, 10000, 20, 0, 0},
  {2060, 0, 127, 0, 254, 20, 0, 0},
  {2186, 0, 127, 0, 254, 20, 0, 0},
  {1932, 0, 127, 0, 254, 20, 0, 0}
};


void SPI0_Handler( void )
{
    d_rx = REG_SPI0_RDR; //registro byte de resivo
    REG_SPI0_TDR = d_tx; //registro byte de envio
    
    // save to buffer
    buff_rx[pos] = d_rx & 0xFF;
    d_tx = buff_tx[pos];
    pos++;
    d_rx = 0;
    
}

void setup() {
  Serial.begin(115200);
  NVIC_ClearPendingIRQ(SPI0_INTERRUPT_NUMBER);
  NVIC_EnableIRQ(SPI0_INTERRUPT_NUMBER);

  SPI.begin(SS);
  REG_SPI0_CR = SPI_CR_SWRST;

  REG_SPI0_IDR = SPI_IDR_TDRE | SPI_IDR_MODF | SPI_IDR_OVRES | SPI_IDR_NSSR | SPI_IDR_TXEMPTY | SPI_IDR_UNDES;
  REG_SPI0_IER = SPI_IER_RDRF;
  REG_SPI0_CR = SPI_CR_SPIEN;     // enable SPI
  REG_SPI0_MR = SPI_MR_MODFDIS;     // slave and no modefault
  REG_SPI0_CSR = SPI_MODE0;    // DLYBCT=0, DLYBS=0, SCBR=0, 8 bit transfer

  pinMode(13,OUTPUT);

  pinMode(35, INPUT_PULLUP); //boton analogo izquierdo
  pinMode(22, INPUT_PULLUP); //boton analogo derecho

  pinMode(38, INPUT_PULLUP); //bonones derecha, A
  pinMode(40, INPUT_PULLUP); //bonones derecha, B
  pinMode(42, INPUT_PULLUP); //bonones derecha, C

  pinMode(30, INPUT_PULLUP); //direccional derecha, boton

  pinMode(37, INPUT_PULLUP); //cruz izquierda, arriba
  pinMode(43, INPUT_PULLUP); //cruz izquierda, abajo
  pinMode(41, INPUT_PULLUP); //cruz izquierda, izquierda
  pinMode(39, INPUT_PULLUP); //cruz izquierda, derecha

  pinMode(32, INPUT_PULLUP); //direccional derecha, arriba
  pinMode(36, INPUT_PULLUP); //direccional derecha, abajo
  pinMode(34, INPUT_PULLUP); //direccional derecha, izquierda
  pinMode(28, INPUT_PULLUP); //direccional derecha, derecha

  for(int i = 0;i<14;i++){
    ms_digitales[i] = micros();
  }
  for(int i = 0;i<4;i++){
    boton_flecha[i][6] = micros();
    sticks_conf[i][7] = micros();
  }
  analogReadResolution(12);

  attachInterrupt(digitalPinToInterrupt(SS), prepare_spi, CHANGE);

}

void loop() {
  digitales[0][0] = !digitalRead(35); //boton analogo izquierdo
  digitales[1][0] = !digitalRead(22); //boton analogo derecho

  digitales[2][0] = !digitalRead(38); //bonones derecha, A
  digitales[3][0] = !digitalRead(40); //bonones derecha, B
  digitales[4][0] = !digitalRead(42); //bonones derecha, C

  digitales[5][0] = !digitalRead(30); //direccional derecha, boton

  digitales[6][0] = !digitalRead(37); //cruz izquierda, arriba
  digitales[7][0] = !digitalRead(43); //cruz izquierda, abajo
  digitales[8][0] = !digitalRead(41); //cruz izquierda, izquierda
  digitales[9][0] = !digitalRead(39); //cruz izquierda, derecha

  digitales[10][0] = !digitalRead(32); //direccional derecha, arriba
  digitales[11][0] = !digitalRead(36); //direccional derecha, abajo
  digitales[12][0] = !digitalRead(34); //direccional derecha, izquierda
  digitales[13][0] = !digitalRead(28); //direccional derecha, derecha

  for (int i = 0; i < 14; i++) {
    if (digitales[i][0] != digitales[i][1]) {
      ms_digitales[i] = micros();
      digitales[i][1] = digitales[i][0];
    }
    else if (digitales[i][0] != digitales[i][2]) {
      if (micros() - ms_digitales[i] >= debounce_time) {
        digitales[i][2] = digitales[i][0];

        if (i <= 5) {
          interpretar_boton_simple(i);
        }
        else if(i == 6 || i == 7){
          //botones flecha con continuo = 0
          interpretar_boton_flecha(0,false);
        }
        else if(i == 8 || i == 9){
          //botones flecha con continuo = 0
          interpretar_boton_flecha(1,false);
        }
        else if(i == 10 || i == 11){
          //botones flecha con continuo = 0
          interpretar_boton_flecha(2,false);
        }
        else if(i == 12 || i == 13){
          //botones flecha con continuo = 0
          interpretar_boton_flecha(3,false);
        }
      }
    }
  }

  interpretar_boton_flecha(0,true);
  interpretar_boton_flecha(1,true);
  interpretar_boton_flecha(2,true);
  interpretar_boton_flecha(3,true);

  samples_count++;
  analogos[0][0] += map(analogRead(A11),0,4095,4095,0); //analogo X izquierda
  analogos[1][0] += analogRead(A10); //analogo Y izquierda

  analogos[2][0] += map(analogRead(A9),0,4095,4095,0); //analogo X derecha
  analogos[3][0] += analogRead(A8); //analogo Y derecha

  analogos[4][0] += analogRead(A7); //analogo panel presicion
  analogos[5][0] += analogRead(A6); //analogo panel

  if (micros() - ms_analogos >= sample_time) {
    ms_analogos = micros();
    for (int i = 0; i < 6; i++) {
      analogos[i][1] = round((float)analogos[i][0] / samples_count);
      analogos[i][0] = 0;
    }
    samples_count = 0;
  }

  interpretar_sticks(0);
  interpretar_sticks(1);
  interpretar_sticks(2);
  interpretar_sticks(3);
}

void interpretar_boton_flecha(int i, bool continuo) {
  if (continuo == boton_flecha[i][2]) {
    bool d1 = digitales[boton_flecha[i][8]][2];
    bool d2 = digitales[boton_flecha[i][9]][2];
    if (d1 != d2) {
      switch (boton_flecha[i][1])
      {
        case 0: //modo normal
          /* code */
          if (d1) {
            boton_flecha[i][0] = 1;
          }
          else {
            boton_flecha[i][0] = -1;
          }
          break;

        case 1: //modo incremental
          if (continuo) {
            if (micros() - boton_flecha[i][6] >= boton_flecha[i][5]) {
              boton_flecha[i][6] = micros();
              if (d1) {
                boton_flecha[i][0] = constrain(boton_flecha[i][0] + 1, boton_flecha[i][3], boton_flecha[i][4]);
              }
              else {
                boton_flecha[i][0] = constrain(boton_flecha[i][0] - 1, boton_flecha[i][3], boton_flecha[i][4]);
              }
            }
          }
          else {
            if (d1) {
              boton_flecha[i][0] = constrain(boton_flecha[i][0] + 1, boton_flecha[i][3], boton_flecha[i][4]);
            }
            else {
              boton_flecha[i][0] = constrain(boton_flecha[i][0] - 1, boton_flecha[i][3], boton_flecha[i][4]);
            }
          }
          break;

        case 2: //modo circular
          if (continuo) {
            if (micros() - boton_flecha[i][6] >= boton_flecha[i][5]) {
              boton_flecha[i][6] = micros();
              if (d1) {
                boton_flecha[i][0] = constrain_circular(boton_flecha[i][0] + 1, boton_flecha[i][3], boton_flecha[i][4]);
              }
              else {
                boton_flecha[i][0] = constrain_circular(boton_flecha[i][0] - 1, boton_flecha[i][3], boton_flecha[i][4]);
              }
            }
          }
          else {
            if (d1) {
              boton_flecha[i][0] = constrain_circular(boton_flecha[i][0] + 1, boton_flecha[i][3], boton_flecha[i][4]);
            }
            else {
              boton_flecha[i][0] = constrain_circular(boton_flecha[i][0] - 1, boton_flecha[i][3], boton_flecha[i][4]);
            }
          }
          break;

        default:
          break;
      }
    }
    else if (boton_flecha[i][1] == 0) {
      boton_flecha[i][0] = 0;
    }
  }
}

void interpretar_boton_simple(int i) {
  switch (boton_simple[i][1])
  {
    case 0:
      if (digitales[i][2]) {
        boton_simple[i][0] = boton_simple[i][3];
      }
      else {
        boton_simple[i][0] = boton_simple[i][2];
      }
      break;

    case 1:
      if (digitales[i][2]) {
        if (boton_simple[i][0] == boton_simple[i][3]) {
          boton_simple[i][0] = boton_simple[i][2];
        }
        else {
          boton_simple[i][0] = boton_simple[i][3];
        }
      }
      break;

    case 2:
      if (digitales[i][2]) {
        boton_simple[i][0] = constrain_circular(boton_simple[i][0] + 1, boton_simple[i][2], boton_simple[i][3]);
      }
      break;

    default:
      boton_simple[i][0] = 0;
      boton_simple[i][1] = 0;
      boton_simple[i][2] = 0;
      boton_simple[i][3] = 1;
      break;
  }
}

int proporcion_stick(int i, int minimo, int maximo, int centro) {
  if (analogos[i][1] > sticks_conf[i][0] - intervalo && analogos[i][1] < sticks_conf[i][0] + intervalo) {
    return (centro);
  }
  else {
    if (analogos[i][1] >= sticks_conf[i][0] + intervalo) {
      return (map(analogos[i][1], sticks_conf[i][0] + intervalo, 4095, centro + 1, maximo));
    }
    else {
      return (map(analogos[i][1], 0, sticks_conf[i][0] - intervalo, minimo, centro - 1));
    }
  }
}

int constrain_circular(int valor, int minimo, int maximo) {
  if (valor > maximo) {
    return (minimo);
  }
  else if (valor < minimo) {
    return (maximo);
  }
  else {
    return (valor);
  }
}

void interpretar_sticks(int i) {
  int pps; 
  switch (sticks_conf[i][1]) {

    case 0: //modo lineal
      sticks[i] = proporcion_stick(i, sticks_conf[i][3], sticks_conf[i][4], sticks_conf[i][2]);
      break;


    case 1: //modo incremental
      pps = proporcion_stick(i, sticks_conf[i][5] * (-1), sticks_conf[i][5], 0);
      if (abs(pps) > 0) {
        sticks_conf[i][6] = 1000000 / abs(pps);

        if (micros() - sticks_conf[i][7] >= sticks_conf[i][6]) {
          sticks_conf[i][7] = micros();
          
          if (pps > 0) {
            sticks[i] = constrain(sticks[i] + 1, sticks_conf[i][3], sticks_conf[i][4]);
          }
          else {
            sticks[i] = constrain(sticks[i] - 1, sticks_conf[i][3], sticks_conf[i][4]);
          }
        }
      }

      break;


    case 2: //modo circular
      pps = proporcion_stick(i, sticks_conf[i][5] * (-1), sticks_conf[i][5], 0);
      if (abs(pps) > 0) {
        sticks_conf[i][6] = 1000000 / abs(pps);

        if (micros() - sticks_conf[i][7] >= sticks_conf[i][6]) {
          sticks_conf[i][7] = micros();

          if (pps > 0) {
            sticks[i] = constrain_circular(sticks[i] + 1, sticks_conf[i][3], sticks_conf[i][4]);
          }
          else {
            sticks[i] = constrain_circular(sticks[i] - 1, sticks_conf[i][3], sticks_conf[i][4]);
          }
        }
      }
      break;


    default:
      sticks[i] = 127;
      sticks_conf[i][1] = 0; //modo
      sticks_conf[i][2] = 127; //valor centro
      sticks_conf[i][3] = 0; //valor minimo
      sticks_conf[i][4] = 254; //valor maximo
      sticks_conf[i][5] = 0; //valor PPS maximo
      sticks_conf[i][6] = 0; //periodo PPS en us
      sticks_conf[i][7] = 0; //us ref
      break;
  }
}

int flecha_valor(bool arriba, bool abajo, bool izquierda, bool derecha) {
  int val = arriba * 8 + abajo * 4 + izquierda * 2 + derecha;
  switch (val) {
    case 1:
      return (3);
      break;

    case 2:
      return (7);
      break;

    case 4:
      return (5);
      break;

    case 5:
      return (4);
      break;

    case 6:
      return (6);
      break;

    case 8:
      return (1);
      break;

    case 9:
      return (2);
      break;

    case 10:
      return (8);
      break;

    default:
      return (0);
      break;
  }
}


void val_to_buff_tx(int i,long val){
  byte * byte_val = (byte*)&val;
  buff_tx[i]   = byte_val[3];
  buff_tx[i+1] = byte_val[2];
  buff_tx[i+2] = byte_val[1];
  buff_tx[i+3] = byte_val[0];
}

long buff_rx_to_val(int i){
  byte val[4];
  val[3] = buff_rx[i+3];
  val[2] = buff_rx[i+2];
  val[1] = buff_rx[i+1];
  val[0] = buff_rx[i];
  return *((long *)val);
}

void write_values() {

  valor_flecha[0] = flecha_valor(digitales[6][2], digitales[7][2], digitales[8][2], digitales[9][2]);
  valor_flecha[1] = flecha_valor(digitales[10][2], digitales[11][2], digitales[12][2], digitales[13][2]);

  analogos_simple[0][0] = map(analogos[4][1], 0, 4095, analogos_simple[0][1], analogos_simple[0][2]);
  analogos_simple[1][0] = map(analogos[5][1], 0, 4095, analogos_simple[1][1], analogos_simple[1][2]);

  val_to_buff_tx(0,sticks[0]);
  val_to_buff_tx(4,sticks[1]);
  val_to_buff_tx(8,sticks[2]);
  val_to_buff_tx(12,sticks[3]);

  val_to_buff_tx(16,boton_flecha[0][0]);
  val_to_buff_tx(20,boton_flecha[1][0]);
  val_to_buff_tx(24,boton_flecha[2][0]);
  val_to_buff_tx(28,boton_flecha[3][0]);
  val_to_buff_tx(32,boton_simple[0][0]);
  val_to_buff_tx(36,boton_simple[1][0]);
  val_to_buff_tx(40,boton_simple[2][0]);
  val_to_buff_tx(44,boton_simple[3][0]);
  val_to_buff_tx(48,boton_simple[4][0]);
  val_to_buff_tx(52,boton_simple[5][0]);

  val_to_buff_tx(56,valor_flecha[0]);
  val_to_buff_tx(60,valor_flecha[1]);

  val_to_buff_tx(64,analogos_simple[0][0]);
  val_to_buff_tx(68,analogos_simple[1][0]);
}

void read_values(){
  sticks[0]=buff_rx_to_val(0);
  sticks_conf[0][1]=buff_rx_to_val(4);
  sticks_conf[0][3]=buff_rx_to_val(8);
  sticks_conf[0][4]=buff_rx_to_val(12);
  sticks_conf[0][5]=buff_rx_to_val(16);
  sticks_conf[0][2]=buff_rx_to_val(20);

  sticks[1]=buff_rx_to_val(24);
  sticks_conf[1][1]=buff_rx_to_val(28);
  sticks_conf[1][3]=buff_rx_to_val(32);
  sticks_conf[1][4]=buff_rx_to_val(36);
  sticks_conf[1][5]=buff_rx_to_val(40);
  sticks_conf[1][2]=buff_rx_to_val(44);

  sticks[2]=buff_rx_to_val(48);
  sticks_conf[2][1]=buff_rx_to_val(52);
  sticks_conf[2][3]=buff_rx_to_val(56);
  sticks_conf[2][4]=buff_rx_to_val(60);
  sticks_conf[2][5]=buff_rx_to_val(64);
  sticks_conf[2][2]=buff_rx_to_val(68);

  sticks[3]=buff_rx_to_val(72);
  sticks_conf[3][1]=buff_rx_to_val(76);
  sticks_conf[3][3]=buff_rx_to_val(80);
  sticks_conf[3][4]=buff_rx_to_val(84);
  sticks_conf[3][5]=buff_rx_to_val(88);
  sticks_conf[3][2]=buff_rx_to_val(92);

  boton_flecha[0][0]=buff_rx_to_val(96);
  boton_flecha[0][1]=buff_rx_to_val(100);
  boton_flecha[0][2]=buff_rx_to_val(104);
  boton_flecha[0][3]=buff_rx_to_val(108);
  boton_flecha[0][4]=buff_rx_to_val(112);
  boton_flecha[0][5]=buff_rx_to_val(116);

  boton_flecha[1][0]=buff_rx_to_val(120);
  boton_flecha[1][1]=buff_rx_to_val(124);
  boton_flecha[1][2]=buff_rx_to_val(128);
  boton_flecha[1][3]=buff_rx_to_val(132);
  boton_flecha[1][4]=buff_rx_to_val(136);
  boton_flecha[1][5]=buff_rx_to_val(140);

  boton_flecha[2][0]=buff_rx_to_val(144);
  boton_flecha[2][1]=buff_rx_to_val(148);
  boton_flecha[2][2]=buff_rx_to_val(152);
  boton_flecha[2][3]=buff_rx_to_val(156);
  boton_flecha[2][4]=buff_rx_to_val(160);
  boton_flecha[2][5]=buff_rx_to_val(164);

  boton_flecha[3][0]=buff_rx_to_val(168);
  boton_flecha[3][1]=buff_rx_to_val(172);
  boton_flecha[3][2]=buff_rx_to_val(176);
  boton_flecha[3][3]=buff_rx_to_val(180);
  boton_flecha[3][4]=buff_rx_to_val(184);
  boton_flecha[3][5]=buff_rx_to_val(188);

  boton_simple[0][0]=buff_rx_to_val(192);
  boton_simple[0][1]=buff_rx_to_val(196);
  boton_simple[0][2]=buff_rx_to_val(200);
  boton_simple[0][3]=buff_rx_to_val(204);

  boton_simple[1][0]=buff_rx_to_val(208);
  boton_simple[1][1]=buff_rx_to_val(212);
  boton_simple[1][2]=buff_rx_to_val(216);
  boton_simple[1][3]=buff_rx_to_val(220);

  boton_simple[2][0]=buff_rx_to_val(224);
  boton_simple[2][1]=buff_rx_to_val(228);
  boton_simple[2][2]=buff_rx_to_val(232);
  boton_simple[2][3]=buff_rx_to_val(236);

  boton_simple[3][0]=buff_rx_to_val(240);
  boton_simple[3][1]=buff_rx_to_val(244);
  boton_simple[3][2]=buff_rx_to_val(248);
  boton_simple[3][3]=buff_rx_to_val(252);

  boton_simple[4][0]=buff_rx_to_val(256);
  boton_simple[4][1]=buff_rx_to_val(260);
  boton_simple[4][2]=buff_rx_to_val(264);
  boton_simple[4][3]=buff_rx_to_val(268);

  boton_simple[5][0]=buff_rx_to_val(272);
  boton_simple[5][1]=buff_rx_to_val(276);
  boton_simple[5][2]=buff_rx_to_val(280);
  boton_simple[5][3]=buff_rx_to_val(284);

  analogos_simple[0][1]=buff_rx_to_val(288);
  analogos_simple[0][2]=buff_rx_to_val(292);
  analogos_simple[1][1]=buff_rx_to_val(296);
  analogos_simple[1][2]=buff_rx_to_val(300);
}

void prepare_spi(){
  if(digitalRead(SS)){
    if(pos >= 303){
      read_values();
    }

    Serial.println("----");
    Serial.println(buff_rx_to_val(0));
    Serial.println(buff_rx_to_val(4));

    for(int i = 0; i<10;i++){
      Serial.print(buff_rx[i],HEX);
      Serial.print("-");
    }
    Serial.println("----");

    for(int i = 0;i<BUFFER_SIZE;i++){
      buff_rx[i] = 0;
      buff_tx[i] = 0;
    }
  }
  else{
    write_values();
    pos = 0;
    d_tx = 127;
    REG_SPI0_TDR = 200;
  }
}