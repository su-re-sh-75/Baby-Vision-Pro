var pusher = new Pusher("a5728f3261909ddf0eba", {
    cluster: "ap2",
});
var channel = pusher.subscribe("sensor-data-channel");
console.log('subscribed to sensor-data-channel in channels');
channel.bind("sensor-data", (data) => {
    console.log(data);
});

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
			var chart = new ApexCharts(document.querySelector("#area-chart"), area_options);
			chart.render();
		})
		.catch(error => console.error('Error fetching initial data:', error));
});
var gauge_temp_options = {
	chart: {
	  height: 280,
	  width: "50%",
	  type: "radialBar",
	},
	series: [67],
	colors: ["#20E647"],
	plotOptions: {
	  radialBar: {
		startAngle: -135,
		endAngle: 135,
		track: {
		  background: '#333',
		  startAngle: -135,
		  endAngle: 135,
		},
		dataLabels: {
		  name: {
			show: true,
		  },
		  value: {
			fontSize: "30px",
			show: true
		  }
		}
	  }
	},
	fill: {
	  type: "gradient",
	  gradient: {
		shade: "dark",
		type: "horizontal",
		gradientToColors: ["#87D4F9"],
		stops: [0, 100]
	  }
	},
	stroke: {
	  lineCap: "butt"
	},
	labels: ["Progress"]
  };
  
  new ApexCharts(document.querySelector("#gauge-temp-chart"), gauge_temp_options).render();
  new ApexCharts(document.querySelector("#gauge-humid-chart"), gauge_temp_options).render();