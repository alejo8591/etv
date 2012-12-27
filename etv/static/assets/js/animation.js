$(document).ready(function(){
	$('#buttonSend').click(function(event){
	    Dajaxice.users.send_form(Dajax.process, {'form':$('#my_form').serialize(true)});		   
    });
});