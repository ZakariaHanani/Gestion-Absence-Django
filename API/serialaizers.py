from rest_framework import serializers
from pfe.models import (Student, Attendance)


class StudentRegisterationDataSerializer(serializers.ModelSerializer):
    class Meta(object):
 
        model = Student
        fields = ['id',
                'fname',
                'lname',
                'email',
                'Identifiant_Filiere',
                ]
        
class StudentSignupSerializer(serializers.ModelSerializer):
    class Meta(object):
 
        model = Student
        fields = ['id',
                  'password',
                  'email',
                  'fname',
                  'lname',
                  'Identifiant_Filiere',
                ]


class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta(object):

        model = Student
        fields = [
            'id',
            'password',
         ]

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta(object):

        model = Attendance
        fields = '__all__'
