from django.db.models import QuerySet, Model
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.request import HttpRequest
from rest_framework import status, viewsets

from apps.base.pagination import GenericOffsetPagination



class ImplementReadOnlySerializer:
    read_only_serializer:ModelSerializer.__class__ = None
    
    def get_read_only_serializer(self, *args, **kwargs) -> ModelSerializer:
        assert self.read_only_serializer is not None, "Debe especificar la clase del readOnly Serializer"
        return self.read_only_serializer(*args, **kwargs)
        

class ImplementGenericResponses:
    
    @property
    def model_name(self):
        return self.serializer_class.Meta.model.__name__
    
    def get_not_found_response(self, message:str = None) -> Response:
        return Response({
            "message": message or "No se han encontrado resultados"
        }, status=status.HTTP_404_NOT_FOUND)
    
    def get_ok_response(self, data:dict[str, str], message:str = None) -> Response:
        detail = data.copy()
        if message is not None:
            detail["message"] = message
        
        
        return Response(detail, status=status.HTTP_200_OK)
    
    def get_created_response(self, data:dict[str, object] = None, message:str = None):
        data = data if data is not None else {}
        return Response({
            **data,
            "message":"Objeto {modelName} creado exitosamente".format(modelName=self.model_name)
        }, status=status.HTTP_201_CREATED)
    
    
    def get_bad_request(self, details:dict[str, object], message:str=None) -> Response:
        return Response({
            "message": message or "Ha ocurrido un error con su solicitud",
            **details,
        }, status=status.HTTP_400_BAD_REQUEST)
    

class GetQuerysetMixin:
    
    select_related_qs: list|tuple = tuple()
    prefetch_related_qs: list|tuple = tuple()
    qs_annotate: dict[str, object] = {}
    
    def get_related_queries(self) -> QuerySet:
        model:Model = self.serializer_class.Meta.model 
        return model.objects\
            .select_related(*self.select_related_qs)\
            .prefetch_related(*self.prefetch_related_qs)
    
    def get_annotate(self) -> dict[str, object]:
        return self.qs_annotate
    
    def get_queryset(self) -> QuerySet:
        qs = self.get_related_queries()\
                .annotate(**self.get_annotate())
        return qs

class Implementations(
            ImplementReadOnlySerializer, 
            ImplementGenericResponses, 
            GetQuerysetMixin,
        ):
    pass


class RetrieveObjectMixin(
            Implementations
        ):
    # Quizá agregar el decorador del caching?
    def retrieve(self, request, pk:str, *args, **kwargs):
        
        obj:QuerySet = self.get_queryset().filter(pk=pk).first()
        
        if obj is not None:
            serializer = self.get_read_only_serializer(instance=obj)
            data = serializer.data
            return self.get_ok_response(data)
        
        return self.get_not_found_response()

class ListObjectMixin(
            Implementations
        ):
    def list(self, request, *args, **kwargs):
        
        data:QuerySet = self.get_queryset()
        
        # Aplicar los filtros y paginación
        data = self.filter_queryset(data)
        page = self.paginate_queryset(data)
        
        if data.exists():
            if page is not None:
                serialized_data = self.get_read_only_serializer(page, many=True).data
                return self.get_paginated_response(serialized_data)
            
            serialized_data = self.get_read_only_serializer(data, many=True).data
            return self.get_ok_response(data=serialized_data)
        
        return self.get_not_found_response()

class CreateObjectMixin(
            Implementations
        ):
    def create(self, request:HttpRequest, *args, **kwargs):
        
        # data = {
        #     **request.data,
        #     "changed_by": request.user.id,
        # }
        data = request.data
        serializer:ModelSerializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            obj = self.get_read_only_serializer(instance=instance).data
            return self.get_created_response(obj)
        
        return self.get_bad_request(serializer.errors)

class UpdateObjectMixin(
            Implementations
        ):
    def update(self, request:HttpRequest, pk:str,  *args, **kwargs):
        partial:bool = kwargs.get("partial", False)
        instance:Model = self.get_queryset().filter(pk=pk).first()
        
        new_data:dict[str, object] = request.data
        
        serializer:ModelSerializer = self.get_serializer(instance=instance, data=new_data, partial=partial)
        if serializer.is_valid():
            instance = serializer.save()
            data = self.get_read_only_serializer(instance=instance).data
            return self.get_ok_response(data, f"{self.model_name} se ha actualizado exitosamente")
        
        return self.get_bad_request(serializer.errors)

class DestroyObjectMixin(
            Implementations
        ):
    """Mixin Class for the destroy of the instance
    You need to rewrite the methods "get_deleted_status" if you
    want to stablish what data type means that the object is deactivated
    (defaults to False)
    you need to rewrite "get_status_field" if you want to specify
    that field of theinstance represents its active or deactivated status
    (defaults to "is_active" field)
    """
    deleted_status = False
    
    def get_deleted_status(self):
        """Returns the data type that means a object is destroyed or
        deactivated
        
        for example, if you have a instance with 3 types of status
        like the Vale instance (valid, processed, nulled)
        you must override this method to nulled (for example)

        Returns:
            boolean | Any: defaults to False
        """
        return False
    
    def get_status_field(self) -> str:
        """This method returns the field name that represents the 
        status of the instance
        
        for example, the field "status" or the default "is_active" that is default for User model

        Returns:
            str: Defaults to "is_active"
        """
        return "is_active"
    
    def destroy(self, request:HttpRequest, pk:str, *args, **kwargs):
        
        obj:Model = self.get_queryset().filter(pk=pk).first()
        if obj is not None:
            # set the attribute of the status to the deleted value
            setattr(obj, self.get_status_field(), self.get_deleted_status())
            obj.save()
            serialized_data = self.get_read_only_serializer(instance=obj).data
            return self.get_ok_response(
                    serialized_data, 
                    f"El objeto {self.model_name} desactivado correctamente",
                )
        
        return self.get_not_found_response()




