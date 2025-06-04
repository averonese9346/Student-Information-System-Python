#Writing a program that is a rudimentary student file recordkeeping system
#to add, delete, change students and show current students
#using a .json file to store database of students

#importing any modules we may need
import re  #we need this module for the pattern recognition
import json  #we need this module to have all student records saved in the json file

#Defining the main function (the "start" function as labeled in the project directions)
def main():
    while True: #while this is all true, this will appear on the screen as the main welcome screen
        #in a while loop because we want this to keep looping back to after certain functions
        readWelcome() #calling the readwelcome function (below) that defines the
        #function that reads and displays the welcome text from a .txt file

        operationCode = input(f"\nPlease Enter the Operation Code: ").strip() #making sure to strip of anything else
        #so this can be read as a string

        cusInput(operationCode) #calling the customer input function that will run the
        #user input for the entire main menu

##############################DEFINING ALL FUNCTIONS##################################
def readWelcome(): #defining the readwelcome function that shows the welcome text from the .txt file
    with open("userWelcome.txt", "r", encoding='utf-8') as welcomeText:  #naming the
        #name of the file, set to read, and setting the encoding so it displays properly
        text = welcomeText.read() #setting a new variable with our text and the readwelcome function
        #printing the results
        print(text, end = ' ')

######################################################################################

def cusInput(operationCode): #this is the customer input function that will take
    #any of the inputs the customer gives from the main menu and sends them
    #to the correct function from that menu option
    if operationCode == '1':    #if statements for each operation code making sure to use '' with the number so that
        #is read as a string and not as a literal integer
        addUser()  #then showing the function that is being called after the user inputs
        #the number choice selection
    elif operationCode == '2':
        delUser() #we will define all of these below for the program
    elif operationCode == '3':
        modifyUser()
    elif operationCode == '4':
        queryUser()
    elif operationCode == '5':
        displayUser()
    elif operationCode == '6':
        exitSystem()
    else:
        print("\u274C Please enter a valid operation code.") #unicode for x to state that
        #this is invalid message please enter a different operation code
        #and it will loop back to show the main menu

######################################################################################

#Defining the add user function, choice option #1
def addUser():
    print("======================Add Student======================\n"  #showing the rules first
          "1. The first letter of firstname and lastname must be capitalized.\n"
          "2. Firstname and lastname must each have at least two letters.\n"
          "3. No digit allowed in the name.\n"
          "4. Student ID is 6 digits long which must start with 700.\n"
          "5. Phone must be in the (xxx-xxx-xxxx) format.\n"
          "6. Student major must be in CS, CYBR, SE, IT, or DS.")

#make all of these their own function so that after each successful input we can move
#directly onto the next step and not get caught in a loop. calling each function here
    studentID = getStudentID()
    if studentID is None: #if the studentID is None then we will return to the main menu
        #meaning of the studentID is already a recognized studentID for another student then
        #it will go back to main menu, as it cannot add this user if the ID is already in place
        return
    studentName = getStudentName() #making sure to call all of our functions that will be used
    #to set the student information
    phoneNumber = getPhoneNumber()
    studentMajor = getStudentMajor()

    #if all inputs are valid create a new student record in the .json file. this is the pattern
    #for how we want the info to show up in the file.
    newStudent = {
        "ID": studentID,
        "Name": studentName,
        "Phone": phoneNumber,
        "Major": studentMajor
    }  #using curly brackets because we are putting all of this info in a dictionary
    #because they are key value pairs with the text and then the text answer

    #now saving the new student record to student.json using the readJSON() function
    students = readJSON("student.json")
    students.append(newStudent) #appending and adding to the list from the create user function

#now actually writing to that file and dumping all of the new info there
#using the writeJSON function
    students = writeJSON("student.json", students)

#printing this message that will print after all conditions have been met
#and the user input all info correctly for a new student
    print(f"\u2714 New student record has been added successfully!")

######################################################################################

#defining the getstudentID function so that we don't get stuck in a loop and accidentally
#entering each of these, if 1 is wrong the loop will go back to the very beginning
#instead of starting over from the point where the invalid info was given. we are avoiding that
#happening.
def getStudentID():
    students = readJSON("student.json")  #reading the JSON file to match the student IDs in various use cases below

    while True:
        studentID = input("Please enter the student ID: ").strip() #stripping of any thing the user might have added
        if re.fullmatch(r"700\d{3}", studentID):  #this is our pattern recognition
            #for student id per parameters
            #if statement meaning that if the input from the user matches the pattern then
            #we can return the ID back to the caller and move on to the next step.
            for student in students:  #each individual student in the students list
                if student["ID"] == studentID:  #if the student id [ID is in brackets bc it is part of the
                    #list and it is also in quotes bc it is a string in the list]
                    #given from the user is the same as an already existing student ID in the list
                    #then we cannot assign this user this ID so it asks them to enter a different ID
                    #and loops back to the main menu
                    print(f"\u274C Student ID already Exists in the System. Please Enter a Different ID.")
                    return None #returning back to the main menu as defined above
            return studentID  #return student ID if there is a match
        else:  #if not then we show error message and ask user to input a valid id per parameters
            print(f"\u274C {studentID} is an invalid Student ID.")

######################################################################################

#same as above except the pattern is different here
def getStudentName():
    while True:
        studentName = input("Please Enter the Student Name (Firstname Lastname): ").strip()
        if re.fullmatch(r"[A-Z][a-zA-Z]{1,} [A-Z][a-zA-Z]{1,}", studentName): #this means that we can only
            #have a name that starts with a uppercase letter and then either an upper or lower
            #case after that and it needs at least one other digit
            #both of these rules apply to first and last name
            return studentName
        else:
            print(f"\u274C {studentName} is an invalid name.")

######################################################################################

#same as above but with different pattern for phone number
def getPhoneNumber():
    while True:
        phoneNumber = input("Please Enter the Student Phone \u260E: ").strip() #added the unicode for phone icon per directions
        if re.fullmatch(r"\d{3}-\d{3}-\d{4}", phoneNumber): #pattern here is
            #3 digits, - , 3 digits, - , 4 digits
            return phoneNumber
        else:
            print(f"\u274C {phoneNumber} is an invalid phone number.")

######################################################################################

#same as above but no pattern here for major, instead we are checking through the list below
def getStudentMajor():
    while True:
        studentMajor = input("Please Enter the Student Major: ").strip()
        studentMajor = studentMajor.upper() #we need to make sure that even if the user
        #inputs a lowercase major it is saved properly in the .json file and still works
        #storing the strings of possible majors in a list so that we can cross check
        #against this list
        if studentMajor in ['CS', 'CYBR', 'SE', 'IT', 'DS']:
            return studentMajor
        else:
            print(f"\u274C {studentMajor} is an invalid student major.")

######################################################################################

#defining the display user function, option #5 on the main menu
def displayUser():
    print("======================Student Record======================")  #the title
    print(f"{"ID":<8} {"Name":<18} {"Phone":<15} {"Major"}")  #printing the headers with
    #defined paramters for their spacing the :<[number] within the brackets defines that
    students = readJSON("student.json")  #using the readJSON file function so that
    #we are checking through all of the students in the json file
    for student in students:
        print(f"{student["ID"]:<8} {student["Name"]:<18} {student["Phone"]:<15} {student["Major"]}")

######################################################################################

#defining querying a user (showing details about just one student), option 4 in main menu
def queryUser():
    students = readJSON("student.json") #using the readJSON file function to read the file
    #and then search through it to find the correct student

    while True: #while loop to iterate through the student ID given from the user
        #and cross checks the json file/list
        studentID = input("Please enter the student ID You Want to Query: ").strip() #stripping of any thing the user might have added

        if not re.fullmatch(r"700\d{3}", studentID):  #if it is not a full match to
            #match our pattern of a valid student id then we tell the user this is an
            #invalid id and go back to the main menu
            print("======================Student Record=====================")
            print(f"\u274C {studentID} is an invalid Student ID.")
            print("=========================================================")
            continue

        for student in students:  #for loop to iterate through if the ID is valid
            #if the student ID, student meaning individual student[brackets for the list] and
            #and the parameters in the quotations for string
            #if it matches then we use the below print statement to print the information
            #about the requested student using their student ID
            if student["ID"] == studentID:
                print("======================Student Record=====================")
                print(f"\u2709 ID: {student['ID']}, Name: {student['Name']}, Phone: {student['Phone']}, Major: {student['Major']}")
                print("=========================================================")
                return #then we can return to the main menu after
            #using f string formatting above to print the request envelope unicode

        print("======================Student Record=====================")
        print(f"\u274C The Student ID {studentID} Record Does Not Exist.")  #printing this statement
        #if the studentid does not exist at all in the system
        print("=========================================================")
        return  #we return to the main menu after

######################################################################################

#Defining the modify user function, option 3 on the main menu. this can change any of the
#student info.
def modifyUser():
    students = readJSON("student.json")  #using the readJSON file function to search
    #through the JSON file to find the correct student to modify

    while True: #while loop to iterate through the student ID given from the user
        #and cross checks the json file/list
        studentID = input("Please enter the Student ID to Modify: ").strip() #stripping of any thing the user might have added

        if not re.fullmatch(r"700\d{3}", studentID):  #if it is not a full match to
            #match our pattern of a valid student id then we tell the user this is an
            #invalid id and go back to the main menu
            print("======================Student Record=====================")
            print(f"\u274C {studentID} is an invalid Student ID.")
            print("=========================================================")
            continue

        for student in students:  #for loop to iterate through the list
            #making sure to refelct that the studentname input and same with phone and major
            #are equal values to the listed information in the json file which the
            #loop is iterating through
            studentName = student["Name"]
            phoneNumber = student["Phone"]
            studentMajor = student["Major"]

            #an if statement in the for loop
            #if the studentid in the json file matches the input then
            #we will show the students current information first
            #and then ask the user to input new information
            if student["ID"] == studentID:
                print("======================Student Record=====================")
                print(f"\u2709 ID: {student['ID']}, Name: {student['Name']}, Phone: {student['Phone']}, Major: {student['Major']}")
                #printing the student's current information found from the json file
                while True:  #in a while loop bc if the user does not follow directions
                    #we want to keep asking them to enter a valid name
                    #before moving onto the next step
                    newName = input("New name (press enter without modification): ").strip()  #stripping of any white space
                    #newname is the new input for the user
                    if not newName:  #if the name is not updated (if the user just pressed enter)
                        #then break the loop and move onto the next step
                        #just in case they don't want to update the name
                        break
                    if newName:
                        #if the new name matches the given parameters for a name (we need to check to make sure
                        #they followed the rules of inputting names, just like when we created a brand new user to begin)
                        if re.fullmatch(r"[A-Z][a-zA-Z]{1,} [A-Z][a-zA-Z]{1,}", newName):  # this means that we can only
                        # have a name that starts with a uppercase letter and then either an upper or lower
                        # case after that and it needs at least one other digit
                        # both of these rules apply to first and last name
                            student["Name"] = newName  #if the name is good then make sure that the variable
                        #is now newName instead of studentName
                            break #making sure to break the loop if it is good
                        else:
                            print(f"\u274C {newName} is an invalid name.")  #if the user does not follow the
                            #parameters we will tell them this is an invalid name and they will be looped to the
                            #question again

                #we need a new while loop because if the user does not enter
                #a valid phone number we do not want them to go to the next step
                #it should keep asking until user inputs a valid phone number
                while True:
                    newPhone = input(f"New phone \u2709 (press enter without modification): ").strip() #stripping of any white space
                    if not newPhone: #if the phone number is not updated or if the user
                        #just pressed enter then break the loop
                        break
                    if newPhone:  #if statement for new phone
                        if re.fullmatch(r"\d{3}-\d{3}-\d{4}", newPhone):  # pattern here is
                    # 3 digits, - , 3 digits, - , 4 digits #if it is a match to the parameters
                            student["Phone"] = newPhone  #then we can replace the phone number
                    #in the json file from the old one to the new phone, matching variables
                            break  #can break the loop if it is valid
                        else: #if not print a new phone number and make sure it iterates to ask again
                            print(f"\u274C {newPhone} is an invalid phone number.")

                #in a while loop to make sure that the user inputs  avalid major and if not
                #loops back to the question again
                while True:
                    newMajor = input("New major (press enter without modification): ").strip().upper() #stripping
                    #of any white space and also converting to uppercase as if the user inputs the major in
                    #lowercase we want it in uppercase saved to the json file
                    if not newMajor:  #if the major is not updated and the user just
                        #pressed enter then break the loop
                        break
                    if newMajor in ['CS', 'CYBR', 'SE', 'IT', 'DS']:  #if the newmajor is in
                        #one of these listed in the list then
                        #update the major from the json file to match the newmajor the user input
                        student["Major"] = newMajor
                        break #and break the loop
                    else:  #if it is not in that list then show the error message to the user
                        print(f"\u274C {newMajor} is an invalid student major. Must be CS, CYBR, SE, IT, or DS.")

                #If the user did not update anything or if the information is exactly the same
                #as it arleady is then print that the record was not modified
                #this is per the directions
                if (newName == "" or newName == studentName) and \
                    (newPhone == "" or newPhone == phoneNumber) and \
                        (newMajor == "" or newMajor == studentMajor):
                    print(f"\u274C Record not modified!")
                else:  #if its anything else (this loops back to the start of each
                    #of the while statements, meaning that if the directions are followed
                    #in each while statement now we are ready actually write to the json file
                    #with the new information
                    students = writeJSON("student.json", students)

                    print(f"\u2714 Student record updated successfully!") #success message
                return #return to main menu

        #this goes back to the original if statement after the user was asked to input
        #the studentid they wanted to modify. if they entered a studnetid that is not
        #in the system it gives this error messsage
        print("======================Student Record=====================")
        print(f"\u274C The Student ID {studentID} Record Does Not Exist.")  # printing this statement
        # if the studentid does not exist at all in the system
        print("=========================================================")
        return  # we return to the main menu after

######################################################################################

#Defining the delete user option, option #2 on the main menu
def delUser():
    students = readJSON("student.json")  #calling the readJSON function to read through
    #the student list to find the correct one to delete

    while True: #while loop to iterate through the student ID given from the user
        #and cross checks the json file/list
        studentID = input("Please enter the Student ID to Delete: ").strip() #stripping of any thing the user might have added
        for student in students: #for loop to begin iterating through the file
            if student["ID"] == studentID:  #if the student id is valid in our records/json file
                #then print the current student info
                print("======================Student Record=====================")
                print(
                    f"\u2709 ID: {student['ID']}, Name: {student['Name']}, Phone: {student['Phone']}, Major: {student['Major']}")
                # printing the student's current information found from the json file
                while True:  # in a while loop bc if the user does not follow directions
                    # we want to keep asking them to enter a valid ID
                    # before moving onto the next step
                    confirmation = input("Are you sure you want to delete this record? Y or N: ").strip().upper()  # stripping of any white space and
                    #making sure the user can enter either upper or lower case for Y or N
                    #confirmation is the user confirming whether they want to delete this file
                    if confirmation == 'N':
                        return  #if no then return to main menu
                    if confirmation == 'Y':  #if yes then
                        #create a new list that is updatedStudentList that is
                        #this new student for the old student in the students file if the studentID does not match
                        #the new id, essentially taking the id that the userinput OUT of the file, removing that ID
                        #but keeping everyone else since if it doesnt match then we keep it
                        updatedStudentList = [student for student in students if student['ID'] != studentID]

                        writeJSON("student.json", updatedStudentList) #now actually writing to the json file
                        #using the writeJSON function

                        print(f"\u2714 Student record deleted successfully!")  #success message
                        return #return to main menu
                    else:
                        print(f"\u274C That is not a valid confirmation. Enter either Y or N.") #if user enters
                        #anything but Y or N the loop continues
                    continue
        else:
            print(f"\u274C {studentID} is an invalid student ID.")  # if the user does not enter a valid
            #student id they will be asked to enter a valid one
            return #return to main menu if they dont give valid id

######################################################################################

#defining the exit system function, used to exit the system altogether.
def exitSystem():
    while True: #while loop to make sure that if the user enters something other than
        #yes or no they will be asked again (else)
        exitConfirmation = input("Do you Want to Exit the System? Enter Y or N: ").strip().upper()
        #exitconfirmation is the user telling the program whether or not they want to exit
        #with stripping the white space and making sure that if the user inputs either
        #upper or lower case it will still work
        if exitConfirmation == 'Y':
            exit()  #if the user wants to exit they can press Y to exit and exit() will stop the program
        if exitConfirmation == 'N':  #if the user says no it will return to the main menu
            return
        else:  #if the user enters anything else it will make the user enter a valid option
            print(f"\u274C That is not a valid option. Please select Y or N.")

######################################################################################

#defining the readJSON function so that every time we need to read the JSON student
#file we can jsut call it from here.
def readJSON(filename):
    try:
        with open("student.json", "r") as file:  #opening and creating and reading the file
            students = json.load(file)  #loading the file
    except (FileNotFoundError, json.JSONDecodeError):  #this will throw an exception error if
        #the file is not found, FileNotFoundError inherint built-in in Python
        students = [] #storing all new student info in a list so that we can add to the list
        #below of new students (below)
    return students

######################################################################################

#defining the write JSON file function so that every time we need to write the new data
#so the JSON file it will be called from here.
def writeJSON(filename, students):   #passing the arguments of the filename and
    #the file alias as 'students', with students = each time for variables in other functions
    with open("student.json", "w") as file:  #the write function syntax
        json.dump(students, file, indent=4) #dump is dumping the info there and saving it

######################################################################################

#Invoke the main function to actually run the program (start as it is called in the directions)
main()