from django.db import models

class CommonModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CityModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class PincodeModel(models.Model):
    city = models.ForeignKey(CityModel, related_name='pincodes', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.code