import os
from dotenv import load_dotenv
from agents.security.security import security_node
from agents.senior_dev.senior_dev import senior_dev_node

# 1. Load Environment
load_dotenv()
print("--- ENVIRONMENT CHECK ---")
if os.getenv("GITHUB_TOKEN"):
    print("✅ GITHUB_TOKEN found.")
else:
    print("❌ GITHUB_TOKEN is MISSING. Check your .env file!")

if os.getenv("GOOGLE_API_KEY"):
    print("✅ GOOGLE_API_KEY found.")
else:
    print("❌ GOOGLE_API_KEY is MISSING. Check your .env file!")

# 2. Test Data (Use your actual Repo URL from the screenshot)
test_state = {
    "repo_url": "https://github.com/saiyesh1th/simple_task_manager_api-qbte",
    "messages": [],
    "security_status": "clean"
}

# 3. Test Security Agent
print("\n--- TESTING SECURITY AGENT ---")
try:
    sec_result = security_node(test_state)
    print("✅ Security Agent Success:", sec_result)
except Exception as e:
    print(f"🔥 SECURITY AGENT CRASHED: {e}")
    import traceback
    traceback.print_exc()

# 4. Test Senior Dev Agent
print("\n--- TESTING SENIOR DEV AGENT ---")
try:
    dev_result = senior_dev_node(test_state)
    print("✅ Senior Dev Success:", dev_result)
except Exception as e:
    print(f"🔥 SENIOR DEV CRASHED: {e}")
    import traceback
    traceback.print_exc()