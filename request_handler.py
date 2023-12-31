from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from views.user import create_user, login_user
from views import get_single_post, get_all_posts, create_post, update_post, delete_post
from views import get_single_subscription, get_all_subscriptions , delete_subscription, update_subscription, create_subscription
from views import get_single_comment, get_all_comments, create_comment, update_comment, delete_comment
from views import get_single_category, get_all_category, update_category, create_category, delete_category
from views import get_all_tags, get_single_tag, update_tag, create_tag, delete_tag, get_single_post_tag, get_all_post_tags, create_post_tag
from views import get_single_reaction, get_all_reactions
from views import get_all_users, get_single_user, get_all_post_reactions, get_single_post_reaction, delete_post_reaction, update_post_reaction, get_all_users_posts
class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        parsed_url = urlparse(path)
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            
            if parsed_url.query:
                query = parse_qs(parsed_url.query)
                return (resource, query)

            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        
        response = {}
        
        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
        
        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed
            
            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)
                    self._set_headers(200)

                else:
                    response = get_all_posts()
                    self._set_headers(200)
            if resource == "subscriptions":
                if id is not None:
                    response = get_single_subscription(id)
                    self._set_headers(200)
                else:
                    response = get_all_subscriptions()
                    self._set_headers(200)
            if resource == "comments":
                if id is not None: 
                    response = get_single_comment(id)
                    self._set_headers(200)
                else:
                    response = get_all_comments()
                    self._set_headers(200)       
            if resource == "categories":
                if id is not None:
                    response = get_single_category(id)
                    self._set_headers(200)
                else:
                    response = get_all_category()
                    self._set_headers(200)
            
            if resource == "tags":
                if id is not None:
                    response = get_single_tag(id)
                    self._set_headers(200)
                else:
                    response = get_all_tags()
                    self._set_headers(200)
            
            if resource == "posttags":
                if id is not None:
                    response = get_single_post_tag(id)
                    self._set_headers(200)
                else:
                    response = get_all_post_tags()
                    self._set_headers(200)
                    
            if resource == "reactions":
                if id is not None:
                    response = get_single_reaction(id)
                    self._set_headers(200)
                else:
                    response = get_all_reactions()
                    self._set_headers(200)
                    
            if resource == "postreactions":
                if id is not None:
                    response = get_single_post_reaction(id)
                    self._set_headers(200)
                else:
                    response = get_all_post_reactions()
                    self._set_headers(200)
                    
            if resource == "users":
                if id is not None:
                    response = get_single_user(id)
                    self._set_headers(200)
                else:
                    response = get_all_users()
                    self._set_headers(200)
        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed
            # see if the query dictionary has an email key
            if query.get('user_id') and resource == 'posts':
                response = get_all_users_posts(query['user_id'][0])
                self._set_headers(200)
            
                    
        self.wfile.write(json.dumps(response).encode())


    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url(self.path)
        
        new_post = None

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == "posts":
            new_post = create_post(post_body)
        if resource == "subscriptions":
            response = create_subscription(post_body)
        if resource == 'comments':
            response = create_comment(post_body)
        if resource == "categories":
            response = create_category(post_body)
        if resource == "tags":
            response = create_tag(post_body)
        if resource == "posttags":
            response = create_post_tag(post_body)
        # self.wfile.write(response.encode())
        # self.wfile.write(json.dumps(new_post).encode())
        if new_post is not None:
            self.wfile.write(json.dumps(new_post).encode())
        else:
            self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)
            # set default value of success
        success = False

        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "subscriptions":
            success = update_subscription(id, post_body)
        if resource == 'comments':
            success = update_comment(id, post_body)
        if resource == "categories":
            success = update_category(id, post_body)
        if resource == "tags":
            success = update_category(id, post_body)
        if resource == "posttags":
            success = update_category(id, post_body)
    # handle the value of success
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())


    def do_DELETE(self):
        """Handle DELETE Requests"""
            # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)
        
        if resource == "posts":
            delete_post(id)
        if resource == "subscriptions":
            delete_subscription(id)
        if resource == 'comments':
            delete_comment(id)
        if resource == "categories":
            delete_category(id)
        if resource == "tags":
            delete_category(id)
        if resource == "posttags":
            delete_post_tag(id)
        self.wfile.write("".encode())

def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
