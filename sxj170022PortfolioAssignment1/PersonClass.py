#PERSON CLASS
# create an initialize the person class constructor with last name, first name, middle initial, id and phone number

class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

# display the list of employees
    def display(self):

        print(" ", "Employee ID: ", self.id)
        print("\t", self.first,end='')
        print(" ", self.mi,end='')
        print(" ", self.last)
        print("\t", self.phone)



