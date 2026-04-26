<h1>13/11/2025</h1>

What I did today:
-
- Set up project repository, project kanban board, a artifacts folder.
- 
Challanges:
- 
- Setting up All tools
- 
Next Steps:
-
- Study basics of Django and React Native

<h1>20/04/2026</h1>

What I Did today: 
-
- Create backend repository
- Create database schema
- Import Dependencies
- Settings for Rest APi
- Settings for basic JWT
- User Model
- UserSerializer
- basicUrls

Next: 
-
- Create models
- test DB
- basic WEB app
- test Integrity

<h1>22/04/26</h1>

What I did today:
-

- initialise APP
- User Model & RegisterSerializer
- Add Register View with POST method
- Add new Register endpoint /api/auth/register/
- test Register endpoint with httpie 
- Add login/, refresh/ endpoints
- Write users app test 
- Add me/ {refreshtoken} protected endpoint
- test me/
- Logout endpoint - blacklist current refresh token
TO DO: EXERCISES AND WORKOUTS ENDPOINT

-----------------
<h1>23/04/26</h1>

USERS APP ENDPOINTS:
-
 - POST  PATH(/api/auth/register/)   create new user account
 - POST  PATH(/api/auth/login/   )   returns access + refresh tokens
 - POST  PATH(/api/auth/refresh/ )   get new access token using refresh token
 - GET   PATH(/api/auth/me/      )   returns current user data (requires auth)
 - POST  PATH(/api/auth/logout/  )   blacklists refresh token

Note: /me/ request requires header(Authorization: 'Bearer {refresh.access_token}')
Note: JWT tokens must be store in httpOnly cookie, only safe storage

EXERCISES ENDPOINTS:
-
 - GET /api/muscle-groups/                  -list all muscle groups
 - GET /api/muscle-groups/<id>/             -single muscle group
 - GET /api/equipment-types/                -list all equipment types
 - GET /api/equipment-types/<id>/           -single equipment type
 - GET /api/exercises/                      -list all exercises
 - GET /api/exercises/<id>/                 -single exercise
 - GET /api/exercises/?muscle_group=<id>    -filter by muscle group
 - GET /api/exercises/?equipment_type=<id>  -filter by equipment type
 - GET /api/exercises/?is_compound=true     -filter by compound/isolation

What I did today:
-
- Created Exercises App
- Model, Serializers, ViewSet classes and corresponding router
- Management command  seed the exercises library
- Test Exercises httpie
- Test Exercises automated tests
- Created plans App
- plans models
- updated admin site
<h1>24/04/26-25/04/26</h1>

What I did in this sprint:
-
- create command to populate workout plans related tables
- add plans serializer 
- add view sets with queryset-level filtering
- test with httpie
- automated tests
- update admin 
- add DRF nested router for auto plans auto urls setup 
- start workout app
- add workouts models

TO DO:
-
- Standard workout logging - user starts workout, logs all exercises and marks workout complete
- Workout Assistant flow - return defaults to walk the user through planned workout

<h1>26/04/26</h1>

What I did today:
-

- Create Serializers for workouts and sets
- Create Views(modelviewsets) for workouts and sets 

