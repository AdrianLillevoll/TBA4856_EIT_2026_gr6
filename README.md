# TBA4856 EIT 2026 gruppe 6
Experts in Team 2026 group 6

This application was created during the course EIT (experts in team) at NTNU spring 2026.

The team project was about the value of sport arenas. During the 15 days of work this project lasted the team created a framework for giving score to sport arenas. This score is based on a set of questions divided into three categories: social, environment and economy. Each question gives a score for its category and are afterwards summarized into an average score. The user can adjust the weighting of the three categories before result is printed. 

This application is a small implementation of the framework. The application can be used to test the logic and questions, but cannot be released as fully functional. Any security mitigations have not been prioritized due to short amount of time. There are not implemented any login functionality, database or docker compatibility. The architechture is flat, without strict frontend/backend and the questions are stored in json format at root level. 

## Prerequisites

If you want to run the application, these are the neccessary programs you need:
- Python 3.11+ with pip 


## Quick installation

- Navigate the root folder of the program and run the command: 
  ```pip install flask```
- Wait for the terminal to finish.
- Then run the command:
  ```python app.py```