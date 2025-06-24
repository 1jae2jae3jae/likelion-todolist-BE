from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from .models import Todo, User
from .serializers import TodoSerializer
from rest_framework import status

# Create your views here.
class Todos(APIView):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    #투두리스트 조회
    def get(self, request, user_id):
        # 유저 가져오기
        user = self.get_user(user_id)

        # 기본적으로 전체 Todo 리스트 조회
        todos = Todo.objects.filter(user=user)

        # 쿼리 파라미터에서 month, day 가져오기
        month = request.query_params.get('month')
        day = request.query_params.get('day')

        # month, day가 둘 다 제공된 경우만 필터링
        if month is not None and day is not None:
            try:
                month = int(month)
                day = int(day)
                todos = todos.filter(date__month=month, date__day=day)
            except ValueError:
                raise ParseError("month와 day는 정수여야 합니다.")
            
        #정렬 및 추가 필터링을 위한 sort_by 파라미터 가져오기
        sort_by = request.query_params.get('sort_by', 'created_at')
        if sort_by not in ['created_at', 'updated_at']:
            sort_by = 'created_at'

        # 직렬화
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    #투두리스트 생성
    def post(self, request, user_id):
        # 유저 가져오기
        user = self.get_user(user_id)

        # 직렬화
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            todo = serializer.save(user=user)
            return Response(TodoSerializer(todo).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TodoDetail(APIView):
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("유저를 찾을 수 없습니다.")
        return user
    
    def get_todo(self, user, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id, user=user)
        except Todo.DoesNotExist:
            raise NotFound("To Do를 찾을 수 없습니다.")
        return todo
    
    # 투두 조회
    def get(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
     # 투두 수정
    def patch(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        
        # content만 업데이트 허용
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=False)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 투두 삭제
    def delete(self, request, user_id, todo_id):
        user = self.get_user(user_id)
        todo = self.get_todo(user, todo_id)
        todo.delete()
        return Response({"detail": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)