import graphene
from graphene_django import DjangoObjectType
from .models import Todo, User
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field() # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class UserType(DjangoObjectType):
	class Meta:
		fields = ['username',"id","first_name","last_name"]
		model = User
class TodoType(DjangoObjectType):
	user = graphene.Field(UserType, id=graphene.Int())
	class Meta:
		fields = '__all__'
		model = Todo


class Query(UserQuery, MeQuery,graphene.ObjectType):
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


class Mutations(AuthMutation, graphene.ObjectType):
	create_todo = CreateTodo.Field()
	update_todo = UpdateTodo.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
