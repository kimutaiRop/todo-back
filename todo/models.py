from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
	place = models.CharField(max_length=200)
	date_time = models.DateTimeField()

	def __str__(self):
		return self.title
