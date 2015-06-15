	$('document').ready(function(){
    var form = $('#betsize');
	var user = $('#user').html();
	$("#call_place").click(function(){
		var payout = $('#call_payout1').html();	
		var strike = $('#call_strike1').html();
		var amount = $('#bet_amount').val();
		$('#bet_payout').val(payout);
		$('#bet_type').val("CALL");
		$('#bet_size').val(amount);
    	$.ajax( 
			{type: "POST",
			url:'/bets/place_bets/',
			data: form.serialize(),
			success: function(response) {
			$('#status').html(response);
			alert(response);
			}
			});
		
		});

		$("#put_place").click(function(){
		var payout = $('#put_payout5').html();	
		var strike = $('#put_strike5').html();
		var amount = $('#bet_amount').val();
		$('#bet_payout').val(payout);
		$('#bet_type').val("PUT");
		$('#bet_size').val(amount);
    	$.ajax( 
			{type: "POST",
			url:'/bets/place_bets/',
			data: form.serialize(),
			success: function(response) {

			$('#status').html(response);
			alert(response); 
			}
			});
		});

	
});
