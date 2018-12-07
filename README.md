My name is David Carey and my final project is titled "Better Bites @ Berg." My project is a web app that can be run through Flask in the CS50 IDE.
Much of the general structure of my code was based off the CS50 staff's implementation of the finance pset8 distribution code. Upon compiling/configuring
my project with Flask, the user will be brought to the login page for my site.

There, the user is prompted for a username/password to log into the site. For those without an account, there are links in the nav bar to register as either
a Harvard freshman student or an Annenberg staff member. By inputting a username that has not already been taken by staff members/students, along with
inputting a password with confirmation, the user will be registered to the site (with the id, username, and password hashes of staff members inserted
into a SQL database table titled "staff_users" and the id, username, and password hashes of student members inserted into a SQL database table titled
"student_users") and brought to the home page of the site.

The home page displays a Bootstrap slideshow that transitions through a few pictures of Annenberg and different meals offered. In the nav bar that is now
displayed for logged in users (for both newly registered users and users who have just logged in), there are links to pages titled "Staff Meal Entries",
"Student Survey", and "Survey Results". Both students and staff have access to the page titled "Staff Meal Entries", which prompts the user for their account
password, as well as the names of the prior night's lunch and dinner. However, only users registered as staff members can submit this form, whereas
students will receive an error message. Upon submission, the id, lunch, and dinner will be inserted into a SQL database titled "meals".

On the page titled "Student Survey", there is a survey titled "Food Ratings Survey" which can be completed by only student users. This survey also asks
for the password of the student's account and asks the user to rate the lunch and dinner from the most recent staff submission on a scale of 1 to 5. The
student can submit this form just once and cannot submit it again until the staff has input a new round of meals the next day. This works because
the most recent meals that the staff has input will have the greatest id number in the SQL table "meals", and the student survey displays the meals
that correspond to the greatest id in the table "meals".

From there, the student ratings are input into a fourth SQL database titled "votes", which records the id number of the vote, as well as the values of the
lunch_rating and the dinner_rating, along with the student_user_id and the meals_id (the last two components being used to confirm that each student can
rate the latest set of meals just once).

The final page displays the Survey Results in the form of two bar graphs that display the student ratings of the lunch and dinner from the past day. These
graphs were implemented with Bootstrap/JavaScript etc.

So, essentially, this site operates on the premise that the staff will update the meals served each day, and the students will provide ratings that same day
that will be displayed in graphs to provide valuable feedback to the staff regarding how well-liked different main courses are.