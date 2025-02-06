# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer




# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Todo
from .serializers import TodoSerializer

# views.py

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TodoViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_queryset(self):
        """
        Restrict the queryset to only the todos belonging to the logged-in user.
        """
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the user to the logged-in user when creating a todo.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure the logged-in user can only update their own todos.
        """
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this todo.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensure the logged-in user can only delete their own todos.
        """
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this todo.")
        instance.delete()


