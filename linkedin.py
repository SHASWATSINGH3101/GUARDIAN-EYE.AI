import requests
import json

def get_user_info(access_token):
    """
    Retrieve user information from LinkedIn using the provided access token
    """
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token.strip()}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching user info: {response.status_code}")
        print(response.text)
        return None

def post_text_only(access_token, user_id, share_text):
    """
    Post text-only content to LinkedIn
    """
    url = "https://api.linkedin.com/v2/ugcPosts"
    
    payload = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": share_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    headers = {
        "Authorization": f"Bearer {access_token.strip()}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error posting content: {response.status_code}")
        print(response.text)
        return None

def main():
    # Replace with your actual access token - make sure to remove any newlines or extra whitespace
    access_token = '''AQWSZdhsJ7PagznPiKGyEQupRISvKjcSZxB686rfcEXOKzd2sDz9WutNVlgzuT8CuCW1_aFAQ4Uiu8ThKfcLTQaCqr2DbxNiZ-pVa5ozOVoM3YBBVQ2HLluCGM3qlVgQlMY7ESvFNgikdq8OptXKB33wxjKO07stfb7QmRF-iXJBxtcI5kF_F1t6qSZTcufYIFDoWBE0rOa5DIsdN5bcrwTgSCc3WEu2rE0ijzb5lZl1CcKtHZDE9_9o6nb0DTjlyFrQTt1_rtbU6HeIYRatfnfPQSIT_b0qYYl5MKU6V-Dfv4wYp0gDPsm_mjVQmeC-Yf6Oot6dslCq3s-ETAkKon2KFQO2qA
'''.strip()
    
    # Step 1: Get user info
    user_info = get_user_info(access_token)
    if not user_info:
        print("Failed to retrieve user information.")
        return
    
    user_id = user_info["sub"]
    print(f"Retrieved user ID: {user_id}")
    
    # Step 2: Post text content
    share_text = "This is a test post from my LinkedIn API integration. #testing #api"
    
    post_result = post_text_only(access_token, user_id, share_text)
    
    if post_result:
        print("Successfully posted content to LinkedIn!")
        print(f"Post ID: {post_result.get('id', 'Unknown')}")
    else:
        print("Failed to post content to LinkedIn.")

if __name__ == "__main__":
    main()