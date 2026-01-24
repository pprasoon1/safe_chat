user_risk = {}

async def update_user_risk(user, toxicity):
    if user not in user_risk:
        user_risk[user] = 0
    
    user_risk[user] += toxicity

# TODO add microservice architecture - docker and requirement.txt for both ml and backend, and real database
 # important- changed bcrypt to argon2
