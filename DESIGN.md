As described in README.md, the purpose of my site is to allow students to rate the meals served at Annenberg each day and it is meant to present an
appealing visual display of the meal ratings for all to see. My project includes a mix of Python, Jinja, HTML, CSS, and Java in a general structure
quite similar to those of pset7 and pset8.

Since my site offers registration to both students and staff, I chose to place staff and student members into separate tables so as to make it easier
to recognize logged in users as either staff or student members, so I could then differentiate between the two groups since they have access to different
capabilities in the site.

One potential flaw in my site is that users have access to the page "Staff Meal Entries" and the staff have access to the page "Student Survey". Although I
managed to prevent students from filling out the "Staff Meal Entries" form and staff members from filling out the "Student Survey" form, I understand that it
is a bit odd for them to have access to these pages in the first place. I considered making two separate layout.html files for students vs. staff since I
only knew how to provide a unique nav bar on the premise that a user had been logged in (unsure how to differentiate between staff and student users in this
section of the code). However, I assumed that this may have been a bit overkill since I then would have likely had to have constructed two separate pages
for the "Survey Results", and this would have resulted in some repetition. So, I decided that it was alright to provide access of the "Staff Meal Entries"
to the students and access of the "Student Survey" to the staff, so long as they could not submit the forms displayed on these pages.

The third SQL table that is integral to my site is the "meals" table, which records the staff's entries for lunch and dinner. By utilizing the fact that
the id of the meals were autoincremented, I was able to specifically display the meals from the row in "meals" with the greatest id value in the form on
the student survey and in the display of the graphs.

Next, in the "votes" SQL table, while recording the ratings input by the students, I also chose to record the id of the student user as well as the
id of the latest meal (again taking advantage of the fact that the id of the meals was autoincremented) so I could ensure that each student could
submit the ratings form just once for any particular set of meals.

Finally, I chose to display the data in the form of bar graphs so as to provide a useful visual representation of the student feedback on meals. In
addition, I chose to display a slideshow of tasty food pictures on the home page for even greater visual appeal.