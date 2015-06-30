	var interval;
	function update(){
	var d = new Date();
	var offset = d.getTimezoneOffset();
    $.ajax({
		type: "GET",
		url:'/bets/update/',
		data: {'offset':offset},
		datatype: 'json',
		success: function(data){
		$('#balance').html(data['balance']);
		$('#recent_bets').html(data['tb']);
		interval = setTimeout(update, 3000);
			}

		});
	}
