import os
import sys
from iics_client import IICSClient

def main():
    uat_commit_hash = os.environ.get('UATCOMMITHASH')
    
    # ✅ FIXÉ : IICSPOD_URL → IICS_POD_URL
    pod_url = os.environ.get('IICS_POD_URL')
    
    session_id = os.environ.get('uatsessionId')
    
    if not uat_commit_hash:
        print("UATCOMMITHASH environment variable is required.")
        sys.exit(1)
    if not pod_url:
        print("IICS_POD_URL environment variable is required.")
        sys.exit(1)
    if not session_id:
        print("uatsessionId environment variable is required.")
        sys.exit(1)
        
    client = IICSClient(pod_url=pod_url, session_id=session_id)
    
    try:
        client.pull_by_commit(uat_commit_hash)
        objects = client.get_commit_objects(uat_commit_hash, resource_type_filter='MTT')
        
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
    print("✅ UAT Deploy SUCCESS")

if __name__ == "__main__":
    main()
