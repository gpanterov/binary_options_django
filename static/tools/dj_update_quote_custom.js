
	function update_quote_custom(){
	var option_type_c = $('#option_type_c').val();
	var strike_price_c = $('#strike_price_c').val();
	var expiration_c = $('#expiration_c').val();
	var amount_c = $('#amount_c').val();
	var asset = $('#asset').val();
    $.ajax({
		type: "GET",
		url:'/bets/update_quote_custom/',
		data: {'option_type_c':option_type_c, 'strike_price_c':strike_price_c, 'expiration_c':expiration_c, 
					'amount_c':amount_c, 'asset':asset},
		datatype: 'json',
		success: function(data){
		$('#custom_payout').html(data['payout']);
		$('#custom_payout_amount').html(data['payout_amount']);
			}

		});
	}
