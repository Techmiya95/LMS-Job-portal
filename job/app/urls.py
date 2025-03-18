from django.urls import path
# from .views import check_user # Import the new view function



from .views import toggle_apply_job,update_profile,profile_page,add_skill,remove_skill,add_project,update_project,delete_project,get_project,get_projects
from .views import check_auth, dashbord, index, job_list_view, login_view, logout_view, signup, user_list, hr_list, api_jobs,get_user_profile,loginhr
from .views import hr_signup, hr_login, create_job, update_job, delete_job, get_job_details, update_application_status, contact_applicant, hr_panel_view, delete_job
from .views import get_job_data
urlpatterns = [  
    # path('check_user/', check_user, name='check_user'),  # Add the new URL pattern 
    path('hr/create-job/', create_job, name='create_job'),
    path('hr/update-job/', update_job, name='update_job'),
    path('hr/delete-job/', delete_job, name='delete_job'),
    path('get_job_details/<str:job_id>/', get_job_details, name='get_job_details'),
    path('delete_job/', delete_job, name='delete_job'),
path('get_job_data/<str:job_id>/', get_job_data, name='get_job_data'),
     path('hr_panel/', hr_panel_view, name='hr_panel'),
    
    # Applicant Management
    path('hr/update-application-status/', update_application_status, name='update_application_status'),
    path('hr/contact-applicant/', contact_applicant, name='contact_applicant'),
    path('add_project/', add_project, name='add_project'),
    path('update_project/', update_project, name='update_project'),
    path('delete_project/', delete_project, name='delete_project'),
    path('get_project/', get_project, name='get_project'),
    path('get_projects/', get_projects, name='get_projects'),
    path('hrsignup/', hr_signup, name='hrsignup'),
    path('hrlogin/', hr_login, name='hrlogin'),
    path('loginhr/', loginhr, name='loginhr'),
 path('create-job/', create_job, name='create-job'),
    # path('save_experience/', save_experience, name='save_experience'),
    # path('get_experiences/', get_experiences, name='get_experiences'),
    path('apply/', toggle_apply_job, name='toggle_apply_job'),  
    path('hr_list/', hr_list, name='hr_list'),
    path('api_jobs/', api_jobs, name='api_jobs'),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashbord/', dashbord, name='dashbord'),
    path('job_list/', job_list_view, name='job_list'),
    path('user_list/', user_list, name='user_list'),
    path('update_profile/', update_profile, name='update_profile'),
    path('add_skill/', add_skill, name='add_skill'),  # Add this line
    path('remove_skill/', remove_skill, name='remove_skill'),
    path('profile/',profile_page, name='profile_page'),
    path('toggle_apply_job/', toggle_apply_job, name='toggle_apply_job'),
    path('get_user_profile/', get_user_profile, name='get_user_profile'),
]
