from django.db import models
from django.conf import settings
# Create your models here.


class AirCraft(models.Model):
    model_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    seats = models.IntegerField()
    a_stat_list = [(0, 'operational'),
                   (1, 'under maintenance'), (2, 'suspended')]
    a_status = models.IntegerField(blank=False, choices=a_stat_list, default=0)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Flight(models.Model):
    aircraft = models.ForeignKey('AirCraft', on_delete=models.CASCADE)
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE)
    dep_airport = models.ForeignKey(
        'Airport', on_delete=models.CASCADE, related_name='dep_airport')
    arr_airport = models.ForeignKey(
        'Airport', on_delete=models.CASCADE, related_name='arr_airport')
    dep_time = models.DateTimeField()
    arr_time = models.DateTimeField()
    fare = models.IntegerField()
    fl_stat_list = [('S', 'Scheduled'), ('A', 'Active'),
                    ('L', 'Landed'), ('C', 'Cancelled')]
    fl_status = models.CharField(
        blank=False, choices=fl_stat_list, max_length=1, default='S')

    def __str__(self):
        return str(self.dep_airport)+' to '+str(self.arr_airport)+' at '+str(self.dep_time)


class Airport(models.Model):
    city = models.CharField(max_length=30)
    run_c = models.IntegerField()

    def __str__(self):
        return str(self.city)


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    fl_id = models.ForeignKey('Flight', on_delete=models.CASCADE)
    seat_n = models.IntegerField()
    total_fare = models.IntegerField()
    statuses = [(0, 'Confirmed'), (1, 'Pending')]
    status = models.IntegerField(blank=False, choices=statuses, default=0)

    def __str__(self):
        return str(self.user)+' '+str(self.fl_id.dep_airport)+' '+str(self.fl_id.arr_airport)


class AdminKey(models.Model):
    a_key = models.CharField(max_length=20)


class CongestionIndex(models.Model):
    delta = models.DurationField()


class Airline(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
