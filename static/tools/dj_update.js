	var interval;
	function update(){
    $.ajax({
		type: "GET",
		url:'/bets/update/',
		data: {},
		datatype: 'json',
		success: function(data){

		var asset_price = data['eurusd'];

		$('#balance').html(data['balance']);
		$('#recent_bets').html(data['tb']);
		$('#remaining_timex').html(data['time']);
		//interval = setTimeout(update, 1000);
			}

		});
	}