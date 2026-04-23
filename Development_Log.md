Date: 13/11/2025
What I did today: Set up project repository, project kanban board, a artifacts folder.
Challanges: Setting up All tools
Next Steps: Study basics of Django and React Native

Date: 20/04/2026
What I Did today: 
- Create backend repository
- Create database schema
- Import Dependencies
- Settings for Rest APi
- Settings for basic JWT
- User Model
- UserSerializer
- basicUrls
Next: 
- Create models
- test DB
- basic WEB app
- test Integrity

22/04/26
What I did today:
-Properly initialise django project + add JWT and REST_FRAMEWORK settings
-users APP:
    -initialise APP
    -User Model & RegisterSerializer
    -Add Register View with POST method
    -Add new Register endpoint /api/auth/register/
    -test Register endpoint with httpie 
    -Add login/, refresh/ endpoints
    -Write users app test 
    -Add me/ {refreshtoken} protected endpoint
    -test me/
    -Logout endpoint - blacklist current refresh token
    TO DO: EXERCISES AND WORKOUTS ENDPOINTS
23/04/26

-----------------
USERS APP ENDPOINTS:
METHOD:    POST | PATH: /api/auth/register/ |-> create new user account
METHOD:    POST | PATH: /api/auth/login/    |-> returns access + refresh tokens
METHOD:    POST | PATH: /api/auth/refresh/  |-> get new access token using refresh token
METHOD:    GET  | PATH: /api/auth/me/       |-> returns current user data (requires auth)
METHOD:    POST | PATH: /api/auth/logout/   |-> blacklists refresh token

Note: /me/ request requires header -> Authorization: 'Bearer {refresh.access_token}'
Note: JWT tokens must be store in httpOnly cookie, only safe storage

TO DO 
Exercises endpoint app, models,serializers, views, urls
