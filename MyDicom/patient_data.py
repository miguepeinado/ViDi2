"""Wrapper with some of the patient data (ID and demographics"""


class PatientData():
    def __init__(self, dicom_set):
        self.name = ""
        self.id = ""
        self.birth_date = ""
        self.age = ""
        self.sex = ""
        self.weight = ""
        if dicom_set is not None:
            if 'PatientsName' in dicom_set:
                self.name = dicom_set.PatientsName
            if 'PatientID' in dicom_set:
                self.id = dicom_set.PatientID
            if 'PatientsBirthDate' in dicom_set:
                self.birth_date = dicom_set.PatientsBirthDate
            if len(self.birth_date) == 0:
                self.birth_date = '00000000'

            if 'PatientsAge' in dicom_set:
                self.age = dicom_set.PatientsAge
            else:
                self.age = '000Y'
            if 'PatientsSex' in dicom_set:
                self.sex = dicom_set.PatientsSex
            else:
                self.sex = 'U'
            if 'PatientsWeight' in dicom_set:
                self.weight = dicom_set.PatientsWeight
            else:
                self.weight = '0'

    def __str__(self):
        return self.as_dict().__str__()

    def __cmp__(self, other):
        return self.id == other.id

    def as_dict(self):
        return {'name': self.name, 'id' : self.id, 'birth_date': self.birth_date,
                'age': self.age, 'sex': self.sex, 'weight': self.weight}

    def demographics(self):
        n = self.name.split("^")
        n = n[0] + ", " + n[1]
        bd = self.birth_date[6:] + "/" + self.birth_date[4:6] + "/" + self.birth_date[0:4]
        return (n, "ID: {}".format(self.id), "{} ({})".format(bd, self.age))



