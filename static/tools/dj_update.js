	var interval;
	function update(){
    $.ajax({
		type: "GET",
		url:'/bets/update/',
		data: {},
		datatype: 'json',
		success: function(data){
		$('#balance').html(data['balance']);
		$('#recent_bets').html(data['tb']);
		//interval = setTimeout(update, 1000);
			}

		});
	}
