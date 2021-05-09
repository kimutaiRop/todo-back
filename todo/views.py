from django.shortcuts import render
from django.http import JsonResponse
from .models import Todo

def serializer(todo):
	user = todo.user
	return {
		'user':{
			"email":user.email,
			"username":user.username,
			"first_name":user.first_name,
			"last_name":user.last_name,
		},
		"timestamp":todo.timestamp,
		"place":todo.place,
		"date_time":todo.date_time,
	}

def get_todos(request):
	user = request.user
	todos = Todo.objects.filter(user=user)
	return JsonResponse({"data":[serializer(td) for td in todos]}, safe=False)