# Polyball Enroller Bot

## Overview

The Polyball Enroller Bot is an automated script that uses Selenium to handle the repetitive task of enrolling in shifts on the Polyball helper portal. It navigates through the shift enrollment page, selects available shifts, and confirms enrollment, making it easier to secure shift slots as soon as they become available.

### Key Features
- **Automated Login**: Automatically logs into the helper portal using provided credentials.
- **Shift Enrollment**: Detects all available shifts and attempts to enroll in each one, clicking through the necessary steps.
- **Stale Element Handling**: Handles dynamic changes in the DOM and stale element references to ensure reliable operation.
- **Real-Time Feedback**: Logs the enrollment status for each shift and reports errors if they occur.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Setup](#setup)
3. [Usage](#usage)

## Project Structure

```plaintext
polyball_enroller/
├── shifts.py                # Main script to run the shift enrollment process
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```
### shifts.py
Contains the main script that performs the following tasks:
- Logs into the Polyball helper portal.
- Finds and clicks each shift available on the page.
- Confirms enrollment by clicking through a series of buttons and modal dialogs.
- Provides real-time status updates on the console.

### requirements.txt
Lists all dependencies required to run the script. The primary dependency is Selenium, which is used for web automation.

## Setup

### Prerequisites
- **Python 3.7+**: Ensure you have Python installed.
- **ChromeDriver**: Download the ChromeDriver binary that matches your Chrome browser version from [ChromeDriver](https://chromedriver.chromium.org/) and add it to your system's PATH.

### Installation
Clone the repository:

```bash
git clone https://github.com/yourusername/polyball_enroller.git
cd polyball_enroller
```

### Set up environment variables for login credentials:
Create a .env file in the project root with your Polyball helper portal credentials:

```bash
EMAIL=your_username
PASSWORD=your_password
CHROMEDRIVER_PATH=path_to_your_chromedriver.exe
```
Verify ChromeDriver: Ensure chromedriver.exe is accessible. You may need to add it to your PATH or specify its path in the script.

## Usage

### Running the Script
Start the bot:

```bash
python shifts.py
```
What to Expect
- The bot will attempt to log into your account.
- Once logged in, it will scan for all available shifts and click to enroll in each one.
- For each shift, the bot will open a modal, click the "Enroll" button, confirm the enrollment, and return to the main shift page.
- Console output will indicate the bot’s progress and any errors encountered.

### Example Output
The console will output logs similar to the following:
```bash
Login successful.
Enrolling in shift 1...
Shift clicked
Enrolled in shift 1
Enrolling in shift 2...
Shift clicked
StaleElementReferenceException caught, re-fetching shift list
Enrolled in shift 2
No more shifts to enroll in.
```
