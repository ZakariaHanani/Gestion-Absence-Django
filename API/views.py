from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status 
from django.shortcuts import get_object_or_404
from pfe.models import Attendance, Student
from .serialaizers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

#################################### Sign up functions
def isSigningDataValid(studentData):
    if studentData.is_valid():
        return True
    return False

def getSigninData(studentData, studentToken):
    print(f"Token for student: {studentToken}")
    return Response({'detail' : 'successfully created',
                     'Token' : studentToken,
                     'student' : studentData
                    })
####################################
#################################### Log in functions
def isIdExist(studentID):
    try:
        student = get_object_or_404(Student, id=studentID)
    except:
        return False
    return True

def studentObjectNotFound():
    return Response(data={'detail'  : 'Student with this id not found'}, status=status.HTTP_404_NOT_FOUND)

def getStudentObject(studentID):
    return Student.objects.get(id=studentID)

def isPasswordCorrect(student, studentPassword):
    return student.check_password(studentPassword)

def passwordIncorrectError():
    return Response(data={'detail'  : 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)
    
def getStudentRegisterationData(student):
    serializer = StudentRegisterationDataSerializer(instance=student)
    return serializer.data
    
def getStudentToken(studentID):
    (studentToken, isTokenCreatedForTheStudent) = Token.objects.get_or_create(user_id=studentID)
    return studentToken.key

def getLoginData(studentData, studentToken):
    return Response(data={'detail' : 'successfully loged in',
                    'token' : studentToken,
                    'student' : studentData
                    }, 
                    status=status.HTTP_200_OK
                    )
####################################   
#################################### Attendance functions
from django.http import HttpResponseForbidden

def isValidToken(studentID, authorization_header):
    if not isIdExist(studentID=studentID):
        return False
    expected_token = getStudentToken(studentID=studentID)
    # Splitting the authorization header to extract the token part
    auth_method, token = authorization_header.split(' ', 1) if authorization_header else (None, None)
    if auth_method != 'Token' or token != expected_token:
        return False
    return True
    
def tokenObjectNotFound():
    return Response(data={'detail' : 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
     
def isAttendanceExist(identifiantSeance, studentID):
    try:
        attendance = get_object_or_404(Attendance, Identifiant_Seance=identifiantSeance, Identifiant_Etudiant=studentID)
    except:
        return False
    return True 

def attendanceObjectNotFound():
    return Response(data={'detail' : 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)

def getAttendanceObject(identifiantSeance, studentID):
    return Attendance.objects.get(Identifiant_Seance=identifiantSeance, Identifiant_Etudiant=studentID)

def updateAttendanceStatus(attendance):
    attendance.Status = 'Present(e)'
    attendance.save()
    
def getAttendanceObjectData(attendance):
    return AttendanceSerializer(instance=attendance).data
    
def getSuccessRegistrationData(attendanceData):
    return Response({'detail' : 'registered successfully', 'attendance' : attendanceData}, status=status.HTTP_200_OK)
#################################### 




####################################  
#################################### Sign up API View
@api_view(['POST'])
def signup(request):
    studentData = StudentSignupSerializer(data=request.data).data
    
    if not isSigningDataValid(studentData):
        return Response({'detail' : studentData.errors})
    
    studentData.save()
    
    student = Student.objects.get(id=request.data['id'])
    studentToken = getStudentToken(studentID=student.id)
    
    return getSigninData(studentData=studentData, studentToken=studentToken)

####################################
#################################### Log in API View



@api_view(['POST'])
def login(request):
   
    if not isIdExist(studentID=request.data['id']):
        return studentObjectNotFound()
    
    student = getStudentObject(studentID=request.data['id'])

    if not isPasswordCorrect(student=student, studentPassword=request.data['password']):
        return passwordIncorrectError()
    
    studentData = getStudentRegisterationData(student=student)
    studentToken = getStudentToken(studentID=student.id)
    print(f"Token for student  {studentToken}")
    
    return getLoginData(studentData=studentData, studentToken=studentToken)

####################################    
#################################### Update Status API View
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateview(request):
    from pfe.models import Seance, Attendance
    from datetime import datetime

    add_client = getIpAdressclient(request)
    add_machine = getIpAdressMachine()


    identifiantSeance = request.data.get('Identifiant_Seance')
    studentID = request.data.get('Identifiant_Etudiant')
    auth_header = request.headers.get('Authorization', 'No Token Provided')

    seance = Seance.objects.get(Identifiant_Seance=identifiantSeance)
    attendance = Attendance.objects.get(Identifiant_Seance=identifiantSeance, Identifiant_Etudiant=studentID)
    date = seance.DateSeance
    heure = seance.HeureDebut
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    print("----------------")
    result = verifiedate("2024-03-10", "13:11:23", "2024-03-10 13:07:00")
    print(f"Result: {result}")



    try:
        attendance = Attendance.objects.get(Identifiant_Seance=identifiantSeance, Identifiant_Etudiant=studentID)
    except Attendance.DoesNotExist:
        return Response({'detail': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)

    if en_reseau(add_client, add_machine, "255.255.255.0"):
        if verifiedate(date, heure, formatted_time):
            attendance.Status = 'Present(e)'
            attendance.save()

            # Serialize the updated attendance object
            attendance_data = AttendanceSerializer(attendance).data

            return Response({'detail': 'registered successfully', 'attendance': attendance_data}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': "la session est  terminée, vous avez été enregistré(e)  absent, contacter l'administration"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'detail': "Vous n'êtes pas dans la classe, votre attendance n'est enregistrée"}, status=status.HTTP_400_BAD_REQUEST)

def getIpAdressclient(request):
    client_ip = request.META.get('REMOTE_ADDR')
    print("Client's IP Address:", client_ip)
    return client_ip

def getIpAdressMachine():
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"machine {ip_address}")
    return ip_address

def en_reseau(add1, add2, mask):
    import ipaddress
    reseau1 = ipaddress.ip_interface(f"{add1}/{mask}")
    reseau2 = ipaddress.ip_interface(f"{add2}/{mask}")
    if reseau1.network == reseau2.network:
        return True
    else:
        return False


def verifiedate(date, heure, formatted_time):
    from datetime import datetime, timedelta
    formatted_time2 = f"{date} {heure}"
    time2 = datetime.strptime(formatted_time2, '%Y-%m-%d %H:%M:%S')
    time1 = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
    time_difference = time1 - time2
    if timedelta(hours=0) <= time_difference <= timedelta(hours=2):
        return True
    else:
        return False





