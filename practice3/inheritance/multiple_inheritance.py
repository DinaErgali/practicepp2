class People:
    def __init__(self, race, sex):
        self.race = race
        self.sex = sex


people = People("Black", "Male")
print(
    f"Information about particular people:\n1. Race: {people.race}\n2. Sex: {people.sex}"
)


class Society(People):
    def __init__(self, race, sex, group):
        super().__init__(race, sex)
        self.group = group


print()
society = Society("White", "Female", "Workers")
print(
    f"Information about particular society:\n1. Race: {society.race}\n2. Sex: {society.sex}\n3. Group: {society.group}"
)


class Person(Society):
    def __init__(self, race, sex, group, name, age, hobby):
        super().__init__(race, sex, group)
        self.name = name
        self.age = age
        self.hobby = hobby


print()
person = Person("Asian", "Male", "Student", "Zhantore", 18, "Programming")
print(
    f"Personal information:\n1. Race: {person.race}\n2. Sex: {person.sex}\n3. Group: {person.group}\n4. Name: {person.name}\n5. Age: {person.age}\n6. Hobby: {person.hobby}"
)