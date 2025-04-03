from django.urls import path
# from .views import check_user # Import the new view function



from .views import toggle_apply_job,update_profile,profile_page,add_skill,remove_skill,add_project,update_project,delete_project,get_projects,get_locations
from .views import check_auth, dashbord, index, job_list_view, login_view, logout_view, signup, user_list, hr_list, api_jobs,get_user_profile,loginhr,get_skills
from .views import hr_signup, hr_login, create_job, update_job, delete_job, get_job_details, hr_panel_view, delete_job, get_api_keys, get_api_keys_message
from .views import get_job_data, get_applicant_details, contact_applicant,hr_userlist,get_user_details,store_jobs,upload_resume,get_resume,download_resume,search_locations
# from .views import save_experience
from .views import get_experiences, add_experience, update_experience, delete_experience,get_jobs
urlpatterns = [  
    # path('check_user/', check_user, name='check_user'),  # Add the new URL pattern 
    path('get-jobs/',get_jobs, name='get_jobs'),
    path('hr/create-job/', create_job, name='create_job'),
    path('hr/update-job/', update_job, name='update_job'),
    path('hr/delete-job/', delete_job, name='delete_job'),
    path('get_job_details/<str:job_id>/', get_job_details, name='get_job_details'),
    path('delete_job/', delete_job, name='delete_job'),
path('get_job_data/<str:job_id>/', get_job_data, name='get_job_data'),
     path('hr_panel/', hr_panel_view, name='hr_panel'),
    path('get_user_details/<str:user_id>/', get_user_details, name='get_user_details'),
    path('hr_userlist/', hr_userlist, name='hr_userlist'),
     path('download_resume/<int:user_id>/', download_resume, name='download_resume'),
    path('upload_resume/', upload_resume, name='upload_resume'),
    path('get_resume/', get_resume, name='get_resume'),
    path('download_resume/', download_resume, name='download_resume'),
    path('get_skills/', get_skills, name='get_skills'),
    # ... your other URLs ...
    path("get-api-keys/", get_api_keys, name="get_api_keys"),
    path("get_api_keys_message/", get_api_keys_message, name="get_api_keys_message"),    
    # Applicant Management
     path('store-jobs/', store_jobs, name='store_jobs'),
   path('get_projects/', get_projects, name='get_projects'),
    path('add_project/', add_project, name='add_project'),
    path('update_project/', update_project, name='update_project'),
    path('delete_project/', delete_project, name='delete_project'),
    path('hrsignup/', hr_signup, name='hrsignup'),
    path('hrlogin/', hr_login, name='hrlogin'),
    path('loginhr/', loginhr, name='loginhr'),
 path('create-job/', create_job, name='create-job'),
 path('get_locations/', get_locations, name='get_locations'),
 path('search_locations/', search_locations, name='search_locations'),
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
     path('get_applicant_details/<str:user_id>/', get_applicant_details, name='get_applicant_details'),
    path('contact_applicant/', contact_applicant, name='contact_applicant'),
     path('get_experiences/', get_experiences, name='get_experiences'),
    path('add_experience/', add_experience, name='add_experience'),
    path('update_experience/', update_experience, name='update_experience'),
    path('delete_experience/', delete_experience, name='delete_experience'),
]
