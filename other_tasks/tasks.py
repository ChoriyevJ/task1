""""""
"""
Task 1
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    def restore(self):
        self.deleted = False
        self.save()

# Task 2
class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    salary_from = models.IntegerField()
    salary_to = models.IntegerField()


class SalaryFilter(filter.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        salary_from = request.query_params.get('salary_from')
        salary_to = request.query_params.get('salary_to')

        if salary_from and salary_to:
            return queryset.filter(
                salary_from__gte=salary_from,
                salary_to__lte=salary_to
            )
        return queryset.filter(
            salary_from=salary_from
        )
"""
Task 2
"""


class VacancyListAPI(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer = serializers.VacansySerializer
    filter_backends = [SalaryFilter ,]
    filterset_fields = ('salary_from', 'salary_to')




"""
Task 3
"""
# pip install cryptography python-dotenv

from cryptography.fernet import Fernet
from django.conf import settings

def generate_key():

    key = Fernet.generate_key()
    with open('.env', 'w') as f:
        f.write(f'SECRET_KEY="{key.decode()}"')
    return key

def get_key():

    try:
        with open('.env') as f:
            key = f.read().split('=')[1].strip('"')
            return Fernet(key.encode())
    except FileNotFoundError:
        raise EnvironmentError("Missing .env file with SECRET_KEY")

def encrypt(data):

    fernet = get_key()
    return fernet.encrypt(str(data).encode()).decode()

def decrypt(data):

    fernet = get_key()
    try:
        return fernet.decrypt(data.encode()).decode()
    except cryptography.fernet.InvalidToken:
        return None


from django.db import models
from .utils import encrypt

class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    marja = models.DecimalField(max_digits=10, decimal_places=2)
    package_code = models.CharField(max_length=20)

    def __str__(self):
        return f"Product: {self.package_code}"

    def get_encrypted_data(self):
        data = {
            'price': encrypt(self.price),
            'marja': encrypt(self.marja),
            'package_code': self.package_code,
        }
        return data




from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        encrypted_data = instance.get_encrypted_data()
        data.update(encrypted_data)
        return data

"""
Task 4
"""


class Country(models.Model):
    title = models.CharField(max_length=255)


class League(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Season(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class Team(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    score = models.IntegerField()
    goals = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    fails = models.IntegerField()



class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE,
                                  simmetric=False)
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE,
                                  simmetric=False)
    round = models.IntegerField()
    home_team_goals = models.IntegerField()
    away_team_goals = models.IntegerField()

    date = models.DateField()
    time = models.TimeField()


class Player(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)

    age = models.IntegerField()

    goals = models.IntegerField()
    matches = models.IntegerField()
    number = models.IntegerField()


    team = models.ForeignKey(Team, on_delete=models.CASCADE)



"""
Leetcode
Task 5
"""
"""
1)
"""

class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        count = 0
        lenght = 0
        for char in s:
            if char != " ":
                count += 1
            elif count != 0:
                lenght = count
                count = 0
        if count != 0:
            lenght = count
        return lenght

"""
2)
"""

class Solution:
    def maximumPopulation(self, logs: List[List[int]]) -> int:

        population_count = dict()

        for log in logs:
            birth = log[0]
            death = log[1]

            for year in range(birth, death):
                if not population_count.get(year):
                    population_count[year] = 0
                population_count[year] += 1

        max_population = max(population_count.values())
        earliest_year = min(year for year, population in population_count.items() if population == max_population)
        return earliest_year














