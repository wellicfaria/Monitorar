
jQuery(document).ready(function() {
	
    /*
        Fullscreen background
    */
    $.backstretch("http://res.cloudinary.com/db79cecgq/image/upload/c_crop,h_720,w_1440,y_91/c_fill,h_800,w_1600/v1423156747/Polui%C3%A7%C3%A3o-do-ar-pode-causar-mudan%C3%A7a-no-DNA_-diz-estudo-.jpg");
    
    /*
        Form validation
    */
    $('.login-form input[type="text"], .login-form input[type="password"], .login-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    $('.login-form').on('submit', function(e) {
    	
    	$(this).find('input[type="text"], input[type="password"], textarea').each(function(){
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	
    });
    
    
});
