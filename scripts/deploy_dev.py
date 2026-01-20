import os
import sys
from iics_client import IICSClient

def main():
    commit_hash = os.environ.get('COMMITHASH')  # ✅ OK
    
    # ✅ CORRECTION : Ligne 11
    pod_url = os.environ.get('IICSPOD_URL')  # ← Ajouté underscore
    
    session_id = os.environ.get('sessionId')  # ✅ OK
    
    if not commit_hash:
        print("COMMITHASH environment variable is required.")  # ✅ OK
    # ✅ CORRECTION : Ligne 18  
    if not pod_url:
        print("IICSPOD_URL environment variable is required.")  # ← Underscore
        
    if not session_id:
        print("sessionId environment variable is required (should be set by previous login step).")
        
    client = IICSClient(pod_url=pod_url, session_id=session_id)
    
    try:
        objects = client.get_commit_objects(commit_hash, resource_type_filter='MTT')  # ✅ OK
        if not objects:
            print(f"No objects of type 'MTT' found in commit {commit_hash}")
        
        for obj in objects:
            app_context_id = obj.get('appContextId')
            if app_context_id:
                client.run_job(app_context_id)
            else:
                print(f"Object {obj} has no appContextId")
                
    except Exception as e:
        print(f"Error checking updates: {e}")
        sys.exit(1)
        
    client.logout()

if __name__ == "__main__":
    main()
