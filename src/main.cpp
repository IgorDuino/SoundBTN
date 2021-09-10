// pc
#include <Arduino.h>
#include "GyverMotor.h"
#include <microLED.h>

#define LED_PIN 12

#define HOLL_1_1_PIN 38
#define HOLL_1_2_PIN 39
#define HOLL_2_1_PIN 40
#define HOLL_2_2_PIN 41
#define HOLL_3_1_PIN 42
#define HOLL_3_2_PIN 43
#define HOLL_4_1_PIN 44
#define HOLL_4_2_PIN 45

#define HOLL_LEFT_1_PIN 24
#define HOLL_LEFT_2_PIN 25
#define HOLL_RIGHT_1_PIN 26
#define HOLL_RIGHT_2_PIN 27

#define LEFT_RIGHT_POT_PIN A0
#define BATTERY_PIN A3

String strData = "";
boolean recievedFlag;

long int timer_led;
long int timer_check_battery;

bool rainbow = 0;

int r = 255; // Красный горит
int b = 0;   // Синий потушен
int g = 0;   // Зелёный потушен

int holl_1_1, holl_1_2, holl_2_1, holl_2_2, holl_3_1, holl_3_2, holl_4_1, holl_4_2;
int holl_left_1, holl_left_2, holl_right_1, holl_right_2;
int battery_val;

char floatbufVar_body_x[32];
char floatbufVar_body_y[32];
char floatbufVar_head_x[32];
char floatbufVar_head_y[32];
char floatbufVar_r[32];
char floatbufVar_g[32];
char floatbufVar_b[32];

float body_x, body_y, head_x, head_y;

GMotor motorL(DRIVER3WIRE, 2, 3, 4, LOW);
GMotor motorR(DRIVER3WIRE, 5, 6, 7, HIGH);

GMotor motorHead1(DRIVER3WIRE, 30, 31, 8, HIGH);
GMotor motorHead2(DRIVER3WIRE, 32, 33, 9, HIGH);
GMotor motorHead3(DRIVER3WIRE, 34, 35, 10, HIGH);
GMotor motorHead4(DRIVER3WIRE, 36, 37, 11, HIGH);

microLED<1, LED_PIN, MLED_NO_CLOCK, LED_WS2818, ORDER_GRB, CLI_AVER> led;

void set_led(int rq, int gq, int bq)
{
  led.set(0, mRGB(rq, gq, bq));
  led.show();
}

void ledManager()
{
  static unsigned long timestamp = millis();
  static int e = 1;

  if (millis() - timestamp > 5)
  {
    timestamp = millis();

    if (e <= 255)
    {
      r++;
      b--;
    }
    if (e > 255 && e <= 510)
    {
      b++;
      g--;
    }
    if (e > 510)
    {
      g++;
      r--;
    }

    set_led(r, g, b);

    e++;
    if (e > 765)
      e = 1;
  } // конец бывшего цикла for
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++)
  {
    if (data.charAt(i) == separator || i == maxIndex)
    {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }

  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void head_left_right(int val)
{
  if (val == 0)
  {
    motorHead1.setMode(STOP);
    motorHead3.setMode(STOP);
  }
  else
  {
    motorHead1.setMode(AUTO);
    motorHead3.setMode(AUTO);

    motorHead1.setSpeed(val / 2);
    motorHead3.setSpeed(val / -2);
  }
}

void head_up_down(int val)
{
  if (val == 0)
  {
    motorHead2.setMode(STOP);
  }
  else
  {
    motorHead2.setMode(AUTO);
    motorHead2.setSpeed(val / -2);
  }
}

void head_forward_back(int val)
{
  if (val == 0)
  {
    motorHead1.setMode(STOP);
    motorHead4.setMode(STOP);
  }
  else
  {
    motorHead1.setMode(AUTO);
    motorHead4.setMode(AUTO);

    motorHead1.setSpeed(val / 2);
    motorHead4.setSpeed(val / -2);
  }
}

void setup()
{
  Serial.begin(9600);

  pinMode(HOLL_1_1_PIN, INPUT);
  pinMode(HOLL_1_2_PIN, INPUT);
  pinMode(HOLL_2_1_PIN, INPUT);
  pinMode(HOLL_2_2_PIN, INPUT);
  pinMode(HOLL_3_1_PIN, INPUT);
  pinMode(HOLL_3_2_PIN, INPUT);
  pinMode(HOLL_4_1_PIN, INPUT);
  pinMode(HOLL_4_2_PIN, INPUT);

  pinMode(HOLL_RIGHT_1_PIN, INPUT);
  pinMode(HOLL_RIGHT_1_PIN, INPUT);
  pinMode(HOLL_LEFT_1_PIN, INPUT);
  pinMode(HOLL_LEFT_2_PIN, INPUT);

  pinMode(BATTERY_PIN, INPUT);
  pinMode(LEFT_RIGHT_POT_PIN, INPUT);

  led.setBrightness(255);

  motorL.setMode(AUTO);
  motorR.setMode(AUTO);

  motorHead1.setMode(AUTO);
  motorHead2.setMode(AUTO);
  motorHead3.setMode(AUTO);
  motorHead4.setMode(AUTO);

  motorL.setMinDuty(21);
  motorR.setMinDuty(21);

  Serial.println("Ready");

  set_led(255, 0, 0);
}

void loop()
{
  if (rainbow)
  {
    ledManager();
  }

  if (millis() - timer_check_battery >= 4000)
  {
    battery_val = analogRead(BATTERY_PIN);
    battery_val = map(battery_val, 0, 1023, 0, 100);

    Serial.print("Bat: ");
    Serial.println(battery_val);
    
    timer_check_battery = millis();
  }

  holl_1_1 = digitalRead(HOLL_1_1_PIN);
  holl_1_2 = digitalRead(HOLL_1_2_PIN);
  holl_2_1 = digitalRead(HOLL_2_1_PIN);
  holl_2_2 = digitalRead(HOLL_2_2_PIN);
  holl_3_1 = digitalRead(HOLL_3_1_PIN);
  holl_3_2 = digitalRead(HOLL_3_2_PIN);
  holl_4_1 = digitalRead(HOLL_4_1_PIN);
  holl_4_2 = digitalRead(HOLL_4_2_PIN);

  holl_left_1 = digitalRead(HOLL_LEFT_1_PIN);
  holl_left_2 = digitalRead(HOLL_LEFT_2_PIN);

  holl_right_1 = digitalRead(HOLL_RIGHT_1_PIN);
  holl_right_2 = digitalRead(HOLL_RIGHT_2_PIN);

  while (Serial.available() > 0)
  {
    strData += (char)Serial.read();
    recievedFlag = true;
    delay(2);
  }
  if (recievedFlag)
  {
    if (strData != "")
    {
      String state = getValue(strData, ';', 0);
      if (state == "m" || state == "mh")
      {
        String body_x_str = getValue(strData, ';', 1);
        String body_y_str = getValue(strData, ';', 2);

        String head_x_str = getValue(strData, ';', 3);
        String head_y_str = getValue(strData, ';', 4);

        body_x_str.toCharArray(floatbufVar_body_x, sizeof(floatbufVar_body_x));
        body_x = atof(floatbufVar_body_x);

        body_y_str.toCharArray(floatbufVar_body_y, sizeof(floatbufVar_body_y));
        body_y = atof(floatbufVar_body_y);

        body_y = body_y * 100;
        body_x = body_x * -100;

        body_x = map(body_x, -100, 100, -255, 255);
        body_y = map(body_y, -100, 100, -255, 255);

        int dutyL = body_y - body_x;
        int dutyR = body_y + body_x;

        motorL.setSpeed(dutyL * 0.35);
        motorR.setSpeed(dutyR * 0.35 * 0.6648);

        head_x_str.toCharArray(floatbufVar_head_x, sizeof(floatbufVar_head_x));
        head_x = atof(floatbufVar_head_x);

        head_y_str.toCharArray(floatbufVar_head_y, sizeof(floatbufVar_head_y));
        head_y = atof(floatbufVar_head_y);

        head_y = head_y * 100;
        head_x = head_x * -100;

        head_x = map(head_x, -100, 100, -255, 255);
        head_y = map(head_y, -100, 100, -255, 255);

        head_left_right(head_x);

        Serial.print("HOLL: ");
        Serial.print(holl_1_1);
        Serial.print(" ");
        Serial.print(holl_1_1);
        Serial.print(" ");
        Serial.print(holl_2_1);
        Serial.print(" ");
        Serial.print(holl_2_2);
        Serial.print(" ");
        Serial.print(holl_3_1);
        Serial.print(" ");
        Serial.print(holl_3_2);
        Serial.print(" ");
        Serial.print(holl_4_1);
        Serial.print(" ");
        Serial.print(holl_4_2);
        Serial.print(" ");
      }

      else if (state == "l")
      {
        String ledr = getValue(strData, ';', 1);
        String ledg = getValue(strData, ';', 2);
        String ledb = getValue(strData, ';', 3);

        ledr.toCharArray(floatbufVar_r, sizeof(floatbufVar_r));
        ledg.toCharArray(floatbufVar_g, sizeof(floatbufVar_g));
        ledb.toCharArray(floatbufVar_b, sizeof(floatbufVar_b));

        int ledRint = atof(floatbufVar_r);
        int ledGint = atof(floatbufVar_g);
        int ledBint = atof(floatbufVar_b);

        set_led(ledRint, ledGint, ledBint);
      }
      if (state == "m")
      {
        head_up_down(head_y);
      }
      if (state == "mh")
      {
        head_forward_back(head_y);
      }
    }
    strData = "";
    recievedFlag = false;
  }
}
a