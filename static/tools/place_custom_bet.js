	$('document').ready(function(){
    var form = $('#custom_binary_form');
	$("#purchase_c").click(function(){
		var shown_payout = $('#custom_payout').html();
		$('#shown_payout').val(shown_payout);
    	$.ajax( 
			{type: "POST",
			url:'/bets/place_custom_bet/',
			data: form.serialize(),
			success: function(response) {
			alert(response);
			update();
			}
			});
// Update the bets
	
	
		});


	
});
