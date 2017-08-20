/*
# This code is a compliment to "Covert lie detection using keyboard dynamics".
This code was modified from:
 * A JavaScript project for accessing the accelerometer and gyro from various devices
 *
 * @author Tom Gallacher <tom.gallacher23@gmail.com>
 * @copyright Tom Gallacher <http://www.tomg.co>
 * @version 0.0.1a
 * @license MIT License
 * @options frequency, callback


API 

console_debugging 	(boolean variable to print messages in the console)


set_timestamp(type) : conversion in string (millisec from epoch)
		(0) timestamp_page_loaded
		(1) timestamp_start_monitoring
		(2) timestamp_first_keytap  (ALREADY INCLUDED IN monitor_keystroke function)
		(3) timestamp_enter_answer 	(ALREADY INCLUDED IN monitor_keystroke function, when enter button is tapped)
		returns the string of the actual timestamp

____________________________________________________________

SENSORS

devicemotion_able		(boolean variable to assess the capability to monitor accellerometer)
deviceorientation_able  (boolean variable to assess the capability to monitor gyroscope)

gyro.frequency 			(variable to set up the frequency of the sampling to X milliseconds)

monitor_sensors(buffersize=0) : function that starts or stops the monitoring on the sensors

is_monitoring 	(boolean variable 0: monitoring not running, 1: monitorin is running)

---results containers---
gyros_before 	(array of sample from gyroscope,	 	before starting tapping)
accel_before 	(array of sample from accellerometer,	before starting tapping)

gyros_typing	(array of sample from gyroscope,	 	before during tapping)
accel_typing	(array of sample from accellerometer,	before during tapping)


_________________________________________

KEYSTROKES
monitor_keystroke(textEdit) : attach the keylisteners to "textEdit object" and start monitoring

var typing_errors	(counter of errors in typing)

_______________________________

answer_submission()	: (function that performs the operations to submit the answer to the database)


*/

/**
 * A JavaScript project for accessing the accelerometer and gyro from various devices
 *
 * @author Tom Gallacher <tom.gallacher23@gmail.com>
 * @copyright Tom Gallacher <http://www.tomg.co>
 * @version 0.0.1a
 * @license MIT License
 * @options frequency, callback
 */
(function (root, factory) {
		if (typeof define === 'function' && define.amd) {
				// AMD. Register as an anonymous module.
				define(factory);
		} else if (typeof exports === 'object') {
				// Node. Does not work with strict CommonJS, but
				// only CommonJS-like enviroments that support module.exports,
				// like Node.
				module.exports = factory();
		} else {
				// Browser globals (root is window)
				root.gyro = factory();
	}
}(this, function () {
	var measurements = {
				x: null,
				y: null,
				z: null,
				alpha: null,
				beta: null,
				gamma: null
			},
			calibration = {
				x: 0,
				y: 0,
				z: 0,
				alpha: 0,
				beta: 0,
				gamma: 0,
				rawAlpha: 0,
				rawBeta: 0,
				rawGamma: 0
			},
			interval = null,
			features = [];

	var gyro = {};

	/**
	 * @public
	 */
	gyro.frequency = 500; //ms
	gyro.calibrate = function() {
		for (var i in measurements) {
			calibration[i] = (typeof measurements[i] === 'number') ? measurements[i] : 0;
		}
	};
	gyro.getOrientation = function() {
		return measurements;
	};
	gyro.startTracking = function(callback) {
		interval = setInterval(function() {
			callback(measurements);
		}, gyro.frequency);
	};
	gyro.stopTracking = function() {
		clearInterval(interval);
	};

	/**
	 * Current available features are:
	 * MozOrientation
	 * devicemotion
	 * deviceorientation
	 */
	gyro.hasFeature = function(feature) {
		for (var i in features) {
			if (feature == features[i]) {
				return true;
			}
		}
		return false;
	};
	gyro.getFeatures = function() {
		return features;
	};

	/**
	 * @private
	 */
	function eulerToQuaternion(e) {
		var s = Math.PI / 180;
		var x = e.beta * s, y = e.gamma * s; z = e.alpha * s;
		var cX = Math.cos(x / 2);
		var cY = Math.cos(y / 2);
		var cZ = Math.cos(z / 2);
		var sX = Math.sin(x / 2);
		var sY = Math.sin(y / 2);
		var sZ = Math.sin(z / 2);
		var w = cX * cY * cZ - sX * sY * sZ;
		x = sX * cY * cZ - cX * sY * sZ;
		y = cX * sY * cZ + sX * cY * sZ;
		z = cX * cY * sZ + sX * sY * cZ;
		return {x:x, y:y, z:z, w:w};
	}
	gyro.eulerToQuaternion=eulerToQuaternion;

	/**
	 * @private
	 */
	function quaternionMultiply(a, b) {
		return {
			w: a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
			x: a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
			y: a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
			z: a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w
		};
	}

	/**
	 * @private
	 */	
	function quaternionApply(v, a) {
		v = quaternionMultiply(a, {x:v.x,y:v.y,z:v.z,w:0});
		v = quaternionMultiply(v, {w:a.w, x:-a.x, y:-a.y, z:-a.z});
		return {x:v.x, y:v.y, z:v.z};
	}

	/**
	 * @private
	 */	
	function vectorDot(a, b) {
		return a.x * b.x + a.y * b.y + a.z * b.z;
	}

	/**
	 * @private
	 */
	function quaternionToEuler(q) {
		var s = 180 / Math.PI;
		var front = quaternionApply({x:0,y:1,z:0}, q);
		console.log(front);
		var alpha = (front.x == 0 && front.y == 0) ?
			0 : -Math.atan2(front.x, front.y);
		var beta = Math.atan2(front.z,Math.sqrt(front.x*front.x+front.y*front.y));
		var zgSide = {
			x: Math.cos(alpha), 
			y: Math.sin(alpha), 
			z: 0
		};
		var zgUp = {
			x: Math.sin(alpha) * Math.sin(beta),
			y: -Math.cos(alpha) * Math.sin(beta),
			z: Math.cos(beta)
		};
		var up = quaternionApply({x:0,y:0,z:1}, q);
		var gamma = Math.atan2(vectorDot(up, zgSide), vectorDot(up, zgUp));

		// wrap-around the value according to DeviceOrientation
		// Event Specification
		if (alpha < 0) alpha += 2 * Math.PI;
		if (gamma >= Math.PI * 0.5) {
			gamma -= Math.PI; alpha += Math.PI;
			if (beta > 0) beta = Math.PI - beta;
			else beta = -Math.PI - beta;
		} else if (gamma < Math.PI * -0.5) {
			gamma += Math.PI; alpha += Math.PI;
			if (beta > 0) beta = Math.PI - beta;
			else beta = -Math.PI - beta;
		}
		if (alpha >= 2 * Math.PI) alpha -= 2 * Math.PI;
		return {alpha: alpha * s, beta: beta * s, gamma: gamma * s};
	}

	/**
	 * @private
	 */
	// it doesn't make sense to depend on a "window" module
	// since deviceorientation & devicemotion make just sense in the browser
	// so old school test used.
	if (window && window.addEventListener) {
		function setupListeners() {
			function MozOrientationInitListener (e) {
				features.push('MozOrientation');
				e.target.removeEventListener('MozOrientation', MozOrientationInitListener, true);

				e.target.addEventListener('MozOrientation', function(e) {
					measurements.x = e.x - calibration.x;
					measurements.y = e.y - calibration.y;
					measurements.z = e.z - calibration.z;
				}, true);
			}
			function deviceMotionListener (e) {
				features.push('devicemotion');
				e.target.removeEventListener('devicemotion', deviceMotionListener, true);
				
				e.target.addEventListener('devicemotion', function(e) {
					measurements.x = e.accelerationIncludingGravity.x - calibration.x;
					measurements.y = e.accelerationIncludingGravity.y - calibration.y;
					measurements.z = e.accelerationIncludingGravity.z - calibration.z;
				}, true);
			}
			function deviceOrientationListener (e) {
				features.push('deviceorientation');
				e.target.removeEventListener('deviceorientation', deviceOrientationListener, true);
				
				e.target.addEventListener('deviceorientation', function(e) {
					var calib = eulerToQuaternion({
						alpha: calibration.rawAlpha, 
						beta: calibration.rawBeta, 
						gamma: calibration.rawGamma
					});
					calib.x *= -1; calib.y *= -1; calib.z *= -1; 

					var raw = eulerToQuaternion({
						alpha: e.alpha, beta: e.beta, gamma: e.gamma
					});
					var calibrated = quaternionMultiply(calib, raw);
					var calibEuler = quaternionToEuler(calibrated);

					measurements.alpha = calibEuler.alpha;
					measurements.beta = calibEuler.beta;
					measurements.gamma = calibEuler.gamma;

					measurements.rawAlpha = e.alpha;
					measurements.rawBeta = e.beta;
					measurements.rawGamma = e.gamma;
				}, true);
			}

			window.addEventListener('MozOrientation', MozOrientationInitListener, true);
			window.addEventListener('devicemotion', deviceMotionListener, true);
			window.addEventListener('deviceorientation', deviceOrientationListener, true);
		}
		setupListeners();
	}

	return gyro;
}));




var console_debugging= 0;


function set_debug(value){
	if(value==0 || value==1){
		console_debugging= value;
	} 
	else {
		console.log("error on setting console_debugging to "+value);
		}
}

var keydyn  =[];
var gyros_before	=[];
var accel_before	=[];
var gyros_typing	=[];
var accel_typing	=[];

var devicemotion_able		= gyro.hasFeature('devicemotion');
var deviceorientation_able	= gyro.hasFeature('deviceorientation');

//I set the frequency of the sampling to X milliseconds
gyro.frequency = 500; //ms

var is_monitoring=0;
var typing_started=0;
var timestamp_page_loaded		=0;		//0
var timestamp_start_monitoring	=0;		//1
var timestamp_first_keytap		=0;		//2
var timestamp_enter_answer		=0;		//3

//global variable for acc and gyro sampling
var timestamp_sample_glb=0;

//boolean to decect typing errors
var typing_errors	=0;

//function that performs the operations to submit the answer to the database
function answer_submission(){
	//insert into the database
	//insert values (user,...,keydyn.toString(),gyros_before.toString(),accel_before.toString(),gyros_typing.toString(),accel_typing.toString()) into answer(..,..,..) 
}

function console_log(string_){
    if(!console_debugging){
      console.log(""+string_+""); 
    } 
    return;
}


function set_timestamp(type){
	ts=""+new Date().getTime()+""; //conversion in string (millisec from epoch)
	if(type==0){timestamp_page_loaded=ts;}
	if(type==1){timestamp_start_monitoring=ts;}
	if(type==2){timestamp_first_keytap=ts;}
	if(type==3){timestamp_enter_answer=ts;}
	console_log("set timestamp for "+type+ " = "+ts);
	return ts;
}

function get_timestamp_now(){
	return new Date().getTime();	
}


//monitor sensors (works as start and stop)
function monitor_sensors(buffersize){ //buffersize<=0 -> no limits
	if (is_monitoring){
		is_monitoring=0;
		gyro.stopTracking();
		console_log("SENSORS: stop tracking sensors at "+get_timestamp_now());
	}	
	
	//checking if the monitor is on and if the device is capable to sense orientation and motion
	if (!is_monitoring && devicemotion_able && deviceorientation_able){
		is_monitoring=1;
		
		//starting to track the sensors with frequency X milliseconds (see above)		
		gyro.startTracking(function(o){
						
			ts=get_timestamp_now();			
			//the typing is not started yet			
			if (!typing_started){
				accel_before.push({"t": ts, "x": o.x, "y": o.y, "z": o.z});
				gyros_before.push({"t": ts, "a": o.alpha, "b": o.beta, "c": o.gamma});
				
				//checking if the buffer is full
				if (buffersize>=0 && (buffersize < accel_before.length || buffersize < gyros_before.length)){
					accel_before.shift(); //removing the first element
					gyros_before.shift(); //removing the first element
				}
			}
			//the typing is already started
			if (typing_started){
				accel_typing.push({"t": ts, "x": o.x, "y": o.y, "z": o.z});
				gyros_typing.push({"t": ts, "a": o.alpha, "b": o.beta, "c": o.gamma});
			}
		
		console_log("SENSORS: stop tracking sensors at "+get_timestamp_now());
		}
		);
	}
	else{
		console_log("SENSOR: not able to start tracking sensors at "+get_timestamp_now());
	}
}

 
