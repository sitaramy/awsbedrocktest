import json
import urllib3
from datetime import datetime, timedelta

# Initialize the connection pooler
http = urllib3.PoolManager()

def lambda_handler(event, context):
    # 1. Safely extract the function name (apiPath for OpenAPI, function for Function-based)
    function = event.get('apiPath') or event.get('function')
    api_path = event.get('apiPath')       # This is what Bedrock is complaining about
    http_method = event.get('httpMethod') # Usually 'POST' or 'GET'
    
    # 2. Safely extract the action group
    action_group = event.get('actionGroup')
    
    # 3. Handle parameters (they might be missing or empty)
    parameters = event.get('parameters', [])
    params = {p['name']: p['value'] for p in parameters}

    # Debugging: This helps you see the event in CloudWatch Logs
    print(f"Received function: {function} from action group: {action_group}")

    if not function:
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': action_group,
                'functionResponse': {
                    'responseBody': {'TEXT': {'body': "Error: No function/apiPath found in event."}}
                }
            }
        }
    
    # ... rest of your if/elif logic ...
    
    result_text = ""

    try:
        # --- ROUTE 1: SEARCH FUND ---
        if function == "search_fund":
            query = params.get('fund_name', '')
            url = f"https://api.mfapi.in/mf/search?q={query.replace(' ', '%20')}"
            response = http.request('GET', url)
            data = json.loads(response.data.decode('utf-8'))
            
            if not data:
                result_text = f"No funds found for '{query}'."
            else:
                results = [f"{item['schemeCode']}: {item['schemeName']}" for item in data[:10]]
                result_text = "Found these matching funds. Use the 6-digit code for details:\n" + "\n".join(results)

        # --- ROUTE 2: LATEST NAV ---
        elif function == "get_latest_nav":
            code = params.get('scheme_code')
            url = f"https://api.mfapi.in/mf/{code}/latest"
            response = http.request('GET', url)
            data = json.loads(response.data.decode('utf-8'))
            nav_info = data['data'][0]
            result_text = f"The latest NAV for {code} is ₹{nav_info['nav']} as of {nav_info['date']}."

        # --- ROUTE 3: HISTORICAL NAV ---
        elif function == "get_historical_nav":
            code = params.get('scheme_code')
            start_dt = datetime.strptime(params.get('start_date'), '%d-%m-%Y')
            end_dt = datetime.strptime(params.get('end_date'), '%d-%m-%Y')
            
            # 3-Month Range Check
            if (end_dt - start_dt) > timedelta(days=90):
                result_text = "Error: The date range exceeds 3 months. Please select a shorter period."
            else:
                url = f"https://api.mfapi.in/mf/{code}"
                response = http.request('GET', url)
                all_data = json.loads(response.data.decode('utf-8'))['data']
                
                filtered = [f"{e['date']}: ₹{e['nav']}" for e in all_data 
                            if start_dt <= datetime.strptime(e['date'], '%d-%m-%Y') <= end_dt]
                
                result_text = "\n".join(filtered) if filtered else "No data found for these dates."

        else:
            result_text = f"Function {function} is not implemented."

    except Exception as e:
        result_text = f"Something went wrong: {str(e)}"

    # 2. Return the response in the format Bedrock expects
    return {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': action_group,
            'function': function,
            'apiPath': api_path,       # CRITICAL: Echo this back
            'httpMethod': http_method, # CRITICAL: Echo this back
            'functionResponse': {
                'responseBody': {
                    'TEXT': {
                        'body': result_text
                    }
                }
            }
        }
    }
