import graphene
from graphene_django import DjangoObjectType
from django.db import models
from .models import CommonModel,CityModel

# ------------------------ Type Registry -------------------------------
class TypeRegistry:
    _instance = None
    _types = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, model, object_type, input_type):
        self._types[model] = {
            'object_type': object_type,
            'input_type': input_type
        }

    def get_type(self, model, type_key):
        return self._types[model][type_key]

# ------------------------ Generic Factories ---------------------------
class GraphQLTypeFactory:
    _field_map = {
        models.CharField: graphene.String,
        models.TextField: graphene.String,
        models.BooleanField: graphene.Boolean,
        models.IntegerField: graphene.Int,
        models.FloatField: graphene.Float,
        models.DateTimeField: graphene.DateTime
    }

    @classmethod
    def create_object_type(cls, model):
        return type(
            f'{model.__name__}Type',
            (DjangoObjectType,),
            {'Meta': type('Meta', (), {'model': model, 'fields': '__all__'})}
        )

    @classmethod
    def create_input_type(cls, model):
        fields = {}
        for field in model._meta.fields:
            if field.name == 'id':
                continue
            field_type = next(
                (graph_type for django_type, graph_type in cls._field_map.items()
                 if isinstance(field, django_type)),
                graphene.String
            )
            fields[field.name] = field_type(required=not field.blank)
        return type(f'{model.__name__}Input', (graphene.InputObjectType,), fields)

# ------------------------ Base Operations -----------------------------
class BaseMutation(graphene.Mutation):
    errors = graphene.List(graphene.String)
    
    class Meta:
        abstract = True

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            return cls.execute_operation(root, info, **kwargs)
        except Exception as e:
            return cls(errors=[str(e)])

    @classmethod
    def execute_operation(cls, root, info, **kwargs):
        raise NotImplementedError

# -------------------- Concrete Operation Classes ----------------------
# ------------------------ Generic Factories ---------------------------
def create_django_object_type(model: type[models.Model], **kwargs) -> type[DjangoObjectType]:
    """Factory for generating DjangoObjectTypes with explicit pk field"""
    meta_attrs = {
        'model': model,
        'fields': ['pk'] + [f.name for f in model._meta.fields]  # Explicitly include pk
    }
    return type(
        f'{model.__name__}Type',
        (DjangoObjectType,),
        {'Meta': type('Meta', (), meta_attrs)}
    )

# -------------------- Concrete Operation Classes ----------------------
class CreateMutation(BaseMutation):
    @classmethod
    def execute_operation(cls, root, info, input):
        model = cls.model
        object_type = TypeRegistry().get_type(model, 'object_type')
        
        # Create instance from validated input
        instance = model(**input)
        instance.full_clean()
        instance.save()
        
        # Return properly initialized DjangoObjectType instance
        return cls(result=object_type(instance))  # Pass model instance to constructor

# ------------------------ Schema Builder ------------------------------
class SchemaBuilder:
    def _create_mutations(self, model, object_type, input_type):
        # Ensure mutations return full object type with model instance
        create_mutation = type(
            f'Create{model.__name__}Mutation',
            (CreateMutation,),
            {
                'model': model,
                'result': graphene.Field(object_type),
                'Arguments': type('Arguments', (), {'input': input_type(required=True)})
            }
        )
        # Similar updates for update and delete mutations
# Similarly fix UpdateMutation
class UpdateMutation(BaseMutation):
    @classmethod
    def execute_operation(cls, root, info, id, input):
        model = cls.model
        object_type = TypeRegistry().get_type(model, 'object_type')
        instance = model.objects.get(pk=id)
        
        for field, value in input.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        
        return cls(result=object_type(instance))  # Return the updated instance
    
class DeleteMutation(BaseMutation):
    success = graphene.Boolean()

    @classmethod
    def execute_operation(cls, root, info, id):
        model = cls._meta.model
        instance = model.objects.get(pk=id)
        instance.delete()
        return cls(success=True)

# ------------------------ Schema Builder ------------------------------
class SchemaBuilder:
    def __init__(self):
        self.registry = TypeRegistry()
        self.type_factory = GraphQLTypeFactory()

    def register_model(self, model):
        object_type = self.type_factory.create_object_type(model)
        input_type = self.type_factory.create_input_type(model)
        self.registry.register(model, object_type, input_type)
        self._create_mutations(model, object_type, input_type)
        self._add_query_field(model, object_type)

    # def _create_mutations(self, model, object_type, input_type):
    #     # Create mutation classes with proper Meta declarations
    #     create_mutation = type(
    #         f'Create{model.__name__}Mutation',
    #         (CreateMutation,),
    #         {
    #             'Meta': type('Meta', (), {'model': model}),
    #             'result': graphene.Field(object_type),
    #             'Arguments': type('Arguments', (), {'input': input_type(required=True)})
    #         }
    #     )
    def _create_mutations(self, model, object_type, input_type):
        create_mutation = type(
            f'Create{model.__name__}Mutation',
            (CreateMutation,),
            {
                'model': model,
                'result': graphene.Field(object_type),
                'Arguments': type('Arguments', (), {
                    'input': input_type(required=True)
                })
            }
        )
        setattr(Mutation, f'create_{model.__name__.lower()}', create_mutation.Field())

        update_mutation = type(
            f'Update{model.__name__}Mutation',
            (UpdateMutation,),
            {
                'Meta': type('Meta', (), {'model': model}),
                'result': graphene.Field(object_type),
                'Arguments': type('Arguments', (), {
                    'id': graphene.ID(required=True),
                    'input': input_type(required=True)
                })
            }
        )

        delete_mutation = type(
            f'Delete{model.__name__}Mutation',
            (DeleteMutation,),
            {
                'Meta': type('Meta', (), {'model': model}),
                'Arguments': type('Arguments', (), {'id': graphene.ID(required=True)})
            }
        )

        # Register mutations
        setattr(Mutation, f'create_{model.__name__.lower()}', create_mutation.Field())
        setattr(Mutation, f'update_{model.__name__.lower()}', update_mutation.Field())
        setattr(Mutation, f'delete_{model.__name__.lower()}', delete_mutation.Field())

    def _add_query_field(self, model, object_type):
        field_name = f'all_{model.__name__.lower()}s'
        resolver = lambda self, info: model.objects.all()
        setattr(Query, field_name, graphene.List(object_type))
        setattr(Query, f'resolve_{field_name}', resolver)

# ------------------------ Schema Setup --------------------------------
class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    pass

# Initialize schema
schema_builder = SchemaBuilder()
schema_builder.register_model(CommonModel)
schema_builder.register_model(CityModel)

schema = graphene.Schema(query=Query, mutation=Mutation)