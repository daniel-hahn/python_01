#include <Wire.h>
#include <Adafruit_SHT31.h>
#include <SPI.h>
#include <SdFat.h>
#include <DS1302.h>
#include <driver/rtc_io.h>
#include <esp_sleep.h>
#include "esp_wifi.h"
#include "esp_bt.h"

// ==== Pin Definitions ====
#define DS1302_CLK        25
#define DS1302_DAT        26
#define DS1302_RST        27
#define SD_CS             5
#define LED_PIN           15
#define SHT31_POWER_PIN   14

// ==== Komponenten ====
DS1302 rtc(DS1302_RST, DS1302_DAT, DS1302_CLK);
Adafruit_SHT31 sht31 = Adafruit_SHT31();
SdFat sd;

// ==== WLAN & Bluetooth deaktivieren ====
void disableRadioModules() {
  esp_bt_controller_disable();
  esp_wifi_stop();
}

// ==== Blinkfunktionen ====
void blinkError(int times, int delayMs = 200) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH); delay(delayMs);
    digitalWrite(LED_PIN, LOW);  delay(delayMs);
  }
}

void blinkSuccess() {
  digitalWrite(LED_PIN, HIGH); delay(500);
  digitalWrite(LED_PIN, LOW);
}

// ==== RTC-Zeit aus Compile-Zeit setzen (einmalig aufrufen) ====
void setRTCFromCompileTime() {
  const char* months[] = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  };

  char mStr[4];
  int day, year, hour, minute, second, month = 0;

  sscanf(__DATE__, "%s %d %d", mStr, &day, &year);
  sscanf(__TIME__, "%d:%d:%d", &hour, &minute, &second);

  for (int i = 0; i < 12; i++) {
    if (strncmp(mStr, months[i], 3) == 0) {
      month = i + 1;
      break;
    }
  }

  rtc.setDOW(1);
  rtc.setTime(hour, minute, second);
  rtc.setDate(day, month, year);
}

// ==== Setup ====
void setup() {
  Serial.begin(115200);
  delay(50);
  //Serial.println("📡 Starte Sensor-Logger...");

  disableRadioModules();  // ✅ WLAN + Bluetooth deaktivieren

  //pinMode(LED_PIN, OUTPUT);
  //digitalWrite(LED_PIN, LOW);

  rtc.halt(false);
  rtc.writeProtect(false);

  // === Optional: RTC setzen (nur 1x aktivieren) ===

  
  //setRTCFromCompileTime();
  

  //pinMode(SHT31_POWER_PIN, OUTPUT);
  //digitalWrite(SHT31_POWER_PIN, HIGH);
  delay(4000);//delay(50);

  //bool sensorOK = sht31.begin(0x44);
  bool sensorOK = false;
  for (int i = 0; i < 5; i++) {
    sensorOK = sht31.begin(0x44);
    if (sensorOK) break;
    delay(200);
  }

  if (!sensorOK) {
    Serial.println("❌ SHT31 nicht gefunden!");
    blinkError(3);
  }

  bool sdOK = sd.begin(SD_CS, SD_SCK_MHZ(4));
  if (!sdOK) {
    Serial.println("❌ SD-Karte nicht erkannt!");
    blinkError(5);
  }

  Time now = rtc.getTime();
  char timestamp[20];
  sprintf(timestamp, "%04d-%02d-%02d %02d:%02d:%02d",
          now.year, now.mon, now.date, now.hour, now.min, now.sec);

  float temp = sensorOK ? sht31.readTemperature() : NAN;
  float hum  = sensorOK ? sht31.readHumidity() : NAN;

  //Serial.printf("⏱️  Zeitstempel: %s\n", timestamp);
  //Serial.printf("🌡️  Temp: %.2f °C, 💧 Feuchte: %.2f %%\n", temp, hum);

  if (sdOK) {
    File dataFile = sd.open("/data.txt", FILE_WRITE);
    if (dataFile) {
      dataFile.printf("%s,%.2f,%.2f\n", timestamp, temp, hum);
      dataFile.close();
      Serial.println(timestamp);
      Serial.println(temp);
      Serial.println(hum);
      Serial.println("✅ Datei erfolgreich geschrieben.");
      blinkSuccess();
    } else {
      Serial.println("❌ Fehler beim Schreiben der Datei!");
      blinkError(5);
    }
  }

  // === Sensor abschalten ===
  digitalWrite(SHT31_POWER_PIN, LOW);
  pinMode(SHT31_POWER_PIN, INPUT);

  SPI.end();
  Wire.end();

  // === Nur RTC-fähige GPIOs isolieren ===
  rtc_gpio_isolate(GPIO_NUM_15);  // LED
  rtc_gpio_isolate(GPIO_NUM_25);  // RTC CLK
  rtc_gpio_isolate(GPIO_NUM_26);  // RTC DAT
  rtc_gpio_isolate(GPIO_NUM_27);  // RTC RST

  // === Deep Sleep für 1 Stunde ===
  //Serial.println("💤 Gehe in Deep Sleep für 1 Stunde...");
  esp_sleep_enable_timer_wakeup(3600ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {
  // nicht genutzt
}
