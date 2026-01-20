import os
import sys
from iics_client import IICSClient

def main():
    # Changé: COMMIT_HASH → COMMITHASH (pour matcher YAML)
    commit_hash = os.environ.get('COMMITHASH')
    
    # Changé: IICS_POD_URL → IICSPODURL (pour matcher YAML)
    pod_url = os.environ.get('IICSPODURL')
    
    # sessionId vient de iics_auth.py via GITHUB_ENV
    session_id = os.environ.get('sessionId')
    
    if not commit_hash:
        print("COMMITHASH environment variable is required.")
        sys.exit(1)
        
    if not pod_url:
        print("IICSPODURL environment variable is required.")
        sys.exit(1)
        
    if not session_id:
        print("sessionId environment variable is required (should be set by previous login step).")
        sys.exit(1)
        
    client = IICSClient(pod_url=pod_url, session_id=session_id)
    
    try:
        # Changé: ZZZ → MTT (votre type d'objet réel)
        objects = client.get_commit_objects(commit_hash, resource_type_filter='MTT')
        
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
