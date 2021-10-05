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



