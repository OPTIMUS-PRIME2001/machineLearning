#activate command=./env_Dir/Scripts/activate

# start a flask server
from flask import Flask, request

# import cors
from flask_cors import CORS

# import url parser
from urllib.parse import urlparse

# import re
import re

# import os
import os

# import pkl to load file
import pickle 

# import model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

# Defining Build Folder Path
buildFolderPath = os.path.join(os.path.dirname(__file__), '..', 'build')

# create a flask app
app = Flask(__name__, static_folder=buildFolderPath, static_url_path='/')

# enable cors
CORS(app)

# define a route to check application
@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

# route at /prediction to get the json response and find the prediction from the model
@app.route('/prediction', methods=['POST'])
def prediction():
    
    data = request.get_json()
    url = data.get('srcurl')
    
    if url is not None:
        # extract features from the url
        features = extract_features(url)
        
        # make prediction
        prediction = model.predict([features])[0]
        
        # return the prediction
        return {'prediction': prediction}
    
    return {'prediction': 'No URL found'}


def display_routes(app):
    """Display all the routes."""
    for route in app.url_map.iter_rules():
        print(route, route.methods)
        
        
def extract_features(url):
            # 1. URL length
            url_length = len(url)

            # 2. Domain length
            domain = urlparse(url).netloc
            domain_length = len(domain)

            # 3. Number of subdomains
            subdomains = domain.split('.')
            num_subdomains = len(subdomains)

            # 4. Use of IP address in URL
            is_ip_address = 1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain) else 0

            # 5. Use of '@' symbol in URL
            has_at_symbol = 1 if '@' in url else 0

            # 6. Use of 'https' in URL
            has_https = 1 if 'https' in url else 0

            # 7. Use of 'http' in URL
            has_http = 1 if 'http' in url else 0

            # 8. Use of 'www' in URL
            has_www = 1 if 'www' in url else 0

            # 9. Use of hyphen '-' in domain
            has_hyphen = 1 if '-' in domain else 0

            # 10. Number of dots in domain
            num_dots = domain.count('.')

            # 11. Number of digits in URL
            num_digits = sum(c.isdigit() for c in url)

            # 12. Number of special characters in URL
            num_special_chars = sum(not c.isalnum() for c in url)

            # 13. Presence of known phishing keywords in URL
            phishing_keywords = ['secure', 'account', 'login', 'verify', 'bank', 'paypal']
            has_phishing_keywords = any(keyword in url for keyword in phishing_keywords)

            # 14. URL path length
            path = urlparse(url).path
            path_length = len(path)

            # 15-20. Presence of specific file extensions in the URL
            extensions = ['.exe', '.zip', '.pdf', '.doc', '.php', '.html']
            has_extensions = [1 if extension in url else 0 for extension in extensions]

            # Combine all features into a feature vector
            feature_vector = [
                url_length,
                domain_length,
                num_subdomains,
                is_ip_address,
                has_at_symbol,
                has_https,
                has_http,
                has_www,
                has_hyphen,
                num_dots,
                num_digits,
                num_special_chars,
                has_phishing_keywords,
                path_length,
                *has_extensions
            ]

            return feature_vector

if __name__ == '__main__':
    display_routes(app)
    app.run(debug=True, host='0.0.0.0')


# # start a flask server
# from flask import Flask, request

# # import pkl to load file
# import pickle

# # import model
# # model = pickle.load(open('model.pkl', 'rb'))

# # create a flask app
# app = Flask(__name__)

# # define a route to check application
# @app.route('/', methods=['GET'])
# def index():
#     return 'Hello World'

# # route at /prediction to get the json response and find the prediction from the model
# @app.route('/prediction', methods=['POST'])
# def prediction():
    
#     data = request.get_json()
#     print(data)
#     return data


# def display_routes(app):
#     """Display all the routes."""
#     for route in app.url_map.iter_rules():
#         print(route, route.methods)

# # run the app
# if __name__ == '__main__':
    
#     # display all the routes
#     display_routes(app)
#     app.run(debug=True, host="0.0.0.0")