	$('document').ready(function(){
    var form = $('#betsize');
	$("#call_place").click(function(){
		var amount = $('#bet_amount').val();
		$('#bet_type').val("CALL");
		$('#bet_size').val(amount);
    	$.ajax( 
			{type: "POST",
			url:'/bets/place_bets/',
			data: form.serialize(),
			success: function(response) {
			alert(response);
			update();
			}
			});
// Update the bets
	
	
		});

		$("#put_place").click(function(){
		var amount = $('#bet_amount').val();
		$('#bet_type').val("PUT");
		$('#bet_size').val(amount);
    	$.ajax( 
			{type: "POST",
			url:'/bets/place_bets/',
			data: form.serialize(),
			success: function(response) {
			alert(response); 
			update();
			}
			});

// Update the bets



		});

	
});
