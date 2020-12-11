Oleksandra Baga
Bachelor Thesis
Obtaining Bachelor of Engineering (B.Eng)
Bachelor of Computer Engineering

===========================================================================================


Development of a database application for "Aca-Loan-Raspi"-project of PSE-Labaratory

===========================================================================================

* Software Arhictecture and Design
* User Stories
* Functional and non functional requirements
* UML Diagramm (Components, Use Cases)

* Programming of MIFARE DESFire Smart Cards - 13.56 MHz 
* Using RFID-Reader ACR122U NFC USB 
* Python 3.8 for the project implementation
* Django Web Framework (Server side)
* Django Finite State Machine
* SQLite Database

* REST API
* Client side Javascript
* jQuery

Start: Spring 2020
End: Winter 2020

** During Coronavirus Pandemie and spring + autumn quarantine with a two years old child at home. 

===========================================================================================
ABSTRACT

The work was written as part of the project "acaLoan-Raspi" of the PSE laboratory. In addition to the initial acaBot robot project, the acaLab projects mainly cover topics from the field of practical and technical computer science. During the development of the "acaLoan-Raspi" project, a distributed system is being developed. The server is implemented with the Python Web Framework Django. Programming is done in Python programming language. With the use of open source libraries, the step-by-step process for integrating the hardware is done with a low-level link for the C library and thus an RFID reader is connected to the Raspberry Pi board. A user-oriented client that is displayed to a user in a web browser in full screen mode has been implemented as an interactive web page in HTML and styling through CSS has been added.

===========================================================================================

The aim of this thesis is the development of a database application to manage the process of lending and returning the hardware to the students of the Beuth University of Applied Sciences in Berlin. For years, all tasks linked to loan management have been managed in a handy way, which leads to a large consumption of working time. The software developed should make it possible, after delivery, to operate an automated loan management system for training courses in the technical informatics course in the PSE laboratory.

There are three components to be developed: Register-Client with connected RFID reader, which sends the read UIDs of the student cards to the Server, which is implemented with the Python Web Framework Django and keeps all data records for administration busy verifying student cards and boards to borrow. The last component is Display-Client, which deals with the display of the information received from the server and an interface is available for the interaction between an end user and the server.

===========================================================================================

CONCLUSION

The goal of developing software for PSE laboratories set at the beginning of the work was successfully achieved. The implementation of all components and an interaction using the development server was successfully presented to the employees of the PSE laboratory. The acaLoan system enables students to independently borrow a Raspi board for the exercises in the PSE laboratory and to return it later. This reduces the amount of working time required to manage the on-board location and the employees can concentrate on further new spiritual and scientific challenges and thus contribute to the further development of the acaLab projects. The functionality of the acaLoan system allows students to borrow the Raspberry Board either for exercise in the laboratory or for independent work at home.

In addition, communication between students and the acaLoan system is reduced to the necessary minimum, so that a loan / return process is only carried out with three keystrokes. First the Loan / Return Board button is printed to start a new user session. Reading of the student card and Raspi boards takes place without further keystrokes only via the register client, which sends the read data to the server in the end point of the REST API. Depending on the type of board, it is determined whether the board that has been read is to be borrowed or returned. With the second press of the button, the student confirms his wish to borrow or return the board. With the third button press after the operation has been successfully completed, the student ends his session and enables the acaLoan system to be released to the next student.

For the implementation of the acaLoan system, extensive software engineering in the form of object-oriented analysis and the design of the finite state machine was carried out. The acaLoan system could not be implemented without a server, as user data must be stored for longer than one session: the student cards and the records of all loan transactions must be stored for at least one current semester, so that the employees of the PSE laboratory always have access to all stored ones prior loan process (from loan to return of a board). The server has been successfully implemented with Django web framework. It is also planned that at the end of the semester after the last return of a board, the records of the semester that has ended can be deleted. Access from the server to the display client is made possible by appropriate interfaces using RESTful communication. In the completed thesis, a necessary part called the register client was developed, to which an RFID reader was connected. The register client itself does not have a database and is only allowed to send the read data to the server. It is about a simplex connection, since message traffic is asymmetrical because the register client is not allowed to get any data back from the server and does not need to know about the successful or failed loan process. For the implementation of the register client uComputer Raspberry Pi was used, which was already available in the PSE laboratory and does not have to be delivered.

===========================================================================================

ANALYZE:

When developing custom acaLoan web application, Python was preferred to another programming language to take advantage of its simple and expressive syntax. Since Django is written in the Python programming language, it also makes more sense to write the thesis in Python code, since all components use Python syntax rules. Django provides the resources that were immediately needed during the implementation of the analyzed software: general processes such as database manipulation, HTML templates, URL routing, session management and security. With the MVC principle (Model-View-Controller), the user interface (UI) and the business logic levels of the acaLoan system are separated. Django supports various operating systems such as Windows, Linux and MacOS, so that there should not be strict software dependencies on acaLoan-System during the deployment of the Django with ASGI as well as in the future.

RFID tags are used to mark the Raspi boards as well as to authenticate the students. Since RFID radio waves are used for communication, RFID tags only need to be located within the reading range of the reader. This allows the small NFC tags to be stuck on the back of each board under the protective screen, so that the board can be read on the RFID reader without precise positioning on the reading field. Since the student cards of the Beuth University are made with MIFARE DESFire contactless chip card technology, it is possible to work with just one RFID reader in the acaLoan system and to read both the student's data and the Raspi boards.

At this point it has to be said that the RFID tags have certain disadvantages, which were discussed between the employee and the author of the thesis. However, the decision was made that RFID tags for the intended purposes of tracking the Raspi board (which Raspi board was borrowed by which student on which day and must be returned by which day) meet the security expectations of the PSE laboratory employees . RFID tags are not ideal in comparison for several reasons. Since an RFID tag cannot differentiate between readers, the information can be read by almost anyone once it leaves the original supply chain. Because RFID readers are so portable and the range of some tags is so great, fraudsters can gather information they would otherwise not have access to. This means that anyone can collect potentially sensitive information without anyone's knowledge. These disadvantages of the RFID tags were neglected, since both student cards and RFID tags glued to the Raspi boards do not retain any sensitive information and have a small range of up to 10 cm. There are two types of threats. Either the student card could be cloned by a perpetrator to impersonate a student and steal a Raspi board. Or a Raspi board tag could be cloned in order to create a record in the database by returning the board, although in reality the Raspi board never came back to the laboratory. Against the cloning of the Raspi tag, it was discussed that in the future in the PSE laboratory in the closet with the Raspi boards every space for each corresponding Raspi board will be equipped with a weight sensor and acaLoan system on the appearance of the specific weight will be expected. However, this is not the part of the existing thesis and is intended by employees of the PSE laboratory as an exciting task for the other thesis. It was first decided against the cloning of the student card that an existing access to a cabinet with Raspi boards along the two work tables of the employees of the PSE laboratory could guarantee a certain level of security. The other solutions will be discussed after the software has been delivered and are also outside the scope of the existing thesis.

Although the disadvantages of the RFID tags were mentioned above, it can be summarized that the new student cards that were used at the Beuth University from the summer semester 2018 are a reliable and contemporary solution. The card does not contain any electronic personal data of the students and the campus machines have to call up all personal data online using a pseudonym (i.e. there are no personal data in the machines either). So that if the personal data is lost, the unauthorized person cannot read it \ cite {website: 12}. That was the focus of the decision to use a student card as the only electronic means of identification during loan / return processes in the PSE laboratory.

In this thesis it was proved that the rental procedure for the Raspi boards (Lab and Home) was successfully automated with the selected means for use in the PSE laboratory. 

===========================================================================================


