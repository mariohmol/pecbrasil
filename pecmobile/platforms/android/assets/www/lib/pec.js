function retiraCharPost(entrada){
	entrada = entrada.replace(/\"/g, ' ');
	entrada = entrada.replace(/\'/g, ' ');
	entrada = entrada.trim();
	return entrada;
}



    //<button onclick="login()">Login</button>
    //<button onclick="askForWritePerm()">Write Permissions</button> 
    //<button onclick="facebookWallPost()">Wall Post</button> 
    //<button onclick="logout()">Logout</button>

     FB.Event.subscribe('auth.login', function(response) {
                console.log('login event:' + JSON.stringify(response));
            });

            function me() {

                  FB.api('/me?fields=picture,name,email', function(user) {
                        console.log('response from facebook: ' + JSON.stringify(user));
                        var profilePictureUrl = '';
                        if (user.picture.data) {
                          profilePictureUrl = user.picture.data.url;
                        } else {
                          profilePictureUrl = user.picture;
                        }
                        console.log('userId: ' + user.id);
                        console.log('name: ' + user.name);
                        console.log('email: ' + user.email);
                        console.log('picture url: ' + profilePictureUrl);

                        $('#log').html(user.name);

                    });
            }
            
            function logout() {
                FB.logout(function(response) {
                    console.log('logout response:' + JSON.stringify(response));
                    alert('logged out');
                });
            }
            
            function login() {
                FB.login( function(response) {
                          
                   if (response.authResponse) {
                        //alert('logged in now');
                        console.log('login response:' + response.authResponse);
                        me();
                   } else {
                        //alert('not logged in on login');
                        console.log('login response:' + response.error);
                   }
                   },
                   { scope: "email" }
                   );
            }

            function askForWritePerm() {
                FB.login(
                   function(response) {
                    
                     if (response.authResponse) {
                          //alert('logged in now');
                          console.log('login response:' + response.authResponse);
                          // me();
                     } else {
                          //alert('not logged in on login');
                          console.log('login response:' + response.error);
                     }
                   },
                   { scope: "publish_actions" } 
                   );
            }
      
      
            function facebookWallPost() {
                console.log('Debug 1');
              var params = {
                  method: 'feed',
                  name: 'Facebook Dialogs',
                  link: 'https://developers.facebook.com/docs/reference/dialogs/',
                  picture: 'http://fbrell.com/f8.jpg',
                  caption: 'Reference Documentation',
                  description: 'Dialogs provide a simple, consistent interface for applications to interface with users.'
                };
              console.log(params);
                FB.ui(params, function(obj) { console.log(obj);});
            }
            
        