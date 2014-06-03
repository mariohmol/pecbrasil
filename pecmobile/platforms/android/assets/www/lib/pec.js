function retiraCharPost(entrada){
	entrada = entrada.replace(/\"/g, ' ');
	entrada = entrada.replace(/\'/g, ' ');
	entrada = entrada.trim();
	return entrada;
}


var storage = window.localStorage;



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
						
						window.localStorage.setItem("user", "user");


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
            	var value = window.localStorage.getItem("user");
				if ( value != null) return value;

                FB.login( function(response) {
                          
                   if (response.authResponse) {
                        //alert('logged in now');
                        console.log('login response:' + response.authResponse);
                        return me();
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
            

function runclassificacao(){
	url="http://localhost/json/times.json";
	//url='http://politicaesporteclube.com/attrs/time/';
	url="http://pecmobile/json/times.json";
	
	$.getJSON( url, function(data) {
			
					    $('#employeeList li').remove();
					    $.each(data.times, function(index, time) {				    
					    	retorno  = '<li><a href="time.html?id=' + time.id + '">' +
							'<h1>' + time.posicao + '</h1>' +
							'<h4>' + time.nome +  '</h4>' +
							'<p>' + time.posicao + '</p>' +
							'<span class="ui-li-count">' + time.pontuacao_total + '</span></a></li>';						
							if(time.pontuacao_total=="") time.pontuacao_total=0;						
					    	$('#employeeList').append(retorno);
					    });
					    $('#employeeList').listview('refresh');
					    $('#devicereadyApp').hide();
					    $('#loaded_header').show();
					    $('#loaded_content').show();
					    
			});
		
}	        