# Fitness Tracker 🏋️‍♂️

A full-stack, responsive web application built with Django that allows users to log, track, and visualize their workout progress over time. 


## ✨ Features

* **User Authentication:** Secure registration, login, and logout functionality. Users can only see and edit their own workout data.
* **Dynamic Workout Logging:** * Log the date and general notes for a workout session.
  * Dynamically add, edit, or remove multiple exercises, sets, reps, and weights within a single session using JavaScript-powered formsets.
* **Progress Dashboard:** Visualizes the user's total volume (reps × weight) over their last 10 workouts using an interactive Chart.js line graph.
* **Full CRUD Functionality:** Create, Read, Update, and Delete capabilities for all workout records.
* **Responsive Design:** Styled with Bootstrap 5 and Django Crispy Forms for a modern, mobile-friendly user experience.
* **Pagination:** Easily navigate through an extensive history of past workouts.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Database:** PostgreSQL
* **Frontend:** HTML, JavaScript, Bootstrap 5, Chart.js, Django Crispy Forms
* **Deployment:** Digital Ocean Droplet (Ubuntu), Gunicorn, Nginx
* **Security:** Let's Encrypt (SSL/HTTPS), python-dotenv (Environment Variables)

## 🚀 Local Setup and Installation

To run this project on your local machine, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/schaefferda/fitness-tracker.git](https://github.com/schaefferda/fitness-tracker.git)
cd fitness-tracker
