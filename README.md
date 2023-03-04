A web application designed to be used inside learning institution in the order to arrange education process digitally. 
Users are divided to students (basic users) and teachers (administrators). Registration is required to use the app. 
Student can view a list of different courses and join them. 
Teacher can add different elements in course area likea articles, videos etc. and also view a list of students enrolled in the course Student can 
also view statisticall information about his proceeding like the course grades et cetera.


SITUATION OF APP (3.2.2023):

I have created and finalized the basic features needed to use the app. There are now sign in and registration features on their own sites
and they should work without a problem. When loggin app displays a summary of chosen courses of user and another summary of all courses
which can be selected by making registration for them. Right the moment the course registration is just a visual concept and I am working
on to get it connected with Postgresql database.

SITUATION OF APP (17.2.2023)

I have now created a functional course registarion system. It is now a bit primitive but it will be developed more in future.
It is now also possible to use LearningApp as admin and create a new courses with admin rights. In curren situation the only thing
missing are the specific enviroments for each individual course and this will be the last thing of the project. I got a couple weeks
ago feedback and I am still working with some issues mentioned therein.

SITUATION OF APP (4.5.2023)

Unlikely I mentioned in my last review I did not created individual pages for each course but added a message feature.
This feature makes possible to share common affairs with all users of LearningApp. I also finalized the visual appearance of app
and it is now mostly okay. Improvements of programing style could still be made but time is running out. Overall all the basic features 
of app like login, registartion new account, adding new courses and issues can now be used without a problem. Only the course registration
system is still a bit primitive.

To test LearningApp in fly.io as user create a new profile or log in with credentials:

username: user

password: useruser


Te test LearningApp in fly.io as admin log in with credentials:

username: admin

password: adminadmin


fly.io address: https://learningapp.fly.dev/
