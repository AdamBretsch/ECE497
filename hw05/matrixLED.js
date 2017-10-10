    var socket;
    var firstconnect = true,
        i2cNum  = "0x70",
	dispg = [], // red display
    dispr = [], // green display
    disp = [];
// Create a matrix of LEDs inside the <table> tags.
var matrixData;
for(var j=7; j>=0; j--) {
	matrixData += '<tr>';
	for(var i=0; i<8; i++) {
	    matrixData += '<td><div class="LED" id="id'+i+'_'+j+
		'" onclick="LEDclick('+i+','+j+')">'+
		i+','+j+'</div></td>';
        }
	matrixData += '</tr>';
}
$('#matrixLED').append(matrixData);

// The slider controls the overall brightness
$("#slider1").slider({min:0, max:15, slide: function(event, ui) {
	socket.emit("i2cset",  {i2cNum: i2cNum, i: ui.value+0xe0, disp: 1});
    }});

// Send one column when LED is clicked.
function LEDclick(i, j) {
 	status_update(i+","+j+" clicked");
    // Toggle bit on display
    var element = $('#id'+i+'_'+j);
    if (element.hasClass('green')){ // if green, turn red
            dispg[i] ^= 0x1<<j;
            socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i, disp: '0x'+dispg[i].toString(16)});
            dispr[i] ^= 0x1<<j;
            socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i+1, disp: '0x'+dispr[i].toString(16)});
            element.removeClass('green');
            element.addClass('red');
    } else if (element.hasClass('red')){ // if red, turn yellow
            dispg[i] ^= 0x1<<j;
            socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i, disp: '0x'+dispg[i].toString(16)});
            element.removeClass('red');
            element.addClass('yellow');
    } else if(element.hasClass('yellow')){ // if yellow, turn off
            dispg[i] ^= 0x1<<j;
            socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i, disp: '0x'+dispg[i].toString(16)});
            dispr[i] ^= 0x1<<j;
            socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i+1, disp: '0x'+dispr[i].toString(16)});
            element.removeClass('yellow');
    } else { // if off, turn green
        dispg[i] ^= 0x1<<j;
        socket.emit('i2cset', {i2cNum: i2cNum, i: 2*i, disp: '0x'+dispg[i].toString(16)});
        element.addClass('green');
    }
}

    function connect() {
      if(firstconnect) {
        socket = io.connect(null);

        // See https://github.com/LearnBoost/socket.io/wiki/Exposed-events
        // for Exposed events
        socket.on('message', function(data)
            { status_update("Received: message " + data);});
        socket.on('connect', function()
            { status_update("Connected to Server"); });
        socket.on('disconnect', function()
            { status_update("Disconnected from Server"); });
        socket.on('reconnect', function()
            { status_update("Reconnected to Server"); });
        socket.on('reconnecting', function( nextRetry )
            { status_update("Reconnecting in " + nextRetry/1000 + " s"); });
        socket.on('reconnect_failed', function()
            { message("Reconnect Failed"); });

        socket.on('matrix',  matrix);

    socket.emit('i2cset', {i2cNum: i2cNum, i: 0x21, disp: 1}); // Start oscillator (p10)
    socket.emit('i2cset', {i2cNum: i2cNum, i: 0x81, disp: 1}); // Disp on, blink off (p11)
    socket.emit('i2cset', {i2cNum: i2cNum, i: 0xe7, disp: 1}); // Full brightness (page 15)
    /*
	i2c_smbus_write_byte(file, 0x21); 
	i2c_smbus_write_byte(file, 0x81);
	i2c_smbus_write_byte(file, 0xe7);
    */
        // Read display for initial image.  Store in disp[]
        socket.emit("matrix", i2cNum);

        firstconnect = false;
      }
      else {
        socket.socket.reconnect();
      }
    }

    function disconnect() {
      socket.disconnect();
    }

    // When new data arrives, convert it and display it.
    // data is a string of 16 values, each a pair of hex digits.
    function matrix(data) {
        var i, j;
        status_update("i2c: " + data);
        // Make data an array, each entry is a pair of digits
        data = data.split(" ");
        status_update("data: " + data);
        // Every other pair of digits are Green. The others are red.
        // Convert from hex.
        for (i = 0; i < data.length; i++) { // construct total display
            disp[i] = parseInt(data[i], 16);
        }
        
        for (i = 0; i < data.length; i++) { // construct green/red displays
            if (i % 2 === 0){
                dispg[i/2] = parseInt(data[i], 16);
                dispr[i/2] = parseInt(data[i+1], 16);
            } 
        }
        //status_update("dispr: " + dispr);
        // i cycles through each column
        for (i = 0; i < dispg.length; i++) { // scan for green
            // j cycles through each bit
            for (j = 0; j < 8; j++) {
                if (((dispg[i] >> j) & 0x1) === 1) {
                    $('#id' + i + '_' + j).addClass('green');
                }
            }
        }
        for (i = 1; i < dispr.length; i++) { // scan for red/yellow
            // j cycles through each bit
            for (j = 0; j < 8; j++) {
                if (((dispr[i] >> j) & 0x1) === 1) {
                    if (((dispg[i] >> j) & 0x1) === 1) {
                        $('#id' + i + '_' + j).addClass('yellow');
                    } else {    
                        $('#id' + i + '_' + j).addClass('red');
                    }
                }
            }
        }
    }

    function status_update(txt){
	$('#status').html(txt);
    }

    function updateFromLED(){
      socket.emit("matrix", i2cNum);    
    }

connect();

$(function () {
    // setup control widget
    $("#i2cNum").val(i2cNum).change(function () {
        i2cNum = $(this).val();
    });
})
