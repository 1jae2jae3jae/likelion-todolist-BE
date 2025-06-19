from rest_framework.serializers  import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__" #user 클래스에 있는 모든 필드들을 userserializer에 포함시킨다.
        extra_kwargs = {
            'usernaeme': {
                'error_messages': {
                    'reuired': '이 필드는 필수 항목입니다.',
                    'unique': 'user의 username은/는 이미 존재합니다.',
                }
            },
            'password': {
                'error_messages': {
                    'required': '이 필드는 필수 항목입니다.',
                }
            }    
        }
