# views.py
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import *
from rest_framework.viewsets import GenericViewSet
from .models import *
from .serializers import * 
from .permissions import * 

# class PlanViewSet(viewsets.ModelViewSet):
#     serializer_class = PlanSerializer

#     def get_queryset(self):
#         return Plan.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    # permission_classes = [IsCoachOrStaff]

    def get_queryset(self):
        return Exercise.objects.select_related('owner')\
                               .prefetch_related('exercise_detail').filter(owner=self.request.user)
    
    def get_serializer_context(self):
        return {"owner": self.request.user}
    
class PlanViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
    # Get all plan IDs the user is subscribed to
        subscribed_plan_ids = PlanSubscription.objects.filter(
            user=self.request.user
        ).values_list('plan_id', flat=True)

        print("Subscribed Plan IDs:", list(subscribed_plan_ids))
        return Plan.objects.filter(Q(id__in=subscribed_plan_ids) | Q(owner=self.request.user))
    
    serializer_class = PlanSerializer
    # permission_classes = [IsCoachOrStaff]

    def get_serializer_context(self):
        try: plan_id = self.kwargs['pk']
        except: plan_id = None
        return {'user': self.request.user,
                'plan_id': plan_id
                }

class PlanRequestView(viewsets.ModelViewSet):
    serializer_class = PlanRequestSerializer

    def get_queryset(self):
        return PlanRequest.objects.all()
    
    def get_serializer_context(self):
        return {"user": self.request.user}

class SportView(viewsets.ModelViewSet):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer

class MuscleView(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer


class NutritionPlanViewSet(viewsets.ModelViewSet):
    serializer_class = NutritionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optimize queries with prefetch and select
        return NutritionPlan.objects.prefetch_related(
            'meals', 
            'meals__food_items'
        ).select_related('owner').filter(owner=self.request.user)

    def get_serializer_context(self):
        return {"owner": self.request.user}

class PlanSubscriptionView(CreateModelMixin,GenericViewSet):
    queryset = PlanSubscription.objects.select_related('nutritionPlan','plan','user')
    serializer_class = PlanSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"user":self.request.user}