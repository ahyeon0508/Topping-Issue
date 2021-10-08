// user-setting
$(document).ready(function (){
	$(".setting-button").click(function (){
  	$("#date-setting").toggle();
    $("#interest-setting").toggle();
    $("#complete-button").toggle();
  });
});

// 기간별 토픽 차트
var keyword = [['관련어1', '관련어2'], ['관련어3', '관련어4']]

$(document).ready(function () {
  new Chart(document.getElementById("term-topic-chart"), {
    type: 'line',
    data: {
			labels: [
				'2021-04-24',
				'2021-04-25',
				'2021-04-26',
				'2021-04-27',
				'2021-04-28',
				'2021-04-29',
				'2021-04-30'
			],
			datasets: [{
				label: 'My First dataset',
				backgroundColor: 'rgba(75, 192, 192, 1)',
				borderColor: 'rgba(75, 192, 192, 1)',
				fill: false,
        pointRadius: 3,
				data: [
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50)
				],
			},
      {
				label: 'My Second dataset',
				backgroundColor: 'rgba(255, 99, 132, 1)',
				borderColor: 'rgba(255, 99, 132, 1)',
				fill: false,
        pointRadius: 3,
        data: [
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50),
					Math.floor(Math.random() * 50)
				],
			}]
		},
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      title: {
        display: true,
        text: '2021-04-24 ~ 2021-04-30',
        position: 'bottom',
      },
      scales: {
        xAxes: [{
          ticks: {
            display: false
          },
          gridLines: {
            display:false,
          }
        }],
        yAxes: [{
          display: false
        }]
      },
      tooltips: {
        callbacks: {
          label: function(tooltipItem, data) {
            return data.datasets[tooltipItem.datasetIndex].label + ' : ' + keyword[tooltipItem.datasetIndex]
          }
        }
      }
    }
  });
});

// N사, D사 감성 분석 차트
var section = document.getElementsByClassName("news-reaction-chart");

$(document).ready(function () {
  for(var i = 0; i < section.length; i++){
    new Chart(document.getElementsByClassName("naver-chart")[i], {
      type: 'doughnut',
      data: {
        labels: ['긍정', '부정', '중립'],
        datasets: [{
          backgroundColor: ["#DEF2F3", "#F1B6AF","#EAE6E6"],
          data: [2478,5267,734]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        plugins: {
          doughnutlabel: {
            labels: [
              {
                text: 'N사',
                font: {
                  size: '16',
                  weight: 'bold'
                },
              },
            ],
          },
        },
      }
    });

    new Chart(document.getElementsByClassName("daum-chart")[i], {
        type: 'doughnut',
        data: {
          labels: ['긍정', '부정', '중립'],
          datasets: [{
            backgroundColor: ["#DEF2F3", "#F1B6AF","#EAE6E6"],
            data: [2478,5267,734]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          legend: {
            display: false
          },
          plugins: {
            doughnutlabel: {
              labels: [
                {
                  text: 'D사',
                  font: {
                    size: '16',
                    weight: 'bold'
                  },
                },
              ],
            },
          },
        }
      });
    }
});



