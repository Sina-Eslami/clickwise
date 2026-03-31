# clickwise
Python automation app using Tkinter, pyautogui &amp; pynput. Record click positions or capture screen regions, the app waits until the target image appears on screen, then clicks automatically. Lightweight and efficient, no extra folder needed.

**ClickWise** is a smart, free auto-clicker desktop application developed as part of a 
Data Engineering project in collaboration with the **IEIS department of 
Eindhoven University of Technology**.

Unlike generic auto-clickers, ClickWise is built with intelligence and reliability 
in mind — featuring a **CI/CD pipeline** with post-observation testing and validated 
modules to minimize bugs and ensure stable releases.

---

## Features

- **Timer Click** — Set a countdown timer; the click triggers once the timer expires.
- **Screenshot Click** *(Smart Mode)* — Capture a reference screenshot of a UI element. 
  Once the timer expires, ClickWise scans the screen and places the click the moment 
  that element appears.
- **Repeat Count** — After configuring your click, set a positive integer to repeat 
  the entire process as many times as needed.
- **Process Log** — The home screen keeps a live log of all your previously automated 
  click processes.
- **Input Validation** — Red error prompts appear instantly if invalid input is entered 
  (e.g. non-integer or negative values for time or repeat count).

---

## How It Works

1. Launch the app and land on the **Home Page**.
2. Choose between **Timer Click** or **Screenshot Click**.
3. Configure your timer and (optionally) capture a reference screenshot.
4. Proceed to the **Finishing Frame** to set how many times to repeat the process.
5. Let ClickWise handle the rest.

---

## Project Status

> ⚠️ Some features are currently **deactivated** and under development.  
> The project is actively maintained and will continue to improve with new releases.

---

## Tech Stack

- **Language:** Python
- **UI Framework:** Tkinter
- **Deployment:** CI/CD with post-observation testing

---

## Acknowledgements

This project was developed in collaboration with the  
**Information Engineering and Innovation Systems (IEIS) Department**  
at **Eindhoven University of Technology (TU/e)**.

---

## License

This project is fully free and open-source.
