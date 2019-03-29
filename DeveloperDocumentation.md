<h1>Developer Documentation for the Medical Social Network</h1>

This documentation is for developers who wish to contribute the the application.  The documentation is split into 6 different categories:

* How to Obtain Source Code
* Layout of Directory Structure
* How to Build
* How to Set Up an Automated Weekly Build and Test
* How to Release
* How to find Bugs

<h2>How to Obtain Source Code</h2>

The source code repository is located here: https://github.com/Cmarquardt17/MedicalSocialNetwork.
The latest stable/released version will be found on the GitHub master branch link on the webpage.

<h2>Layout of Directory Structure</h2>
For our project, the website is laid out in five folders in a main Project folder. The folder includes project,  and the subfolders of project which are tests, _pycache_, users, templates, static, posts, main, and errors. Testing includes the unit testing of the website. While the other folders contain the python, html and css files that run the website.  There will be ReadMe’s for each folder to go into more detail about what is in each folder, and what each file does.

<h2>How to Build</h2>
The first step in building the network was to create wireframes for the complete feature release that entails homepage with the link to the GitHub for repository, contact us page, sign in and login in page for clinicians and patients. The wireframes were then used in creating a website in html. A local database is linked to the website that holds the clinician and patient information. For the clinicians, to test their credentials, their information will be linked back to the Federation of State Medical Boards, which shows if a clinician is certified that a backend developer or hospital authority can check and certify that that person is allowed to have doctor/clinican credentials.   

<h2>How to Test</h2>
To run the software/website, a patient or a clinician will need to either log in or sign up. When signing up, the clinician or patient will be added into the database with their information. For clinicians, they will need to verify their credentials, and patients will have to add in their medical history, but they will both have to put in their name, email address, phone number, username, password and other basic contact information, which will be stored in the database. When logging in, the patient or clinician will input their username and password which will then pull their information out of the database. Clinicians will be able to see and share information with their patients, while the patients will be able to friend their clinicians and share information they think is necessary to their clinician.

<h2>How to Set Up an Automated Weekly Build and Test</h2>
For our weekly build, we will use Travis. For our failure test case, we received test cannot be created from invalid user. When passed in an invalid user, we expected to get an invalid user, but, it still accepted the user and created it, which failed the test. 

<h2>How to Release</h2>
The way we will release is updating the code and documentation. This will then have the newest version readily available for the user, since it is a website, we do not have to have downloads for the new release. We will then do sanity-checking that the website and downloadable files are as we wish. 

<h2>How to find Bugs</h2>
A list of outstanding bugs can be found here:  https://medicalsocialnetwork.atlassian.net/projects/MSN/issues
