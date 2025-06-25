from django.db import models

class Role(models.Model):
    RoleId = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=100)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.RoleName

class Staff(models.Model):
    StaffId = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    Gender = models.CharField(max_length=10)
    JoiningDate = models.DateField()
    MobileNumber = models.CharField(max_length=15)
    UserName = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=128)  # Use Django's hashing for passwords
    RoleId = models.ForeignKey(Role, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.FullName

class Specialization(models.Model):
    SpecializationId = models.AutoField(primary_key=True)
    SpecializationName = models.CharField(max_length=100)

    def __str__(self):
        return self.SpecializationName

class Doctor(models.Model):
    DoctorId = models.AutoField(primary_key=True)
    ConsultationFee = models.DecimalField(max_digits=10, decimal_places=2)
    SpecializationId = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    StaffId = models.OneToOneField(Staff, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.StaffId.FullName}"

class Membership(models.Model):
    MembershipId = models.AutoField(primary_key=True)
    MembershipType = models.CharField(max_length=100)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.MembershipType

class Patient(models.Model):
    PatientId = models.AutoField(primary_key=True)
    PatientName = models.CharField(max_length=100)
    DateOfBirth = models.DateField()
    Gender = models.CharField(max_length=10)
    MobileNumber = models.CharField(max_length=15)
    Address = models.TextField()
    MembershipId = models.ForeignKey(Membership, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.PatientName

class Appointment(models.Model):
    AppointmentId = models.AutoField(primary_key=True)
    AppointmentDate = models.DateTimeField()
    TokenNumber = models.IntegerField()
    ConsultationStatus = models.CharField(max_length=50)
    PatientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    DoctorId = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return f"Appointment {self.AppointmentId} - {self.AppointmentDate}"

class MedicineCategory(models.Model):
    MedicineCategoryId = models.AutoField(primary_key=True)
    MedicineCategoryName = models.CharField(max_length=100)

    def __str__(self):
        return self.MedicineCategoryName

class Medicine(models.Model):
    MedicineId = models.AutoField(primary_key=True)
    MedicineName = models.CharField(max_length=100)
    ManufacturingDate = models.DateField()
    ExpiryDate = models.DateField()
    Unit = models.CharField(max_length=50)
    MedicineCategoryId = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.MedicineName

class MedicinePrescription(models.Model):
    MedicinePrescriptionId = models.AutoField(primary_key=True)
    MedicineId = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    Dosage = models.CharField(max_length=50)
    Frequency = models.CharField(max_length=50)
    Duration = models.CharField(max_length=50)
    AppointmentId = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

class Consultation(models.Model):
    ConsultationId = models.AutoField(primary_key=True)
    Symptoms = models.TextField()
    Diagnosis = models.TextField()
    Notes = models.TextField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    AppointmentId = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

class MedicineStock(models.Model):
    MedicineStockId = models.AutoField(primary_key=True)
    StockInHand = models.IntegerField()
    ReOrderLevel = models.IntegerField()
    Purchase = models.IntegerField()
    Issuance = models.IntegerField()
    MedicineId = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    CreatedDate = models.DateField()
    IsActive = models.BooleanField(default=True)

class LabTestCategory(models.Model):
    LabTestCategoryId = models.AutoField(primary_key=True)
    LabTestCategoryName = models.CharField(max_length=100)

    def __str__(self):
        return self.LabTestCategoryName

class LabTest(models.Model):
    LabTestId = models.AutoField(primary_key=True)
    TestName = models.CharField(max_length=100)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    ReferenceMinRange = models.DecimalField(max_digits=10, decimal_places=2)
    ReferenceMaxRange = models.DecimalField(max_digits=10, decimal_places=2)
    SampleRequired = models.CharField(max_length=100)
    LabTestCategoryId = models.ForeignKey(LabTestCategory, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.TestName

class LabTestPrescription(models.Model):
    LabTestPrescriptionId = models.AutoField(primary_key=True)
    LabTestId = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    LabTestValue = models.DecimalField(max_digits=10, decimal_places=2)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    Remarks = models.TextField()
    AppointmentId = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)
