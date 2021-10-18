$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});

// 기간별 토픽 차트
var termChartDate = JSON.parse(termChartDate);
var termChartsubData = JSON.parse(termChartsubData);

$(document).ready(function () {
  var ctx = document.getElementById('term-topic-chart');
  var config = {
    type: 'line',
    data: {
      labels: termChartDate,
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      title: {
        display: true,
        text: termChartDate[0] + " ~ " + termChartDate[termChartDate.length - 1],
        position: 'top',
        fontColor: "gray",
      },
      scales: {
        xAxes: [{
          ticks: {
            display: false
          },
          gridLines: {
            display: false,
          }
        }],
        yAxes: [{
          display: false
        }]
      },
      tooltips: {
        callbacks: {
          label: function (tooltipItem, data) {
            return "[" + data.datasets[tooltipItem.datasetIndex].label + "]"
          },
          afterLabel: function (tooltipItem) {
            return termChartsubData[tooltipItem.index][tooltipItem.datasetIndex]
          }
        }
      }
    }
  };

  var termTopicChart = new Chart(ctx, config);

  var color = ['rgba(185, 176, 255, 1)', 'rgba(255, 216, 176, 1)', 'rgba(255, 176, 176, 1)', 'rgba(176, 255, 178, 1)', 'rgba(176, 255, 249, 1)'];

  var keywords = Object.keys(JSON.parse(termChartData));
  for (var i = 0; i < keywords.length; i++) {
    var term_dataset = {
      label: [],
      borderColor: '',
      backgroundColor: '',
      data: [],
      fill: false
    }

    term_dataset.borderColor = color[i];
    term_dataset.backgroundColor = color[i];
    term_dataset.label = keywords[i];
    term_dataset.data = JSON.parse(termChartData)[keywords[i]];

    config.data.datasets.push(term_dataset);
    termTopicChart.update();
  }
});

// N사, D사 감성 분석 차트
var newsData = JSON.parse(newsData);
var newsData_keys = Object.keys(newsData);
var html = '';

function news_info(key){
  temp_html = '';
  for (var i = 0; i < newsData[key].length; i++){
    temp_html += '<div class="news-title" OnClick="location.href =\'' + newsData[key][1][i] + '\'">' + newsData[key][0][i] + '</div>'
  }
  return temp_html
}

function sub_news_info(m){
  temp_html = '<div class=sub-word-buttons>';
  for (var i = 0; i < subNewsData[m][0].length; i++){
    temp_html += '<button class="sub-word-button" data-toggle="tooltip" title="파생주제 ' + (i+1) + '등">' + subNewsData[m][0][i] + '</button>'
  }
  temp_html += '</div>'
  for (var i = 0; i < subNewsData[m][0].length; i++){
    temp_html +=  '<div class="sub-news-keyword"><div class="sub-news"><div class="sub-news-info"><p class="cluster-name">'+ subNewsData[m][0][i] + '</p>'
    for (var j = 0; j < subNewsData[m][1][i].length; j++){
      temp_html += '<div class="news-title" OnClick="location.href =\'' + subNewsData[m][2][i][j] + '\'">' + subNewsData[m][1][i][j] + '</div>'
    }
    temp_html += '</div><div class="sub-news-reaction-chart">' +
    '<div class="naver-news-reaction"><div class="naver"><canvas class="naver-subNews-chart"></canvas></div></div>' + 
    '<div class="daum-news-reaction"><div class="daum"><canvas class="daum-subNews-chart"></canvas></div></div>'
    temp_html += '</div></div></div></div>'
  }
  return temp_html
}

function news_chart(m){
  if (JSON.stringify(JSON.parse(N_sentimentData)[m-1]) == JSON.stringify([0, 0, 0])){
    new Chart(document.getElementsByClassName("naver-chart"), {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(N_sentimentData)[m-1]
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
                  size: '36',
                  weight: 'bold'
                },
              },
              {
                text: '- 관련 댓글이',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
              {
                text: '존재하지 않습니다 -',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
            ],
          },
        }
      }
    })
  }
  else{
    new Chart(document.getElementsByClassName("naver-chart"), {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(N_sentimentData)[m-1]
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
  }
  if (JSON.stringify(JSON.parse(D_sentimentData)[m-1]) == JSON.stringify([0, 0, 0])){
    new Chart(document.getElementsByClassName("daum-chart"), {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(D_sentimentData)[m-1]
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
                  size: '36',
                  weight: 'bold'
                },
              },
              {
                text: '- 관련 댓글이',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
              {
                text: '존재하지 않습니다 -',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
            ],
          },
        }
      }
    })
  }
  else{
    new Chart(document.getElementsByClassName("daum-chart"), {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(D_sentimentData)[m-1]
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
}

function sub_news_chart(i, j){
  if (JSON.stringify(JSON.parse(N_sub_sentimentData)[i][j]) == JSON.stringify([0, 0, 0])) {
    if (window.n_chartObj != undefined){
      window.n_chartObj.destroy();
    }
    window.n_chartObj = new Chart(document.getElementsByClassName("naver-subNews-chart")[j], {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(N_sub_sentimentData)[i][j]
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
                  size: '36',
                  weight: 'bold'
                },
              },
              {
                text: '- 관련 댓글이',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
              {
                text: '존재하지 않습니다 -',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
            ],
          },
        }
      }
    })
  }
  else{
    if (window.n_chartObj != undefined){
      window.n_chartObj.destroy();
    }
    window.n_chartObj = new Chart(document.getElementsByClassName("naver-subNews-chart")[j], {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(N_sub_sentimentData)[i][j]
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
  }
  if (JSON.stringify(JSON.parse(D_sub_sentimentData)[i][j]) == JSON.stringify([0, 0, 0])) {
    if (window.d_chartObj != undefined){
      window.d_chartObj.destroy();
    }
    window.d_chartObj = new Chart(document.getElementsByClassName("daum-subNews-chart")[j], {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(D_sub_sentimentData)[i][j]
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
                  size: '36',
                  weight: 'bold'
                },
              },
              {
                text: '- 관련 댓글이',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
              {
                text: '존재하지 않습니다 -',
                font: {
                  size: '18',
                  weight: 'bold'
                },
              },
            ],
          },
        }
      }
    })
  }
  else{
    if (window.d_chartObj != undefined){
      window.d_chartObj.destroy();
    }
    window.d_chartObj = new Chart(document.getElementsByClassName("daum-subNews-chart")[j], {
      type: 'doughnut',
      data: {
        labels: ['부정', '긍정', '판별불가'],
        datasets: [{
          backgroundColor: ["#F1B6AF", "#DEF2F3", "#EAE6E6"],
          data: JSON.parse(D_sub_sentimentData)[i][j]
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
  window.n_chartObj.canvas.parentNode.style.width = '250px';
  window.n_chartObj.canvas.parentNode.style.height = '125px';
  window.d_chartObj.canvas.parentNode.style.width = '250px';
  window.d_chartObj.canvas.parentNode.style.height = '125px';
}

function fnMove(){
  var offset = $(".content").offset();
  $('html, body').animate({scrollTop : offset.top}, 400);
}

$(document).ready(function () {
  $(".content").hide()
  for (var i = 0; i < 11; i++) {
    (function (m) {
      $("#top-news-" + (m)).click(function () {
        html = '';
        $(".content").empty();
        $(".content").hide()
        html += '<div class="news-info"><p class="cluster-name">' + newsData_keys[m-1] + '</p>'
        html += news_info(newsData_keys[m-1]) + '</div>'
        html += '<div class="news-reaction-chart">' + 
        '<div class="naver-news-reaction"><div class="naver"><canvas class="naver-chart"></canvas></div></div>' + 
        '<div class="daum-news-reaction"><div class="daum"><canvas class="daum-chart"></canvas></div></div></div>'
        html += sub_news_info(m-1)
        if ($(".content").is(':empty')){
          $(".content").toggle()
          $(".content").append(html);
          news_chart(m);
          $(".sub-news-keyword").hide();
          $(".sub-word-button").click(function () {
            if ($(this).index() == 0){
              $('.sub-news-keyword').eq(1).hide();
              $('.sub-news-keyword').eq(0).toggle();
              sub_news_chart(m-1, $(this).index())
              $('[data-toggle="tooltip"]').tooltip();
            }
            else {
              $('.sub-news-keyword').eq(0).hide();
              $('.sub-news-keyword').eq(1).toggle();
              sub_news_chart(m-1, $(this).index())
            }
          });
          fnMove()
        }
      });
    })(i);
  }
});