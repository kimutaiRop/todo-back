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
	todo = graphene.Field(TodoType, id=graphene.Int())
	todos = graphene.List(TodoType)
	success = graphene.Boolean()
	def resolve_todo(root, info,id):
		user = info.context.user
		success = True
		return Todo.objects.select_related("user").get(id=id, user=user)

	def resolve_todos(root, info):
		user = info.context.user
		return Todo.objects.filter(user=user)


class CreateTodo(graphene.Mutation):
	todo = graphene.Field(TodoType)

	class Arguments:
		place = graphene.String(required=True)
		title = graphene.String(required=True)
		date_time = graphene.String(required=True)

	@classmethod
	def mutate(cls,root,info,place,title,date_time):
		return Todo.objects.create(
			place=place,
			title = title,
			date_time=date_time,
			user=info.context.user
		)

class UpdateTodo(graphene.Mutation):
	todo = graphene.Field(TodoType)

	class Arguments:
		id=graphene.Int()
		place = graphene.String(required=True)
		title = graphene.String(required=True)
		date_time = graphene.String(required=True)

	@classmethod
	def mutate(cls,root,info,place,title,date_time, id):
		todo =  Todo.objects.get(id=id, user=info.context.user)
		todo.place=place
		todo.title = title
		todo.date_time = date_time
		todo.save()

		return todo


class TodoMutations(graphene.ObjectType):
	create_todo = CreateTodo.Field()
	update_todo = UpdateTodo.Field()

schema = graphene.Schema(query=Query, mutation=TodoMutations)
