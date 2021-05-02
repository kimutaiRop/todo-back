import graphene
from graphene_django import DjangoObjectType
from .models import Todo, User

class UserType(DjangoObjectType):
	class Meta:
		fields = ['username',"id","first_name","last_name"]
		model = User
class TodoType(DjangoObjectType):
	user = graphene.Field(UserType, id=graphene.Int())
	class Meta:
		fields = '__all__'
		model = Todo


class Query(graphene.ObjectType):
	todo = graphene.Field(TodoType, id=graphene.String())
	todos = graphene.List(TodoType)
	success = graphene.Boolean()
	def resolve_todo(root, info,id):
		user = info.context.user
		success = True
		return Todo.objects.select_related("user").get(id=int(id), user=user)

	def resolve_todos(root, info):
		user = info.context.user
		return Todo.objects.filter(user=user)

schema = graphene.Schema(query=Query)
