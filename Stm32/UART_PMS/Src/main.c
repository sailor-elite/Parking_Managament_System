/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * <h2><center>&copy; Copyright (c) 2024 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under BSD 3-Clause license,
 * the "License"; You may not use this file except in compliance with the
 * License. You may obtain a copy of the License at:
 *                        opensource.org/licenses/BSD-3-Clause
 *
 ******************************************************************************
 */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "i2c.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "ssd1306.h"
#include "ssd1306_tests.h"
#include "ssd1306_fonts.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* Declare variables for UART data handling */

volatile char rx_data[1] = { 0 };
uint8_t rx_index = 0;
uint8_t led_on = 0;
volatile uint32_t led_on_time = 0;

#define BUFFER_SIZE 8

/* Define a circular buffer structure */

typedef struct {
	char buffer[BUFFER_SIZE];
	uint8_t head;
	uint8_t tail;
	uint8_t count;
} CircularBuffer;

CircularBuffer rx_buffer = { .head = 0, .tail = 0, .count = 0 };

/* Bitmap data for a car image (used with the display) */
// 'car', 102x42px
const unsigned char epd_bitmap_car[] = { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
		0xc0, 0x03, 0xff, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff,
		0xfc, 0x00, 0x00, 0x1f, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff,
		0xff, 0xf0, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xfc, 0xff, 0xff, 0xff,
		0xff, 0xff, 0xe0, 0x00, 0x00, 0x80, 0x1f, 0xff, 0xff, 0xfc, 0xff, 0xff,
		0xff, 0xff, 0xff, 0x84, 0x00, 0x00, 0x00, 0x03, 0xff, 0xff, 0xfc, 0xff,
		0xff, 0xff, 0xff, 0xfe, 0x00, 0xff, 0xfe, 0x00, 0x00, 0x7f, 0xff, 0xfc,
		0xff, 0xff, 0xff, 0xff, 0xf8, 0x01, 0xff, 0xfe, 0x70, 0x04, 0x0f, 0xff,
		0xfc, 0xff, 0xff, 0xff, 0xff, 0xe0, 0x07, 0xff, 0xfe, 0x7f, 0x01, 0x01,
		0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0x80, 0x1f, 0xff, 0xfc, 0x7f, 0xf0,
		0xe0, 0x3f, 0xfc, 0xff, 0xff, 0xff, 0xf8, 0x00, 0x3c, 0x00, 0xfc, 0x80,
		0x38, 0xf8, 0x0f, 0xfc, 0xff, 0xff, 0xf8, 0x00, 0x10, 0x00, 0x00, 0x00,
		0x00, 0x00, 0xff, 0x03, 0xfc, 0xff, 0xe0, 0x00, 0x00, 0x60, 0x00, 0x00,
		0x00, 0x00, 0x01, 0xff, 0xc0, 0xfc, 0xff, 0x00, 0x00, 0xff, 0xe3, 0xff,
		0xff, 0xfe, 0x3f, 0xff, 0xff, 0x80, 0x7c, 0xfe, 0x03, 0xff, 0xff, 0xf3,
		0xff, 0xff, 0xff, 0x3f, 0xff, 0xff, 0x00, 0x3c, 0xfc, 0x07, 0xff, 0xff,
		0xf3, 0xff, 0xff, 0xff, 0x3f, 0xff, 0xff, 0x9f, 0x1c, 0xe0, 0xcf, 0xe0,
		0xff, 0xf3, 0xff, 0xff, 0xf1, 0x3f, 0xe0, 0x7f, 0x87, 0x8c, 0x81, 0x8f,
		0x00, 0x1f, 0xf3, 0xff, 0xff, 0xf1, 0x3f, 0x80, 0x1f, 0xc0, 0xcc, 0x09,
		0x1e, 0x00, 0x0f, 0xf3, 0xff, 0xff, 0xfe, 0x3e, 0x00, 0x0f, 0xf0, 0x04,
		0x00, 0x1c, 0x00, 0x07, 0xf3, 0xff, 0xff, 0xfc, 0x7c, 0x00, 0x07, 0xfc,
		0x04, 0x00, 0x78, 0x80, 0x23, 0xf3, 0xff, 0xff, 0xfc, 0x7c, 0x00, 0x03,
		0xff, 0xe4, 0x23, 0xf1, 0x00, 0x13, 0xf3, 0xff, 0xff, 0xf8, 0xf9, 0x00,
		0x01, 0xff, 0xe4, 0x00, 0xf2, 0x0e, 0x01, 0xe3, 0xff, 0xff, 0xf9, 0xf0,
		0x0e, 0x09, 0xff, 0xe4, 0x00, 0xe0, 0x31, 0x89, 0xe3, 0xff, 0xff, 0xf1,
		0xf2, 0x19, 0x80, 0xff, 0xe4, 0x01, 0xe0, 0x20, 0x81, 0xe3, 0xff, 0xff,
		0xe3, 0xf2, 0x20, 0xc4, 0xff, 0xe4, 0x3f, 0xe4, 0x40, 0xc0, 0xe3, 0xff,
		0xff, 0xc7, 0xe0, 0x20, 0x40, 0xff, 0xc4, 0x1f, 0xe4, 0x40, 0x40, 0xe3,
		0xff, 0xff, 0x8f, 0xe0, 0x60, 0x64, 0xf8, 0x04, 0x01, 0xe4, 0x40, 0xc0,
		0xe3, 0xff, 0xff, 0x9f, 0xe0, 0x20, 0x44, 0x80, 0x0c, 0x80, 0x04, 0x20,
		0x80, 0xe3, 0xff, 0xff, 0x1f, 0xe2, 0x20, 0xc4, 0x01, 0xfc, 0xf8, 0x06,
		0x11, 0x08, 0x00, 0x00, 0x00, 0x00, 0x02, 0x19, 0x84, 0x1f, 0xfc, 0xff,
		0xfe, 0x0e, 0x08, 0x00, 0x00, 0x00, 0x00, 0x02, 0x0e, 0x0f, 0xff, 0xfc,
		0xff, 0xff, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x80, 0x07, 0x00, 0x1f, 0xff,
		0xfc, 0xff, 0xff, 0x80, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0x80, 0x3f,
		0xff, 0xfc, 0xff, 0xff, 0xe0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xe0,
		0x7f, 0xff, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
		0xff, 0xff, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };


/* Display const */

#define BITMAP_X 15
#define BITMAP_Y 30
#define BITMAP_WIDTH 102
#define BITMAP_HEIGHT 64

#define CURSOR_TITLE_X 7
#define CURSOR_TITLE_Y 0
#define CURSOR_GREEN_X 26
#define CURSOR_GREEN_Y 25
#define CURSOR_BLUE_X 34
#define CURSOR_BLUE_Y 25
#define CURSOR_RED_X 38
#define CURSOR_RED_Y 25

#define FONT_SYSTEM_SIZE Font_6x8
#define FONT_NOTIFICATION_TITLE Font_7x10
#define FONT_ZONE_NAME Font_16x26

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */


uint8_t TIME_CONDITION()
{
	return (HAL_GetTick() - led_on_time >= 5000);
}

uint8_t LED_ON_CONDITION() {
	return led_on > 0 && (TIME_CONDITION());
}

// Adds a character to the circular buffer if space is available

void buffer_push(CircularBuffer *cb, char data) {
	if (cb->count < BUFFER_SIZE) {
		cb->buffer[cb->head] = data;
		cb->head = (cb->head + 1) % BUFFER_SIZE;
		cb->count++;
	}
}

// Removes and returns a character from the circular buffer

char buffer_pop(CircularBuffer *cb) {
	if (cb->count > 0) {
		char data = cb->buffer[cb->tail];
		cb->tail = (cb->tail + 1) % BUFFER_SIZE;
		cb->count--;
		return data;
	}
	return 0;
}

// Returns the number of characters in the circular buffer


uint8_t buffer_available(CircularBuffer *cb) {
	return cb->count;
}

void DEFAULT_SCREEN() {
    ssd1306_Fill(Black);
    ssd1306_DrawBitmap(BITMAP_X, BITMAP_Y, epd_bitmap_car, BITMAP_WIDTH, BITMAP_HEIGHT, White);
    ssd1306_SetCursor(10, 0);
    ssd1306_WriteString("Parking Managament System", FONT_SYSTEM_SIZE, White);
    ssd1306_SetCursor(50, 9);
    ssd1306_WriteString("System", FONT_SYSTEM_SIZE, White);
    ssd1306_UpdateScreen();
    HAL_GPIO_WritePin(GREEN_ZONE_LEDOFF_GPIO_Port, GREEN_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
    HAL_GPIO_WritePin(BLUE_ZONE_LEDOFF_GPIO_Port, BLUE_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
    HAL_GPIO_WritePin(RED_ZONE_LEDOFF_GPIO_Port, RED_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
}

void GREEN_ZONE_NOTIFICATION_ENTRY() {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(CURSOR_TITLE_X, CURSOR_TITLE_Y);
    ssd1306_WriteString("Dostep do strefy:", FONT_NOTIFICATION_TITLE, White);
    ssd1306_SetCursor(CURSOR_GREEN_X, CURSOR_GREEN_Y);
    ssd1306_WriteString("GREEN", FONT_ZONE_NAME, White);
    ssd1306_UpdateScreen();
}

void GREEN_ZONE_NOTIFICATION_NO_ENTRY() {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(CURSOR_TITLE_X, CURSOR_TITLE_Y);
    ssd1306_WriteString("ZAKAZ do strefy:", FONT_NOTIFICATION_TITLE, White);
    ssd1306_SetCursor(CURSOR_GREEN_X, CURSOR_GREEN_Y);
    ssd1306_WriteString("GREEN", FONT_ZONE_NAME, White);
    ssd1306_UpdateScreen();
}

void BLUE_ZONE_NOTIFICATION_NO_ENTRY() {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(CURSOR_TITLE_X, CURSOR_TITLE_Y);
    ssd1306_WriteString("ZAKAZ do strefy:", FONT_NOTIFICATION_TITLE, White);
    ssd1306_SetCursor(CURSOR_BLUE_X, CURSOR_BLUE_Y);
    ssd1306_WriteString("BLUE", FONT_ZONE_NAME, White);
    ssd1306_UpdateScreen();
}

void RED_ZONE_NOTIFICATION_NO_ENTRY() {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(CURSOR_TITLE_X, CURSOR_TITLE_Y);
    ssd1306_WriteString("ZAKAZ do strefy:", FONT_NOTIFICATION_TITLE, White);
    ssd1306_SetCursor(CURSOR_RED_X, CURSOR_RED_Y);
    ssd1306_WriteString("RED", FONT_ZONE_NAME, White);
    ssd1306_UpdateScreen();
}

void BLUE_ZONE_NOTIFICATION_ENTRY() {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(CURSOR_TITLE_X, CURSOR_TITLE_Y);
    ssd1306_WriteString("Dostep do strefy:", FONT_NOTIFICATION_TITLE, White);
    ssd1306_SetCursor(CURSOR_BLUE_X, CURSOR_BLUE_Y);
    ssd1306_WriteString("BLUE", FONT_ZONE_NAME, White);
    ssd1306_UpdateScreen();
}

void RED_ZONE_NOTIFICATION_ENTRY() {
    ssd1306_Fill(Black);
    ssd1306_SetCursor(CURSOR_TITLE_X, CURSOR_TITLE_Y);
    ssd1306_WriteString("Dostep do strefy:", FONT_NOTIFICATION_TITLE, White);
    ssd1306_SetCursor(CURSOR_RED_X, CURSOR_RED_Y);
    ssd1306_WriteString("RED", FONT_ZONE_NAME, White);
    ssd1306_UpdateScreen();
}

void GREEN_ZONE_LED() {
	GREEN_ZONE_NOTIFICATION_ENTRY();
	HAL_GPIO_WritePin(GREEN_ZONE_LEDON_GPIO_Port, GREEN_ZONE_LEDON_Pin,
			GPIO_PIN_SET);
	HAL_GPIO_WritePin(GREEN_ZONE_LEDOFF_GPIO_Port, GREEN_ZONE_LEDOFF_Pin,
			GPIO_PIN_RESET);
	led_on = 1;
	led_on_time = HAL_GetTick();

}

void GREEN_ZONE_LED_ON() {
	HAL_GPIO_WritePin(GREEN_ZONE_LEDON_GPIO_Port,
	GREEN_ZONE_LEDON_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GREEN_ZONE_LEDOFF_GPIO_Port,
	GREEN_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
	DEFAULT_SCREEN();
}

void BLUE_ZONE_LED() {
	BLUE_ZONE_NOTIFICATION_ENTRY();
	HAL_GPIO_WritePin(BLUE_ZONE_LEDON_GPIO_Port, BLUE_ZONE_LEDON_Pin,
			GPIO_PIN_SET);
	HAL_GPIO_WritePin(BLUE_ZONE_LEDOFF_GPIO_Port, BLUE_ZONE_LEDOFF_Pin,
			GPIO_PIN_RESET);
	led_on = 2;
	led_on_time = HAL_GetTick();
}

void BLUE_ZONE_LED_ON() {
	HAL_GPIO_WritePin(BLUE_ZONE_LEDON_GPIO_Port,
	BLUE_ZONE_LEDON_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(BLUE_ZONE_LEDOFF_GPIO_Port,
	BLUE_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
	DEFAULT_SCREEN();
}

void RED_ZONE_LED() {
	RED_ZONE_NOTIFICATION_ENTRY();
	HAL_GPIO_WritePin(RED_ZONE_LEDON_GPIO_Port, RED_ZONE_LEDON_Pin,
			GPIO_PIN_SET);
	HAL_GPIO_WritePin(RED_ZONE_LEDOFF_GPIO_Port, RED_ZONE_LEDOFF_Pin,
			GPIO_PIN_RESET);
	led_on = 3;
	led_on_time = HAL_GetTick();
}

void RED_ZONE_LED_ON() {
	HAL_GPIO_WritePin(RED_ZONE_LEDON_GPIO_Port, RED_ZONE_LEDON_Pin,
			GPIO_PIN_RESET);
	HAL_GPIO_WritePin(RED_ZONE_LEDOFF_GPIO_Port,
	RED_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
	DEFAULT_SCREEN();
}

void GREEN_ZONE_NO_ENTRY() {
	GREEN_ZONE_NOTIFICATION_NO_ENTRY();
	led_on = 4;
	led_on_time = HAL_GetTick();
}

void GREEN_ZONE_LED_NO_ENTRY() {
	HAL_GPIO_WritePin(GREEN_ZONE_LEDON_GPIO_Port,
	GREEN_ZONE_LEDON_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GREEN_ZONE_LEDOFF_GPIO_Port,
	GREEN_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
	DEFAULT_SCREEN();
}

void BLUE_ZONE_NO_ENTRY() {
	BLUE_ZONE_NOTIFICATION_NO_ENTRY();
	led_on = 5;
	led_on_time = HAL_GetTick();
}

void BLUE_ZONE_LED_NO_ENTRY() {
	HAL_GPIO_WritePin(BLUE_ZONE_LEDON_GPIO_Port,
	BLUE_ZONE_LEDON_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(BLUE_ZONE_LEDOFF_GPIO_Port,
	BLUE_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
	DEFAULT_SCREEN();
}

void RED_ZONE_NO_ENTRY() {
	RED_ZONE_NOTIFICATION_NO_ENTRY();
	led_on = 6;
	led_on_time = HAL_GetTick();
}

void RED_ZONE_LED_NO_ENTRY() {
	HAL_GPIO_WritePin(RED_ZONE_LEDON_GPIO_Port, RED_ZONE_LEDON_Pin,
			GPIO_PIN_RESET);
	HAL_GPIO_WritePin(RED_ZONE_LEDOFF_GPIO_Port,
	RED_ZONE_LEDOFF_Pin, GPIO_PIN_SET);
	DEFAULT_SCREEN();
}

/* Function to process the received command */

void process_command(void) {

	while (buffer_available(&rx_buffer) >= 2) {
		char command[3] = { 0 };
		command[0] = buffer_pop(&rx_buffer);
		command[1] = buffer_pop(&rx_buffer);

		if (strlen(command) == 2 && TIME_CONDITION()) {
			if (strcmp(command, "11") == 0) {
				GREEN_ZONE_LED();
			} else if (strcmp(command, "21") == 0) {
				BLUE_ZONE_LED();
			} else if (strcmp(command, "31") == 0) {
				RED_ZONE_LED();
			} else if (strcmp(command, "10") == 0) {
				GREEN_ZONE_NO_ENTRY();
			} else if (strcmp(command, "20") == 0) {
				BLUE_ZONE_NO_ENTRY();
			} else if (strcmp(command, "30") == 0) {
				RED_ZONE_NO_ENTRY();
			}

		}
	}

}

/* Function to process UART transmission */


void UART_TransmitInit() {
	char message[] = "Init MSG\r\n";
	HAL_UART_Transmit(&huart2, (uint8_t*) message, strlen(message), 1000);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
	if (huart->Instance == USART2) {
		buffer_push(&rx_buffer, rx_data[0]);
		HAL_UART_Receive_IT(&huart2, (uint8_t *) rx_data, 1);
	}
}





/* USER CODE END 0 */

/**
 * @brief  The application entry point.
 * @retval int
 */
int main(void) {
	/* USER CODE BEGIN 1 */

	/* USER CODE END 1 */

	/* MCU Configuration--------------------------------------------------------*/

	/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
	HAL_Init();

	/* USER CODE BEGIN Init */

	/* USER CODE END Init */

	/* Configure the system clock */
	SystemClock_Config();

	/* USER CODE BEGIN SysInit */

	/* USER CODE END SysInit */

	/* Initialize all configured peripherals */
	MX_GPIO_Init();
	MX_USART2_UART_Init();
	MX_TIM2_Init();
	MX_I2C1_Init();
	/* USER CODE BEGIN 2 */
	UART_TransmitInit();
	HAL_UART_Receive_IT(&huart2, (uint8_t *) rx_data, 1);
	ssd1306_Init();
	DEFAULT_SCREEN();

	/* USER CODE END 2 */

	/* Infinite loop */
	/* USER CODE BEGIN WHILE */
	while (1) {

		process_command();
		if (LED_ON_CONDITION()) {
			switch (led_on) {
			case 1:
				GREEN_ZONE_LED_ON();
				break;
			case 2:
				BLUE_ZONE_LED_ON();
				break;
			case 3:
				RED_ZONE_LED_ON();
				break;
			case 4:
				GREEN_ZONE_LED_NO_ENTRY();
				break;
			case 5:
				BLUE_ZONE_LED_NO_ENTRY();
				break;
			case 6:
				RED_ZONE_LED_NO_ENTRY();
				break;
			}
			led_on = 0;

		}
		/* USER CODE END WHILE */

		/* USER CODE BEGIN 3 */
	}
	/* USER CODE END 3 */
}

/**
 * @brief System Clock Configuration
 * @retval None
 */
void SystemClock_Config(void) {
	RCC_OscInitTypeDef RCC_OscInitStruct = { 0 };
	RCC_ClkInitTypeDef RCC_ClkInitStruct = { 0 };

	/** Configure the main internal regulator output voltage
	 */
	__HAL_RCC_PWR_CLK_ENABLE()
	;
	__HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
	/** Initializes the CPU, AHB and APB busses clocks
	 */
	RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
	RCC_OscInitStruct.HSIState = RCC_HSI_ON;
	RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
	RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
	if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
		Error_Handler();
	}
	/** Initializes the CPU, AHB and APB busses clocks
	 */
	RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
			| RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
	RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
	RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
	RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
	RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

	if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK) {
		Error_Handler();
	}
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
 * @brief  This function is executed in case of error occurrence.
 * @retval None
 */
void Error_Handler(void) {
	/* USER CODE BEGIN Error_Handler_Debug */
	/* User can add his own implementation to report the HAL error return state */

	/* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
