from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from usuarios.models import Usuario


class UsuariosSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        exclude = ("password",)     

class ChangePasswordSerializer(serializers.Serializer):
    model = Usuario

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    email        = serializers.CharField(required=True)

    
class UsuarioRegisterSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id','email', 'nome','is_superuser','is_staff','is_active','password')


    def create(self, validated_data):        
        tb_usuario = Usuario(
            is_superuser=validated_data.get('is_superuser'),
            nome=validated_data.get('nome'),
            is_staff=validated_data.get('is_staff'),
            is_active=validated_data.get('is_active'),
            email=validated_data.get('email')
        )
        tb_usuario.set_password(validated_data['password'])
        tb_usuario.save()
        return tb_usuario