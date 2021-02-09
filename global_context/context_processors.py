import datetime
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from session_semester.models import SessionAndSemester

def global_variables(request):
    now = datetime.datetime.now()
    current_year = now.strftime('%Y')
    hour = now.hour
    greeting = None
    if int(hour) in range(0,12):
        greeting = "Good Morning "
    elif int(hour) in range(12,17):
        greeting = "Good Afternoon "
    elif int(hour) in range(17,24):
        greeting = "Good Evening "
    short_name = ''
    user_profile = None
    if request.user.is_authenticated:
        short_name = request.user.get_short_name()
        user = User.objects.get(id=request.user.id)
        try: 
            user_profile = UserProfile.objects.get(user=user)
        except:
            user_profile = None
    
    session__semester = SessionAndSemester.objects.get(id=1)

    return {
        'current_year': current_year,
        "short_name": short_name,
        'user_profile': user_profile,
        'greeting': greeting,
        'current_session': session__semester.get_session_display,
        'current_semester': session__semester.get_semester_display,
    }