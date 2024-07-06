
var pusher = new Pusher("a5728f3261909ddf0eba", {
    cluster: "ap2",
});
var channel = pusher.subscribe("sensor-data-channel");
console.log('subscribed to sensor-data-channel in channels');
channel.bind("sensor-data", (data) => {
    console.log(data);
});

var gauge_temp_options = {
	series: [0],
	colors: ['#34d399'],
	chart: {
		height: 300,
		width: 300,
		type: "radialBar",
	  },
	plotOptions: {
		radialBar: {
			startAngle: -135,
			endAngle: 135,
			track: {
				background: "#fff",
				strokeWidth: '90%',
				margin: 5, // margin is in pixels
				dropShadow: {
					enabled: true,
					top: 2,
					left: 0,
					color: '#999',
					opacity: 1,
					blur: 2
				}
			},
			dataLabels: {
				name: {
					show: true,
				},
				value: {
					fontSize: "16px",
					formatter: function(val){
						return val + ""
					}
				}
			}
		}
	},
	fill: {
		type: "gradient",
	  	gradient: {
			shade: "light",
			type: "horizontal",
			gradientToColors: ["#6ee7b7"],
			stops: [0, 100]
		},
	},
	labels: ['Temperature'],
  };
  
var gauge_humid_options = {
	series: [0],
	colors:['#38bdf8'],
	chart: {
		height: 300,
		width: 300,
		type: "radialBar",
	  },
	plotOptions: {
		radialBar: {
			startAngle: -135,
			endAngle: 135,
			track: {
				background: "#fff",
				strokeWidth: '90%',
				margin: 5, // margin is in pixels
				dropShadow: {
					enabled: true,
					top: 2,
					left: 0,
					color: '#999',
					opacity: 1,
					blur: 2
				}
			},
			dataLabels: {
				name: {
					show: true
				},
				value: {
					fontSize: '14px',
					formatter: function(val){
						return val + ""
					}
				}
			}
		}
	},
	fill: {
		type: "gradient",
	  	gradient: {
			shade: "light",
			type: "horizontal",
			gradientToColors: ["#7dd3fc"],
			stops: [0, 100]
		},
	},
	labels: ["Humidity"]
  };
  
const gauge_temp_chart = new ApexCharts(document.querySelector("#gauge-temp-chart"), gauge_temp_options);
gauge_temp_chart.render();
const gauge_humid_chart = new ApexCharts(document.querySelector("#gauge-humid-chart"), gauge_humid_options);
gauge_humid_chart.render();

var min_temp_ele = document.querySelector("#min-temp");
var max_temp_ele = document.querySelector("#max-temp");
var min_humid_ele = document.querySelector("#min-humid");
var max_humid_ele = document.querySelector("#max-humid");

document.addEventListener('DOMContentLoaded', function() {
	fetch('/api/initial-data/')
		.then(response => response.json())
		.then(data => {
			var initialTempData = data.initial_temp_data;
			var initialHumidityData = data.initial_humidity_data;

			// Initialize ApexCharts with initial data
			var area_options = {
				chart: {
					type: 'area',
					height: 400,
					width: 943,
					stacked: true,
					animations: {
						enabled: true,
						easing: 'easeinout',
						speed: 800,
						animateGradually: {
							enabled: true,
							delay: 150
						},
						dynamicAnimation: {
							enabled: true,
							speed: 350
						}
					}
				},
				series: [{
					name: 'Temperature',
					data: initialTempData
				}, 
				{
					name: 'Humidity',
					data: initialHumidityData
				}],
				xaxis: {
					type: 'datetime'
				},
				colors:["#00e396", "#008ffb"],
				dataLabels:{
					enabled: false
				},
				onItemClick: {
					toggleDataSeries: true
				},
				onItemHover: {
					highlightDataSeries: true
				},
			};
			const area_chart = new ApexCharts(document.querySelector("#area-chart"), area_options);
			area_chart.render();
		})
		.catch(error => console.error('Error fetching initial data:', error));

		fetch('/api/min-max-last-data/')
		.then(response => response.json())
		.then(data => {
			gauge_humid_chart.updateSeries([data.last_humid]);
			gauge_temp_chart.updateSeries([data.last_temp]);
			min_temp_ele.textContent = data.min_temp;
			max_temp_ele.textContent = data.max_temp;
			min_humid_ele.textContent = data.min_humid;
			max_humid_ele.textContent = data.max_humid;
		})
		.catch(error => console.error('Error fetching data:', error));
});
