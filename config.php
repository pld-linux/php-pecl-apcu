<?php
// Use (internal) authentication - best choice if
// no other authentication is available
// If set to 0:
//  There will be no further authentication. You
//  will have to handle this by yourself!
// If set to 1:
//  You need to change ADMIN_PASSWORD to make
//  this work!
define('USE_AUTHENTICATION', 1);

// Admin Username
define('ADMIN_USERNAME', 'apc');
// Admin Password - CHANGE THIS TO ENABLE!!!
define('ADMIN_PASSWORD', 'password');

// (beckerr) I'm using a clear text password here, because I've no good idea how to let 
//           users generate a md5 or crypt password in a easy way to fill it in above

//define('DATE_FORMAT', "d.m.Y H:i:s");	// German
//define('DATE_FORMAT', "d/m/Y H:i:s");	// French
//define('DATE_FORMAT', 'Y/m/d H:i:s'); 	// US
define('DATE_FORMAT', 'Y-m-d H:i:s'); 	// ISO8601

// Image size
define('GRAPH_SIZE',200);

//define('PROXY', 'tcp://127.0.0.1:8080');
