# Remember Code
This IOS application will allow developers of different levels (Junior, Middle, Senior) to refresh their knowledge of programming languages (mainly Python, Swift), so developers could prepare for their interviews. Repository contains the Remember Code app. 

# Main project features
- Hundreds of relevant, graded by difficulty interview questions for programming languages.
- Progression system.
- Daily activities.
- Time limited challenges with different exercises. 

# Some of the so far implemented backend features
- Personal account for users (powered by PostgreSQL, fastapi-users).
- Model of registrated users database (database - PostgreSQL, ORM - SQLAlchemy), registration and authentication logic. Authentication is currently based on customised fastapi users library.
- Login works by Redis database with infinite lifetime tokens (token expires with logout, or by admins actions).
- MongoDB (powered by ODM Beanie) is used to store questions and exercises.
- Pydantic for data validation.

# Programming languages, frameworks
Swift, Python 3.11, FastAPI, SQLAlchemy, PostgreSQL, MongoDB, Beanie, Redis. View full req list -> requirements.txt

# Work in progress, App Store release is planned for February 2024.
