def user_list(request):
    users = list(auth_user_collection.find({}))  # Fetch users
    print(f"Fetched Users: {users}")  # Debugging line to check fetched users
    user_id = "19"  # Check for user with ID 19
    user_data = auth_user_collection.find_one({"_id": user_id})
    print(f"User Data for ID {user_id}: {user_data}")  # Debugging line to check specific user data
    social_auths = list(social_auth_collection.find({}))  # Fetch social auth users
    
    return render(request, 'user_list.html', {'users': users, 'social_auths': social_auths})
from django.shortcuts import render
from pymongo import MongoClient
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime


# Other views (e.g., job_list_view, signup, login_view, etc.) remain unchanged
# Connect to MongoDB Atlas (First Database)
MONGO_URI = "mongodb+srv://pavan:database@atlas.eokhe.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["test_mongo"]

# Connect to MongoDB Atlas (Second Database)
MONGO_URI1 = "mongodb+srv://pavankumar9686323614:job@job-portal.m1m85.mongodb.net/"
client1 = MongoClient(MONGO_URI1)
db1 = client1["test_mongo"]

# Collections
Experience = db1["Experience"]
hr_collection = db1["authhr"]
auth_user_collection = db["auth_user"]
social_auth_collection = db["social_auth_usersocialauth"]
job_collection = db1["Joblist"]  # Renamed to avoid conflict
job_applied_collection = db1["JobApplied"]  # Renamed to avoid conflict
skills_collection = db["skills"]  # Renamed to avoid conflict
location_collection=db["location"]
jobrole_collection=db["jobrole"]

def user_list(request):
    users = list(auth_user_collection.find({}))  # Fetch users
    social_auths = list(social_auth_collection.find({}))  # Fetch social auth users
    
    return render(request, 'user_list.html', {'users': users, 'social_auths': social_auths})

def api_jobs(request):
    return render(request, 'Api_job.html')


@login_required
def job_list_view(request):
    # Handle AJAX requests for job role and location suggestions
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'term' in request.GET:
        search_term = request.GET.get('term', '').lower()
        field = request.GET.get('field', '')
        
        if field == 'job_role':
            # Get job roles from the array field
            roles_doc = jobrole_collection.find_one({}, {"job_roles": 1})
            job_roles = roles_doc.get('job_roles', []) if roles_doc else []
            suggestions = [role for role in job_roles if role and search_term in role.lower()][:10]
            return JsonResponse(suggestions, safe=False)
        elif field == 'location':
            # Get locations from the array field
            locs_doc = location_collection.find_one({}, {"locations": 1})
            locations = locs_doc.get('locations', []) if locs_doc else []
            suggestions = [loc for loc in locations if loc and search_term in loc.lower()][:10]
            return JsonResponse(suggestions, safe=False)

    # Get current date in the same format as deadline (YYYY-MM-DD)
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Fetch only jobs where deadline is greater than or equal to current date
    jobs = list(job_collection.find({
        "deadline": {"$gte": current_date}
    }).sort("posted_date", -1))
    
    for job in jobs:
        job['jid'] = str(job['_id'])  # Ensure consistent string format

    # Get user data
    user_data = None
    user_mongo_id = None
    if request.user.is_authenticated:
        user_data = auth_user_collection.find_one({"id": request.user.id})
        if user_data:
            user_mongo_id = str(user_data['_id'])

    # Prepare user profile data
    data = {
        "father_name": user_data.get("father_name", "N/A") if user_data else "N/A",
        "branch": user_data.get("branch", "N/A") if user_data else "N/A",
        "Passout_Year": user_data.get("Passout_Year", "N/A") if user_data else "N/A",
        "Graduation_Percentage": user_data.get("Graduation_Percentage", "N/A") if user_data else "N/A",
        "Percentage_10": user_data.get("10th_Percentage", "N/A") if user_data else "N/A",
    }

    # Convert skills to list
    for job in jobs:
        if 'Skills' in job and isinstance(job['Skills'], str):
            job['Skills'] = [skill.strip() for skill in job['Skills'].split(',')]

    # Get applied jobs
    applied_jobs = set()
    if user_mongo_id:
        applications = job_applied_collection.find({"user_id": user_mongo_id})
        applied_jobs = {str(app['job_id']) for app in applications}

    # Get job roles and locations from their respective collections
    roles_doc = jobrole_collection.find_one({}, {"job_roles": 1})
    job_roles = roles_doc.get('job_roles', []) if roles_doc else []
    
    locs_doc = location_collection.find_one({}, {"locations": 1})
    locations = locs_doc.get('locations', []) if locs_doc else []

    return render(request, 'job_list.html', {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
        'user': request.user,
        'data': [data],
        'job_roles': sorted(job_roles, key=lambda x: x.lower()),
        'locations': sorted(locations, key=lambda x: x.lower()),
    })








def hr_list(request):
 return render(request, 'hr.html')

def index(request):
    return render(request, 'authunticate.html')

def add_person(request):
    person = Person(name="Doe", age=30)
    person.save()
    return HttpResponse("<h1>Person added successfully</h1>")

def get_person(request):
    person = Person.objects.first() # Get first person
    return HttpResponse(f"<h1>Name: {person.name}, Age: {person.age}</h1>")

def check_auth(request):
    if request.user.is_authunticated:
        return HttpResponse(f"<h1>User is authenticated</h1>")
    return HttpResponse(f"<h1>User is not authenticated</h1>")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        # Check if email or username already exists
        if User.objects.filter(email=email).count() > 0:
            return render(request, "authunticate.html", {
                "error_message": "Email already exists"
            })
        if User.objects.filter(username=username).count() > 0:
            return render(request, "authunticate.html", {
                "error_message": "User already exists"
            })

        # Create user with hashed password
        user = User(username=username, email=email, password=make_password(password))
        user.save()
        
        return redirect('/')  # Redirect to login or home page

    return redirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log in the user
            return redirect('job_list')  # Redirect to dashboard

        return render(request, "authunticate.html", {"error_message": "Invalid credentials"})

    return redirect('/')


def loginhr(request):
    return render(request, 'authhr.html')



# hr authentication
def hr_signup(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        email = request.POST['email']
        hrname = request.POST['hrname']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            return render(request, "authhr.html", {"error_message": "Passwords do not match"})
        
        if hr_collection.find_one({"email": email}) or hr_collection.find_one({"hrname": hrname}):
            return render(request, "authhr.html", {"error_message": "HR already exists"})
        
        hashed_password = make_password(password)
        hr_data = {
            "hrname": hrname,
            "email": email,
            "password": hashed_password,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }
        hr_collection.insert_one(hr_data)
        return redirect('loginhr')
    return redirect('/')


def hr_login(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()  # Accepts hrname or email
        password = request.POST.get("password", "").strip()

        print("Received data:", request.POST)  # Debugging

        if not identifier or not password:
            return render(request, "authhr.html", {"error_message": "Both fields are required"})

        hr = hr_collection.find_one({"$or": [{"hrname": identifier}, {"email": identifier}]})

        if hr:
            print("Found HR:", hr)  # Debugging

            if check_password(password, hr["password"]):
                # Store HR information in the session
                request.session["hr_username"] = hr["hrname"]
                request.session["hr_id"] = str(hr["_id"])

                # Redirect to HR dashboard without using Django's auth system
                return redirect("hr_panel")
            else:
                print("Password mismatch")  # Debugging
        else:
            print("HR not found")  # Debugging

        return redirect('loginhr')

    return redirect('loginhr')  # Show login page if GET request



@login_required(login_url='/')
def dashbord(request):
    print("hiii")
    # return render(request, 'job_list.html',{"user": request.user})

from django.shortcuts import redirect

def logout_view(request):
    if request.user.is_authenticated:  # Optional check
        request.session.flush()  # Clears all session data
    return redirect('login')  # Redirects to login page


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime


@csrf_exempt
@login_required
def toggle_apply_job(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    
    try:
        job_id = request.POST.get("job_id", "").strip()
        hr_id = request.POST.get("hr_id", "").strip()
        
        # Get user's MongoDB _id
        user = auth_user_collection.find_one({"id": request.user.id})
        if not user:
            return JsonResponse({"error": "User not found"}, status=400)
        user_id = str(user["_id"])
        
        # Validate IDs
        if not job_id or not hr_id:
            return JsonResponse({"error": "Missing IDs"}, status=400)
        
        # Check existing application
        existing = job_applied_collection.find_one({
            "user_id": user_id,
            "job_id": job_id
        })
        
        if existing:
            # Unapply
            job_applied_collection.delete_one({"_id": existing["_id"]})
            return JsonResponse({"status": "unapplied"})
        else:
            # Apply
            job_applied_collection.insert_one({
                "user_id": user_id,
                "job_id": job_id,
                "hr_id": hr_id,
                "applied_at": datetime.datetime.now()
            })
            return JsonResponse({"status": "applied"})
            
    except Exception as e:
        print(f"Error in toggle_apply_job: {str(e)}")
        return JsonResponse({"error": "Server error"}, status=500)
        # profile side bar logic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_user_profile(request):
    user = request.user
    user_data = auth_user_collection .find_one({"id": request.user.id})
    user_name = user_data.get("username", "N/A")
    ug_college = user_data.get("ug_college", "N/A")
    email = user_data.get("email", "N/A")
    father_name = user_data.get("father_name", "N/A")
    progress = user_data.get("progress", "N/A")
    branch = user_data.get("branch", "N/A")
    Passout_Year = user_data.get("Passout_Year", "N/A")
    Graduation_Percentage = user_data.get("Graduation_Percentage", "N/A")
    Percentage_10 = user_data.get("10th_Percentage", "N/A")
    profile_picture = user_data.get("profile_picture", None)
    mobile = user_data.get("mobile", "N/A")
    location = user_data.get("location", "N/A")
    tenth_school = user_data.get("10th_school", "N/A")
    tenth_board = user_data.get("10th_board", "N/A")
    tenth_passout_year = user_data.get("10th_passout_year", "N/A")
    twelfth_school = user_data.get("12th_school", "N/A")
    twelfth_board = user_data.get("12th_board", "N/A")
    twelfth_passout_year = user_data.get("12th_passout_year", "N/A")
    twelfth_percentage = user_data.get("12th_Percentage", "N/A")
    skills = user_data.get("skills", [])  # Fetch skills from user document
  
    data = [{
    # "father_name": father_name,
    "profile_picture": profile_picture,
    "email": email,
    "father_name": father_name,
    "progress": progress,
    "branch": branch,
    "ug_college": ug_college,
    "user_name": user_name,
    "Passout_Year": Passout_Year,
    "Graduation_Percentage": Graduation_Percentage,
    "Percentage_10": Percentage_10,
    "mobile": mobile,
    "location": location,
    "tenth_school": tenth_school,
    "tenth_board": tenth_board,
    "tenth_year": tenth_passout_year,
    "twelfth_school": twelfth_school,
    "twelfth_board": twelfth_board,
    "twelfth_year": twelfth_passout_year,
    "twelfth_percentage": twelfth_percentage,
    "skills": skills,  # Include skills in the response 
       
    }]
    return JsonResponse({"success": True, "data": data})
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from pymongo import MongoClient


# @csrf_exempt
# @require_POST
# def update_profile(request):
#     try:
#         user = request.user  
#         if not user.is_authenticated:  
#             return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

#         # Check if request is multipart/form-data (for file upload)
#         if request.content_type.startswith('multipart/form-data'):
#             data = request.POST.dict()  # Convert form data to dict
#             profile_picture = request.FILES.get("profile_picture")  # Get uploaded file
#         else:
#             try:
#                 data = json.loads(request.body.decode("utf-8"))
#                 profile_picture = None
#             except json.JSONDecodeError:
#                 return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

#         print(f"Received data: {data}")  # Debugging

#         # Fetch user data from MongoDB
#         user_data = auth_user_collection.find_one({"username": user.username})

#         if not user_data:
#             return JsonResponse({"status": "error", "message": "User profile not found"}, status=404)

#         # Field mappings
#         field_mappings = {
#             "name": "username",
#             "email": "email",
#             "father_name": "father_name",
#             "ug_college": "ug_college",
#             "branch": "branch",
#             "passout_year": "Passout_Year",
#             "graduation_percentage": "Graduation_Percentage",
#             "tenth_percentage": "10th_Percentage",
#             "twelfth_percentage": "12th_Percentage",
#         }

#         update_data = {}
#         for frontend_field, db_field in field_mappings.items():
#             new_value = data.get(frontend_field, "").strip()
#             old_value = str(user_data.get(db_field, "")).strip()

#             if new_value and new_value != old_value:
#                 update_data[db_field] = new_value

#         # **Handle profile picture upload**
#         if profile_picture:
#             image_data = profile_picture.read()  # Read the image file
#             encoded_image = base64.b64encode(image_data).decode("utf-8")  # Convert to Base64
#             update_data["profile_picture"] = encoded_image  # Store in MongoDB

#         # print(f"Changes detected: {update_data}")  # Debugging

#         if not update_data:
#             return JsonResponse({"status": "success", "message": "No changes detected."})

#         # Update user profile in MongoDB
#         result = auth_user_collection.update_one(
#             {"username": user.username},
#             {"$set": update_data}
#         )

#         print(f"Update result: {result.modified_count} document(s) modified.")  # Debugging

#         return JsonResponse({"status": "success", "message": "Profile updated successfully!"})

#     except Exception as e:
#         print(f"Error updating profile: {e}")  # Debugging
#         return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
#     from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import ObjectId
from datetime import datetime

@csrf_exempt
def get_experiences(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        user_data = auth_user_collection.find_one({"username": user.username})
        if not user_data:
            return JsonResponse({"success": False, "error": "User not found"}, status=404)

        experiences = user_data.get("experiences", [])
        
        # Convert ObjectId to string for JSON serialization
        for exp in experiences:
            if '_id' in exp:
                exp['_id'] = str(exp['_id'])
                
        return JsonResponse({"success": True, "data": experiences})
        
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def add_experience(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['company_name', 'job_title', 'start_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({"success": False, "error": f"Missing required field: {field}"}, status=400)

        experience_data = {
            "_id": ObjectId(),  # Generate new ObjectId
            "company_name": data['company_name'],
            "job_title": data['job_title'],
            "start_date": data['start_date'],
            "end_date": data.get('end_date'),
            "currently_working": data.get('currently_working', False),
            "description": data.get('description', '')
        }

        # Update MongoDB
        result = auth_user_collection.update_one(
            {"username": user.username},
            {"$push": {"experiences": experience_data}}
        )

        if result.modified_count == 1:
            return JsonResponse({"success": True, "experience_id": str(experience_data['_id'])})
        else:
            return JsonResponse({"success": False, "error": "Failed to add experience"}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def update_experience(request):
    if request.method != 'PUT':
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        data = json.loads(request.body)
        
        if not data.get('experience_id'):
            return JsonResponse({"success": False, "error": "Missing experience_id"}, status=400)

        # Validate required fields
        required_fields = ['company_name', 'job_title', 'start_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({"success": False, "error": f"Missing required field: {field}"}, status=400)

        update_data = {
            "experiences.$.company_name": data['company_name'],
            "experiences.$.job_title": data['job_title'],
            "experiences.$.start_date": data['start_date'],
            "experiences.$.end_date": data.get('end_date'),
            "experiences.$.currently_working": data.get('currently_working', False),
            "experiences.$.description": data.get('description', '')
        }

        # Update MongoDB
        result = auth_user_collection.update_one(
            {"username": user.username, "experiences._id": ObjectId(data['experience_id'])},
            {"$set": update_data}
        )

        if result.modified_count == 1:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Experience not found or not modified"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def delete_experience(request):
    if request.method != 'DELETE':
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        data = json.loads(request.body)
        
        if not data.get('experience_id'):
            return JsonResponse({"success": False, "error": "Missing experience_id"}, status=400)

        # Update MongoDB
        result = auth_user_collection.update_one(
            {"username": user.username},
            {"$pull": {"experiences": {"_id": ObjectId(data['experience_id'])}}}
        )

        if result.modified_count == 1:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Experience not found or not deleted"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
    
    from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import ObjectId
from datetime import datetime

@csrf_exempt
def get_projects(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        user_data = auth_user_collection.find_one({"username": user.username})
        if not user_data:
            return JsonResponse({"success": False, "error": "User not found"}, status=404)

        projects = user_data.get("projects", [])
        
        # Convert ObjectId to string for JSON serialization
        for proj in projects:
            if '_id' in proj:
                proj['_id'] = str(proj['_id'])
                
        return JsonResponse({"success": True, "data": projects})
        
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def add_project(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['title', 'start_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({"success": False, "error": f"Missing required field: {field}"}, status=400)

        project_data = {
            "_id": ObjectId(),  # Generate new ObjectId
            "title": data['title'],
            "start_date": data['start_date'],
            "end_date": data.get('end_date'),
            "currently_ongoing": data.get('currently_ongoing', False),
            "description": data.get('description', ''),
            "link": data.get('link', '')
        }

        # Update MongoDB
        result = auth_user_collection.update_one(
            {"username": user.username},
            {"$push": {"projects": project_data}}
        )

        if result.modified_count == 1:
            return JsonResponse({"success": True, "project_id": str(project_data['_id'])})
        else:
            return JsonResponse({"success": False, "error": "Failed to add project"}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def update_project(request):
    if request.method != 'PUT':
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        data = json.loads(request.body)
        
        if not data.get('project_id'):
            return JsonResponse({"success": False, "error": "Missing project_id"}, status=400)

        # Validate required fields
        required_fields = ['title', 'start_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({"success": False, "error": f"Missing required field: {field}"}, status=400)

        update_data = {
            "projects.$.title": data['title'],
            "projects.$.start_date": data['start_date'],
            "projects.$.end_date": data.get('end_date'),
            "projects.$.currently_ongoing": data.get('currently_ongoing', False),
            "projects.$.description": data.get('description', ''),
            "projects.$.link": data.get('link', '')
        }

        # Update MongoDB
        result = auth_user_collection.update_one(
            {"username": user.username, "projects._id": ObjectId(data['project_id'])},
            {"$set": update_data}
        )

        if result.modified_count == 1:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Project not found or not modified"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def delete_project(request):
    if request.method != 'DELETE':
        return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

        data = json.loads(request.body)
        
        if not data.get('project_id'):
            return JsonResponse({"success": False, "error": "Missing project_id"}, status=400)

        # Update MongoDB
        result = auth_user_collection.update_one(
            {"username": user.username},
            {"$pull": {"projects": {"_id": ObjectId(data['project_id'])}}}
        )

        if result.modified_count == 1:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Project not found or not deleted"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
@csrf_exempt
@require_POST
def update_profile(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

        # Check if request is multipart/form-data (for file upload)
        if request.content_type.startswith('multipart/form-data'):
            data = request.POST.dict()  # Convert form data to dict
            profile_picture = request.FILES.get("profile_picture")  # Get uploaded file
        else:
            try:
                data = json.loads(request.body.decode("utf-8"))
                profile_picture = None
            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

        # print(f"Received data: {data}")  # Debugging

        # Fetch user data from MongoDB
        user_data = auth_user_collection.find_one({"username": user.username})

        if not user_data:
            return JsonResponse({"status": "error", "message": "User profile not found"}, status=404)

        # Field mappings for personal information
        field_mappings = {
            "username": "username",  # Match the name attribute in the form
            "email": "email",  # Match the name attribute in the form
            "father_name": "father_name",  # Match the name attribute in the form
            "mobile": "mobile",  # Match the name attribute in the form
            "location": "location",  # Match the name attribute in the form
            "tenth_school": "10th_school",  # Match the name attribute in the form
            "tenth_board": "10th_board",  # Match the name attribute in the form  
            "tenth_year": "10th_passout_year",  # Match the name attribute in the form
            "tenth_percentage": "10th_Percentage",  # Match the name attribute in the form
            "twelfth_school": "12th_school",  # Match the name attribute in the form
            "twelfth_board": "12th_board",  # Match the name attribute in the form
            "twelfth_year": "12th_passout_year",  # Match the name attribute in
            "twelfth_percentage": "12th_Percentage",  # Match the name attribute in the form
            "ug_college": "ug_college",  # Match the name attribute in the form
            "branch": "branch",  # Match the name attribute in the form
            "passout_year": "Passout_Year",  # Match the name attribute in the form
            "graduation_percentage": "Graduation_Percentage",  # Match the name attribute in the form
            
            
            
        }

        update_data = {}
        for frontend_field, db_field in field_mappings.items():
            new_value = data.get(frontend_field, "").strip()
            old_value = str(user_data.get(db_field, "")).strip()

            if new_value and new_value != old_value:
                update_data[db_field] = new_value

        # Handle profile picture upload
        if profile_picture:
            image_data = profile_picture.read()  # Read the image file
            encoded_image = base64.b64encode(image_data).decode("utf-8")  # Convert to Base64
            update_data["profile_picture"] = encoded_image  # Store in MongoDB

        # print(f"Changes detected: {update_data}")  # Debugging

        if not update_data:
            return JsonResponse({"status": "success", "message": "No changes detected."})

        # Update user profile in MongoDB
        result = auth_user_collection.update_one(
            {"username": user.username},
            {"$set": update_data}
        )

        # print(f"Update result: {result.modified_count} document(s) modified.")  # Debugging

        return JsonResponse({"status": "success", "message": "Profile updated successfully!"})

    except Exception as e:
        print(f"Error updating profile: {e}")  # Debugging
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
@login_required
def profile_page(request):
    """
    View to render the profile page HTML
    """
    return render(request, 'profile.html')



import os
import json
from datetime import datetime as dt  # Changed import to avoid conflict
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Path to store resumes
RESUME_DIR = os.path.join(settings.MEDIA_ROOT, 'resumes')
RESUME_INFO_FILE = os.path.join(RESUME_DIR, 'resume_info.json')

def ensure_resume_dir():
    """Ensure the resume directory exists"""
    if not os.path.exists(RESUME_DIR):
        os.makedirs(RESUME_DIR)

def get_user_resume_filename(user_id):
    """Get the filename for a user's resume"""
    return f"resume_{user_id}.pdf"

def save_resume_info(user_id, filename, file_size):
    """Save resume metadata to a JSON file"""
    ensure_resume_dir()
    info = {}
    
    if os.path.exists(RESUME_INFO_FILE):
        with open(RESUME_INFO_FILE, 'r') as f:
            try:
                info = json.load(f)
            except json.JSONDecodeError:
                info = {}
    
    info[str(user_id)] = {
        'filename': filename,
        'file_size': file_size,
        'updated_at': dt.now().isoformat()  # Using dt instead of datetime
    }
    
    with open(RESUME_INFO_FILE, 'w') as f:
        json.dump(info, f, indent=4)

def get_resume_info(user_id):
    """Get resume metadata from JSON file"""
    if not os.path.exists(RESUME_INFO_FILE):
        return None
    
    with open(RESUME_INFO_FILE, 'r') as f:
        try:
            info = json.load(f)
            return info.get(str(user_id))
        except json.JSONDecodeError:
            return None

def delete_resume_file(user_id):
    """Delete a user's resume file"""
    filename = get_user_resume_filename(user_id)
    filepath = os.path.join(RESUME_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Not authenticated'}, status=401)
        
        resume_file = request.FILES['resume']
        user_id = request.user.id
        
        # Delete old resume if exists
        delete_resume_file(user_id)
        
        # Save new resume
        ensure_resume_dir()
        filename = get_user_resume_filename(user_id)
        filepath = os.path.join(RESUME_DIR, filename)
        
        with open(filepath, 'wb+') as destination:
            for chunk in resume_file.chunks():
                destination.write(chunk)
        
        # Save metadata
        save_resume_info(user_id, resume_file.name, resume_file.size)
        
        return JsonResponse({
            'success': True,
            'resume': {
                'filename': resume_file.name,
                'updated_at': dt.now().isoformat()  # Using dt instead of datetime
            }
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def get_resume(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Not authenticated'}, status=401)
    
    resume_info = get_resume_info(request.user.id)
    if resume_info:
        return JsonResponse({
            'success': True,
            'resume': {
                'filename': resume_info['filename'],
                'updated_at': resume_info['updated_at']
            }
        })
    return JsonResponse({'success': True, 'resume': None})

def download_resume(request):
    if not request.user.is_authenticated:
        return HttpResponse('Not authenticated', status=401)
    
    resume_info = get_resume_info(request.user.id)
    if not resume_info:
        return HttpResponse('Resume not found', status=404)
    
    filename = get_user_resume_filename(request.user.id)
    filepath = os.path.join(RESUME_DIR, filename)
    
    if os.path.exists(filepath):
        response = FileResponse(open(filepath, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{resume_info["filename"]}"'
        return response
    return HttpResponse('File not found', status=404)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_skill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        skill = data.get('skill')
        user = request.user
        auth_user_collection.update_one(
            {"id": user.id},
            {"$push": {"skills": skill}}
        )
        return JsonResponse({"success": True, "skill": skill})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@csrf_exempt
def remove_skill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        skill = data.get('skill')
        user = request.user
        auth_user_collection.update_one(
            {"id": user.id},
            {"$pull": {"skills": skill}}
        )
        return JsonResponse({"success": True, "skill": skill})
    return JsonResponse({"success": False, "error": "Invalid request method"})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from bson import ObjectId
# def get_projects(request):
#     user_id = request.GET.get('user_id')
#     print(f"Fetching projects for user_id: {user_id}")  # Debugging
#     projects = list(Experience.find({"user_id": user_id}))
#     print(f"Projects found: {projects}")  # Debugging
#     for project in projects:
#         project['_id'] = str(project['_id'])
#     return JsonResponse({"success": True, "data": projects})


    
    # views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from bson.objectid import ObjectId
import json
from datetime import datetime

# Create your HR dashboard view




# @login_required
# def hr_dashboard(request):
#     if not request.session.get('hr_id'):
#         messages.error(request, "You need to log in as an HR to access this page.")
#         return redirect('hr_login')
    
#     hr_id = request.session.get('hr_id')
#     print(f"HR ID: {hr_id}")
    
#     # Fetch jobs created by the current HR
#     hr_jobs = list(job_collection.find({"hr_id": hr_id}))
#     print(hr_jobs)
    
#     # Convert ObjectId to string for each job
#     for job in hr_jobs:
#         job['_id'] = str(job['_id'])
        
#         # Convert Skills to list if it's a string
#         if 'Skills' in job and isinstance(job['Skills'], str):
#             job['Skills'] = [skill.strip() for skill in job['Skills'].split(',')]
        
#         # Count applicants for each job
#         job['applicants_count'] = job_applied_collection.count_documents({"job_id": str(job['_id'])})
    
#     # Fetch job applications for jobs created by this HR
#     job_ids = [job['_id'] for job in hr_jobs]
#     applications = list(job_applied_collection.find({"job_id": {"$in": job_ids}}))
    
#     job_applications = []
#     for app in applications:
#         # Get job details
#         job = job_collection.find_one({"_id": ObjectId(app['job_id'])})
        
#         if job:
#             # Get user details
#             user_details = auth_user_collection.find_one({"id": int(app['user_id'])})
#             user = User.objects.get(id=int(app['user_id']))
            
#             # Format user data
#             user_data = {
#                 "father_name": user_details.get("father_name", "N/A"),
#                 "progress": user_details.get("progress", "N/A"),
#                 "branch": user_details.get("branch", "N/A"),
#                 "Passout_Year": user_details.get("Passout_Year", "N/A"),
#                 "Graduation_Percentage": user_details.get("Graduation_Percentage", "N/A"),
#                 "Percentage_10": user_details.get("10th_Percentage", "N/A"),
#                 "Percentage_12": user_details.get("12th_Percentage", "N/A")
#             }
            
#             job_applications.append({
#                 "id": str(app['_id']),
#                 "job_id": app['job_id'],
#                 "job_title": job.get('title', 'Unknown Position'),
#                 "user_id": app['user_id'],
#                 "user": user,
#                 "user_data": user_data,
#                 "applied_date": app.get('applied_date', datetime.now()),
#                 "status": app.get('status', 'pending')
#             })
    
#     return render(request, 'hr.html', {
#         'hr_jobs': hr_jobs,
#         'job_applications': job_applications
#     })
    
    
    

# Create a new job
@login_required
def create_job(request):
    if request.method == 'POST':
        hr_id = request.session.get('hr_id')
        if not hr_id:
            messages.error(request, "You need to be logged in as an HR to create jobs.")
            return redirect('hr_login')
        
        # Get form data
        job_data = {
            'Job': request.POST.get('title'),
            'Org': request.POST.get('company'),
            'Location': request.POST.get('location'),
            'Salary': request.POST.get('salary'),
            'job_type': request.POST.get('job_type'),
            'experience': request.POST.get('experience'),
            'Skills': request.POST.get('Skills'),
            'FullDescription': request.POST.get('description'),
            'education': request.POST.get('education'),
            'deadline': request.POST.get('deadline'),
            'hr_id': hr_id,
            'posted_date': datetime.datetime.now()
        }
        
        # Insert into MongoDB
        job_collection.insert_one(job_data)
        
        messages.success(request, "Job posting created successfully!")
        return redirect('hr_panel')
    
    return redirect('hr_panel')

from bson import ObjectId
import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

# update the job
@login_required
def update_job(request):
    if request.method == 'POST':
        hr_id = request.session.get('hr_id')
        job_id = request.POST.get('job_id')
        print(hr_id)
        print(job_id)

        if not hr_id:
            messages.error(request, "You need to be logged in as an HR to update jobs.")
            return redirect('hr_login')

        if not job_id:
            messages.error(request, "Job ID is missing.")
            return redirect('hr_panel')

        try:
            job_object_id = ObjectId(job_id)
        except Exception as e:
            messages.error(request, "Invalid Job ID format.")
            return redirect('hr_panel')

        # Check if the job exists and belongs to HR
        job = job_collection.find_one({"_id": job_object_id, "hr_id": hr_id})
        if not job:
            messages.error(request, "You can only edit jobs that you've created.")
            return redirect('hr_panel')

        # Update job data
        update_data = {
            'title': request.POST.get('title'),
            'company': request.POST.get('company'),
            'location': request.POST.get('location'),
            'salary': request.POST.get('salary'),
            'job_type': request.POST.get('job_type'),
            'experience': request.POST.get('experience'),
            'Skills': request.POST.get('Skills'),
            'description': request.POST.get('description'),
            'education': request.POST.get('education'),
            'deadline': request.POST.get('deadline'),
            'updated_at': datetime.now()

        }

        job_collection.update_one({"_id": job_object_id}, {"$set": update_data})
        messages.success(request, "Job posting updated successfully!")
        return redirect('hr_panel')

    return redirect('hr_panel')
from django.http import JsonResponse
from bson import ObjectId

def get_job_data(request, job_id):
    try:
        job_object_id = ObjectId(job_id)
        job = job_collection.find_one({"_id": job_object_id})
        if job:
            job['_id'] = str(job['_id'])  # Convert ObjectId to string
            return JsonResponse(job)
        else:
            return JsonResponse({"error": "Job not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from bson import ObjectId
# delete jobs
@login_required
def delete_job(request):
    if request.method == 'POST':
        hr_id = request.session.get('hr_id')
        job_id = request.POST.get('job_id')  # Ensure this matches the form field name
        print(f"HR ID: {hr_id}")
        print(f"Job ID from form: {job_id}")
        
        if not hr_id:
            messages.error(request, "You need to be logged in as an HR to delete jobs.")
            return redirect('hr_login')
        
        if not job_id:
            messages.error(request, "No job ID provided for deletion.")
            return redirect('hr_panel')
            
        try:
            # Convert job_id to ObjectId for MongoDB query
            job_id_obj = ObjectId(job_id)
            print(f"Successfully converted to ObjectId: {job_id_obj}")
            
            # Check if the job belongs to this HR
            job = job_collection.find_one({"_id": job_id_obj, "hr_id": hr_id})
            print(f"Job found: {job is not None}")
            
            if not job:
                messages.error(request, "You can only delete jobs that you've created.")
                return redirect('hr_panel')
            
            # Delete job
            result = job_collection.delete_one({"_id": job_id_obj})
            print(f"Delete result: {result.deleted_count} document(s) deleted")
            
            # Delete related applications
            app_result = job_applied_collection.delete_many({"job_id": str(job_id_obj)})
            print(f"Applications deleted: {app_result.deleted_count}")
            
            messages.success(request, "Job posting and related applications deleted successfully!")
        except Exception as e:
            messages.error(request, f"Error deleting job: {str(e)}")
            print(f"Error in delete_job: {str(e)}")
        
        return redirect('hr_panel')
    
    return redirect('hr_panel')
# Get job details for editing
@login_required
@login_required
def get_job_details(request, job_id):
    hr_id = request.session.get('hr_id')
    
    if not hr_id:
        return JsonResponse({"error": "Not authorized"}, status=401)
    
    try:
        # Fetch job details
        job = job_collection.find_one({"_id": ObjectId(job_id), "hr_id": hr_id})
        
        if not job:
            return JsonResponse({"error": "Job not found or not authorized"}, status=404)
        
        # Convert ObjectId to string for JSON serialization
        job['_id'] = str(job['_id'])
        
        print(f"Job data: {job}")  # Debugging line
        
        return JsonResponse(job)
    except Exception as e:
        print(f"Error fetching job details: {e}")  # Debugging line
        return JsonResponse({"error": "Invalid Job ID format or server error"}, status=500)
# Update application status
@login_required
def update_application_status(request):
    if request.method == 'POST':
        hr_id = request.session.get('hr_id')
        application_id = request.POST.get('application_id')
        status = request.POST.get('status')
        
        if not hr_id:
            return JsonResponse({"error": "Not authorized"}, status=401)
        
        # Update application status
        application = job_applied_collection.find_one({"_id": ObjectId(application_id)})
        
        if not application:
            return JsonResponse({"error": "Application not found"}, status=404)
        
        # Check if the job belongs to this HR
        job = job_collection.find_one({"_id": ObjectId(application['job_id']), "hr_id": hr_id})
        
        if not job:
            return JsonResponse({"error": "Not authorized to update this application"}, status=401)
        
        # Update status
        job_applied_collection.update_one(
            {"_id": ObjectId(application_id)},
            {"$set": {"status": status, "updated_at": datetime.now()}}
        )
        
        return JsonResponse({"success": True, "message": f"Application marked as {status}"})
    
    return JsonResponse({"error": "Method not allowed"}, status=405)



# HR logout
def hr_logout(request):
    logout(request)
    if 'hr_username' in request.session:
        del request.session['hr_username']
    if 'hr_id' in request.session:
        del request.session['hr_id']
    return redirect('hr_login')



# Hr panel
from bson import ObjectId
from django.shortcuts import render, redirect
from django.http import JsonResponse
import re

import re

def hr_panel_view(request):
    if not request.session.get('hr_id'):
        return redirect('loginhr')

    hr_id = request.session.get('hr_id')
    hr_user = hr_collection.find_one({"_id": ObjectId(hr_id)})
    # print(f"HR ID: {hr_id}")
    is_active = hr_user.get('is_active', False) if hr_user else False
    print(is_active)
    
    # Fetch jobs created by this HR
    hr_jobs = list(job_collection.find({"hr_id": hr_id}))
    # print(f"HR Jobs: {hr_jobs}")
    
    # Calculate applicants_count for each job dynamically
    for job in hr_jobs:
        job_id = job['_id']
        # print(f"Job ID: {job_id}")
        
        # Convert job_id to string (if it's an ObjectId)
        job_id_str = str(job_id)
        job['job_id'] = job_id_str
        job['id'] = job_id_str 
        # print(f"Job ID (String): {job_id_str}")
        
        # Debugging: Print the query
        # print(f"Querying for job_id: {ObjectId(job_id_str)}")
        
        # Count applications for this job dynamically
        applicants_count = job_applied_collection.count_documents({"job_id": ObjectId(job_id_str)})
        # print(f"Applicants Count for Job {job_id_str}: {applicants_count}")
        
        # Debugging: Print the applications found
        applications = list(job_applied_collection.find({"job_id": ObjectId(job_id_str)}))
        # print(f"Applications for Job {job_id_str}: {applications}")
        
        # Add applicants_count to the job
        job['applicants_count'] = applicants_count

    # print(f"HR Jobs with Applicants Count: {hr_jobs}")
    
    # Preprocess skills to split and clean
    for job in hr_jobs:
        if 'Skills' in job:
            # Split the skills string into a list
            if isinstance(job['Skills'], str):
                skills_list = job['Skills'].split(',')  # Split by comma
                skills_list = [skill.strip() for skill in skills_list]  # Remove extra spaces
                job['Skills'] = skills_list
            
            # Remove ALL whitespace from each skill
            job['Skills'] = [re.sub(r'\s+', '', skill) for skill in job['Skills']]
            # print(f"Processed Skills: {job['Skills']}")
    
    # Extract job titles (or another unique field) from hr_jobs
    # job_titles = [job['Job'] for job in hr_jobs]
    # # print(f"Job Titles: {job_titles}")
    
    
    # # Fetch applications for these job titles
    # applications = list(job_applied_collection.find({"job_id": {"$in": job_titles }}))
    # print(f"Applications: {applications}")
    job_ids = [str(job['_id']) for job in hr_jobs]  # Convert each _id to ObjectId
    print(f"Job IDs: {job_ids}")

# Fetch applications where job_id matches any job ObjectId
    applications = list(job_applied_collection.find({"job_id": {"$in": job_ids}}))
    # Process applicants
    applicants = []
    for application in applications:
        user_id = application.get('user_id')
        # print(f"Fetching user data for user_id: {user_id}")
        
        if user_id:
            user_data = auth_user_collection.find_one({"_id": ObjectId(user_id)})
            # print(f"User data: {user_data}")
            
            if user_data:
                user_data['application_id'] = str(application['_id'])
                user_data['applied_job_id'] = application['job_id']
                user_data['applied_at'] = application.get('applied_at', 'N/A')
                
                # Find the job details for the applied job
                job = next((j for j in hr_jobs if j['_id'] == ObjectId(application['job_id'])), None)

# Assign job title or default to 'Unknown Job'
                user_data['applied_job_title'] = job['Job'] if job else 'Unknown Job'
                
                # Rename _id to applicant_id
                user_data['applicant_id'] = str(user_data['_id'])
                
                # Remove the _id field to avoid confusion
                if '_id' in user_data:
                    del user_data['_id']
                
                applicants.append(user_data)
        else:
            print(f"No user found for user_id: {user_id}")
    
    # print(f"Applicants: {applicants}")
    
    context = {
        'hr_jobs': hr_jobs,
        'applicants': applicants,
         'is_active': is_active 
    }

    return render(request, 'hr.html', context)
# Add a view to get user details
def get_applicant_details(request, user_id):
    if not request.session.get('hr_id'):
        return JsonResponse({"error": "Not authorized"}, status=403)
    print(f"Fetching details for user_id  for view details: {user_id}")
    
    user_data = auth_user_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user_data:
        return JsonResponse({"error": "User not found"}, status=404)
    
    # Process user data for response
    user_details = {
        "user_id": user_id,
        "username": user_data.get("username", "N/A"),
        "email": user_data.get("email", "N/A"),
        "father_name": user_data.get("father_name", "N/A"),
        "mobile": user_data.get("mobile", "N/A"),
        "location": user_data.get("location", "N/A"),
        "branch": user_data.get("branch", "N/A"),
        "ug_college": user_data.get("ug_college", "N/A"),
        "Passout_Year": user_data.get("Passout_Year", "N/A"),
        "Graduation_Percentage": user_data.get("Graduation_Percentage", "N/A"),
        "10th_Percentage": user_data.get("10th_Percentage", "N/A"),
        "12th_Percentage": user_data.get("12th_Percentage", "N/A"),
        ""
        "skills": user_data.get("skills", []),
        "profile_picture": user_data.get("profile_picture", None)
    }
    # print(f"User details: {user_details}")
    return JsonResponse({"success": True, "data": user_details})

# hr user list
def hr_userlist(request):
    if not request.session.get('hr_id'):
        return redirect('loginhr')
    
    # Get filter parameters from request
    skills = request.GET.getlist('skills', [])
    graduation_year = request.GET.get('graduation_year', '')
    location = request.GET.get('location', '')
    min_percentage = request.GET.get('min_percentage', '')
    search = request.GET.get('search', '')
    
    query = {}
    
    # Handle skills filter - users must have ALL selected skills
    if skills:
        # Convert skills to regex patterns for case-insensitive matching
        skills_regex = [{'$regex': f'^{re.escape(skill)}', '$options': 'i'} for skill in skills]
        query['skills'] = {'$all': skills_regex}
    
    # Other filters remain the same
    if graduation_year:
        query['graduation_year'] = graduation_year
    
    if location:
        query['location'] = {'$regex': location, '$options': 'i'}
    
    if min_percentage:
        query['Graduation_Percentage'] = {'$gte': float(min_percentage)}
    
    if search:
        query['$or'] = [
            {'first_name': {'$regex': search, '$options': 'i'}},
            {'last_name': {'$regex': search, '$options': 'i'}},
            {'email': {'$regex': search, '$options': 'i'}},
            {'username': {'$regex': search, '$options': 'i'}}
        ]
    
    users = list(auth_user_collection.find(query))
    hr_id = request.session.get('hr_id')
    
    return render(request, 'hr_userlist.html', {'users': users, 'hr_id': hr_id})

def get_skills(request):
    search_term = request.GET.get('search', '').strip()
    
    # Create a case-insensitive regex pattern if search term exists
    query = {}
    if search_term:
        query['name'] = {'$regex': f'^{re.escape(search_term)}', '$options': 'i'}
    
    # Fetch skills with projection
    skills = list(skills_collection.find(query, {'name': 1, '_id': 0}).limit(20))
    
    return JsonResponse({
        'success': True,
        'skills': [skill['name'] for skill in skills]
    })

# API endpoint to get detailed user information
from bson import ObjectId
from django.http import JsonResponse

from bson import ObjectId
from django.http import JsonResponse
def get_user_details(request, user_id):
    if not request.session.get('hr_id'):
        return JsonResponse({'error': 'Not authorized'}, status=401)
    
    try:
        user_id = int(user_id)
    except ValueError:
        return JsonResponse({"error": "Invalid user ID format"}, status=400)
    
    user_data = auth_user_collection.find_one({"id": user_id})

    if not user_data:
        return JsonResponse({"error": "User not found"}, status=404)
    
    # Check if resume exists in filesystem
    resume_filename = f"resume_{user_id}.pdf"
    resume_path = os.path.join(settings.MEDIA_ROOT, 'resumes', resume_filename)
    has_resume = os.path.exists(resume_path)
    
    # If using MongoDB GridFS, you could check like this:
    # has_resume = fs.exists({"filename": resume_filename})
    
    user_details = {
        "user_id": user_data["id"],
        "username": user_data.get("username", "N/A"),
        "email": user_data.get("email", "N/A"),
        "father_name": user_data.get("father_name", "N/A"),
        "mobile": user_data.get("mobile", "N/A"),
        "location": user_data.get("location", "N/A"),
        "branch": user_data.get("branch", "N/A"),
        "ug_college": user_data.get("ug_college", "N/A"),
        "Passout_Year": user_data.get("Passout_Year", "N/A"),
        "Graduation_Percentage": user_data.get("Graduation_Percentage", "N/A"),
        "10th_Percentage": user_data.get("10th_Percentage", "N/A"),
        "12th_Percentage": user_data.get("12th_Percentage", "N/A"),
        "skills": user_data.get("skills", []),
        "profile_picture": user_data.get("profile_picture", None),
        "has_resume": has_resume,  # Add this flag
        "resume_filename": resume_filename if has_resume else None
    }
    
    return JsonResponse({"success": True, "data": user_details})

  
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def contact_applicant(request):
    if not request.session.get('hr_id'):
        return redirect('loginhr')
    
    if request.method == 'POST':
        applicant_email = request.POST.get('applicant_email')
        subject = request.POST.get('email_subject')
        message = request.POST.get('email_message')
        
        if not all([applicant_email, subject, message]):
            messages.error(request, 'All fields are required.')
            return redirect('hr_panel')
        
        # Get HR details for the 'from' email
        hr_id = request.session.get('hr_id')
        hr_data = hr_collection.find_one({"_id": ObjectId(hr_id)})
        hr_email = hr_data.get('email', settings.DEFAULT_FROM_EMAIL)
        
        try:
            send_mail(
                subject,
                message,
                hr_email,  # From email
                [applicant_email],  # To email
                fail_silently=False,
            )
            messages.success(request, f'Message sent successfully to {applicant_email}')
        except Exception as e:
            messages.error(request, f'Failed to send message: {str(e)}')
        
        return redirect('hr_panel')
   
   
   
   
   
   
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from bson import json_util

# In-memory collection to store jobs
apijob_collection = db1["apijob"]

# Track last cleanup time
last_cleanup_time = None

@csrf_exempt
def store_jobs(request):
    global last_cleanup_time
    
    if request.method == 'POST':
        try:
            # Check if 14390 minutes (~10 days) have passed since last cleanup
            current_time = datetime.now()
            if last_cleanup_time is None or (current_time - last_cleanup_time) >= timedelta(minutes=14390):
                apijob_collection.delete_many({})
                last_cleanup_time = current_time
                print(f"Performed cleanup at {current_time}")

            data = json.loads(request.body)
            jobs = data.get('jobs', [])

            if not jobs:
                return JsonResponse({'status': 'error', 'message': 'No jobs provided'}, status=400)

            # Insert jobs into MongoDB collection
            result = apijob_collection.insert_many(jobs)

            return JsonResponse({
                'status': 'success', 
                'message': f'{len(result.inserted_ids)} jobs stored successfully'
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def get_jobs(request):
    if request.method == 'GET':
        try:
            # Get all jobs from collection (no pagination for now)
            jobs = list(apijob_collection.find())
            
            # Convert ObjectId to string for JSON serialization
            for job in jobs:
                job['_id'] = str(job['_id'])
            
            return JsonResponse({
                'status': 'success',
                'data': jobs,
                'count': len(jobs)
            }, json_dumps_params={'default': json_util.default})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
from django.http import FileResponse, Http404
import os
from django.conf import settings

def download_resume(request, user_id):
    if not request.session.get('hr_id'):
        return JsonResponse({'error': 'Not authorized'}, status=401)
    
    try:
        user_id = int(user_id)
    except ValueError:
        return JsonResponse({"error": "Invalid user ID format"}, status=400)
    
    resume_filename = f"resume_{user_id}.pdf"
    resume_path = os.path.join(settings.MEDIA_ROOT, 'resumes', resume_filename)
    
    if not os.path.exists(resume_path):
        return JsonResponse({"error": "Resume not found"}, status=404)
    
    try:
        file = open(resume_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{resume_filename}"'
        response['Content-Type'] = 'application/pdf'
        return response
    except Exception as e:
        return JsonResponse({"error": f"Error accessing resume: {str(e)}"}, status=500)
    
from django.http import JsonResponse
from django.conf import settings

def get_api_keys(request):
    print(f"RAPIDAPI_KEY: {settings.RAPIDAPI_KEY}")
    print(f"RAPIDAPI_HOST: {settings.RAPIDAPI_HOST}")
    return JsonResponse({
        "RAPIDAPI_KEY": settings.RAPIDAPI_KEY,
        "RAPIDAPI_HOST": settings.RAPIDAPI_HOST
    })
    
from django.http import JsonResponse

def get_api_keys_message(request):
    print(f"RAPIDAPI_KEY: {settings.RAPIDAPI_KEY}")
    print(f"RAPIDAPI_HOST: {settings.RAPIDAPI_HOST}")
    return JsonResponse({
        "serviceID": settings.SERVICE_ID,  # Use correctly loaded variables
        "templateID": settings.TEMPLATE_ID,
    })


import re
from django.http import JsonResponse

def get_locations(request):
    search_term = request.GET.get('search', '').strip().lower()
    
    # Create query for array field
    query = {}
    if search_term:
        query["locations"] = {
            "$elemMatch": {
                "$regex": f".*{re.escape(search_term)}.*",
                "$options": "i"
            }
        }
    
    # Alternative query if above doesn't work
    # query["locations"] = {
    #     "$regex": f".*{re.escape(search_term)}.*",
    #     "$options": "i"
    # }
    
    # print("MongoDB Query:", query)  # Debug
    
    # Fetch matching documents
    docs = list(location_collection.find(query, {"_id": 0, "locations": 1}))
    
    # Extract all matching locations from arrays
    location_names = []
    for doc in docs:
        if "locations" in doc:
            for loc in doc["locations"]:
                if search_term in loc.lower():
                    location_names.append(loc)
    
    # Remove duplicates
    unique_locations = list(set(location_names))
    
    # print("Locations found:", unique_locations)  # Debug
    
    return JsonResponse({
        "success": True,
        "locations": unique_locations
    })


def search_locations(request):
    search_term = request.GET.get('search', '').strip().lower()
    country_filter = request.GET.get('country', '').strip()
    state_filter = request.GET.get('state', '').strip()
    
    # Build the query based on filters
    query = {}
    if country_filter:
        query['location.country'] = country_filter
    if state_filter:
        query['location.state'] = state_filter
    
    # Search across all location fields
    if search_term:
        query['$or'] = [
            {'location.country': {'$regex': search_term, '$options': 'i'}},
            {'location.state': {'$regex': search_term, '$options': 'i'}},
            {'location.city': {'$regex': search_term, '$options': 'i'}}
        ]
    
    # Get matching locations
    locations = list(auth_user_collection.find(query, {
        'location.country': 1,
        'location.state': 1,
        'location.city': 1,
        '_id': 0
    }).limit(20))
    
    # Remove duplicates and empty values
    unique_locations = []
    seen = set()
    
    for loc in locations:
        if 'location' in loc:
            loc_data = loc['location']
            loc_key = (loc_data.get('country'), loc_data.get('state'), loc_data.get('city'))
            if loc_key not in seen:
                seen.add(loc_key)
                unique_locations.append({
                    'country': loc_data.get('country'),
                    'state': loc_data.get('state'),
                    'city': loc_data.get('city')
                })
    
    return JsonResponse({
        'success': True,
        'locations': unique_locations
    })