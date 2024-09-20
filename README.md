# Project Description: University Grades Telegram Bot
The project focuses on creating a Telegram bot that allows university students to save, manage, and track their grades. The bot will offer a simple interface for students to enter their grades, and generate statistical reports. The system will also be optimized for performance, ensuring that tasks like generating stats and formatting reports are handled efficiently.
Main Features:
Grade Entry: Users will be able to send their grades to the bot.
Data Storage: Grades will be saved in a database for future reference.
Statistics Generation: The bot will calculate various statistics (e.g., average grades, grade distribution) based on the stored data.
Report Generation: The bot will format these statistics into user-friendly reports in PDF, SVG, or PNG format.
Performance Optimization: Multithreading will be employed to ensure efficient report generation.


## Main Features:
+ **Grade Entry:** Users will be able to send their grades to the bot.
+ **Data Storage:** Grades will be saved in a database for future reference.
+ **Statistics Generation:** The bot will calculate various statistics (e.g., average grades, grade distribution) based on the stored data.
+ **Report Generation:** The bot will format these statistics into user-friendly reports in PDF, SVG, or PNG format.
+ **Performance Optimization:** Multithreading will be employed to ensure efficient report generation.


## Project Tasks
### 1. **Database**
**Goal:** Design and implement a  SQL database to store and manage user grades efficiently.
+ **Database Architecture:** Design a schema that stores user data, grades, and stats efficiently.
+ **Database Deployment:** Set up and deploy the chosen database system.
+ **Python API:** Develop an interface class to interact with the database (CRUD operations), making it easy for the bot to store and retrieve data.
### 2. Python Telegram Bot
**Goal:** Develop a Telegram bot for users to interact with the system, submit grades, and request statistics.
+ **Telegram Library Integration:** Integrate with a library to handle operations and user interactions.
+ **Grade Submission and Storage:** Implement the logic for users to submit their grades, which will be stored in the database.
+ **Statistics Calculation:** Add logic for generating various stats based on the grades (e.g., average, min/max, distribution).
+ **Report Formatting:** Implement logic to format statistics into different file formats (PDF, SVG, PNG).
+ **Bot Deployment:** Deploy the bot to a server and set up continuous operation (via Docker on AWS or Google Cloud).
### 3. Optimization
**Goal:** Improve the performance of the bot, especially for stats formatting and report generation.
+ **Multithreading Implementation:** Introduce multithreading to handle computationally intensive tasks (formatting large stats reports) efficiently.


## Definition of Done for University Grades Telegram Bot Project
**1.	Telegram Bot Functionality:**
+ The bot can receive and handle user inputs (grades) through the Telegram interface.
+ User interactions, such as submitting grades and requesting stats, are smooth and error-free.

**2.	Database Integration:**
+ A fully operational database is implemented to store user data, grades, and statistics.
+ The database can perform all necessary CRUD operations on grades and user information.

**3.	Grade Statistics:**
+ The bot is able to calculate necessary statistics (average, min/max grades, grade distributions).
+ All statistics are correctly computed based on the data stored in the database.

**4.	Report Generation:**
+ The bot can generate reports of the calculated statistics in multiple formats (PDF, SVG, PNG).
+ Reports are correctly formatted and visually clear, presenting the data in an easy-to-understand format.
+ Users can easily request these reports via the bot.

**5.	Performance Optimization:**
+ Multithreading is implemented for handling performance-heavy tasks such as report generation and formatting.
+ Performance benchmarks show that the bot can handle multiple requests concurrently without significant delays.

**6.	Bot Deployment:**
+ The bot is deployed to a production environment and runs continuously without interruptions.
+ The bot is available and responsive to users during testing and live usage.

**7.	Error Handling and Robustness:**
+ Comprehensive error handling is implemented to manage all possible issues.
+ The system can recover gracefully from failures and notify users appropriately in case of issues.

**8.	User Experience:**
+ The bot provides a smooth and intuitive user experience, including clear instructions and feedback for each command.
+ Users are notified of successful operations (e.g., grade submission, stat generation) and errors (e.g., invalid input).
+ The interface is simple, with easy-to-understand commands for interacting with the bot.

**9.	Testing:**
+ Unit, integration, and performance tests are written and pass successfully.
+ The system has been stress-tested with a large number of requests to ensure stability under load.
+ The entire system functions as expected in both normal and edge-case scenarios.
