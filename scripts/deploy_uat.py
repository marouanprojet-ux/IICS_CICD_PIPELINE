import os
import sys
from iics_client import IICSClient

def main():
    uat_commit_hash = os.environ.get('UATCOMMITHASH')  # ✅ OK
    
    # ✅ CORRECTION : Ligne 11
    pod_url = os.environ.get('IICSPOD_URL')  # ← Ajouté underscore
    
    session_id = os.environ.get('uatsessionId')  # ✅ OK
    
    if not uat_commit_hash:
        print("UATCOMMITHASH environment variable is required.")  # ✅ OK
    # ✅ CORRECTION : Ligne 18
    if not pod_url:
        print("IICSPOD_URL environment variable is required.")  # ← Underscore
        
    if not session_id:
        print("uatsessionId environment variable is required.")
        
    client = IICSClient(pod_url=pod_url, session_id=session_id)
    
    try:
        client.pull_by_commit(uat_commit_hash)  # ✅ OK
        
        objects = client.get_commit_objects(uat_commit_hash, resource_type_filter='MTT')  # ✅ OK
        
        for obj in objects:
            app_context_id = obj.get('appContextId')
            if app_context_id:
                client.run_job(app_context_id)
            else:
                print(f"Skipping object {obj} (no appContextId)")
                
    except Exception as e:
        print(f"Error in UAT update and test: {e}")
        sys.exit(1)
        
    client.logout()

if __name__ == "__main__":
    main()
