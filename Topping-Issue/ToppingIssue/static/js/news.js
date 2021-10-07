// user-setting
$(document).ready(function (){
	$(".setting-button").click(function (){
  	$("#date-setting").toggle();
    $("#interest-setting").toggle();
    $("#complete-button").toggle();
  });
});

// 기간별 토픽 차트
$(document).ready(function () {
  new Chart(document.getElementById("term-topic-chart"), {
    type: 'line',
    data: {
			labels: [
				'data1',
				'',
				'',
				'data4',
				'',
				'',
				'data7'
			],
			datasets: [{
				label: 'My First dataset',
				backgroundColor: 'rgba(75, 192, 192, 1)',
				borderColor: 'rgba(75, 192, 192, 1)',
				fill: false,
        pointRadius: 1,
        lineTension: 0.5,  
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
        pointRadius: 1,
        lineTension: 0.5,
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
      plugins:{
        legend: {
          display: false
        },
      },
      scales: {
        x:{
          grid: {
            display: false,
          },
        },
        y: {
          display: false,
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
        datasets: [{
          backgroundColor: ["#DEF2F3", "#F1B6AF","#EAE6E6"],
          data: [2478,5267,734]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });

    new Chart(document.getElementsByClassName("daum-chart")[i], {
        type: 'doughnut',
        data: {
          datasets: [{
            backgroundColor: ["#DEF2F3", "#F1B6AF","#EAE6E6"],
            data: [2478,5267,734]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        }
    });
  }
});



