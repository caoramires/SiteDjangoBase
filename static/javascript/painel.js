  <script>
        // Access data from the template context

<!--        function loadJson(selector) {-->
<!--            return JSON.parse(document.querySelector(selector).getAttribute('chart_data'));-->
<!--            }-->

<!--            var jsonData = loadJson('#jsonData');-->

<!--            var datasets = jsonData.map((item) => item.datasets);-->
<!--            var labels = jsonData.map((item) => item.labels);-->


//        const labels = JSON.parse(document.getElementById('labels').textContent);
//        const datasets = JSON.parse(document.getElementById('datasets').textContent);

            const labels = ["IDENTIFICAR", "PROTEGER", "DETECTAR", "RESPONDER", "RECUPERAR"]
            const datasets =[{ "label": "Sim", "data": [15, 3, 9, 13, 5, 6]}, {"label": "Não","data": [11, 5, 1, 10, 2, 5]}, {"label": "EmP","data": [12, 5, 1, 18, 4, 7]}]

<!--         document.getElementById("demo").innerHTML = labels-->
<!--        document.getElementById("demo2").innerHTML = datasets-->


        // Create the Chart.js chart
        const ctx = document.getElementById('myChart').getContext('2d');

        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets:  datasets
            },
            options: {
                plugins: {
                    legend: {
                        position: 'bottom'
                        },
                        title: {
                            display: true,
                            text: 'Totais por Dimensão'
                        }

                 },
                scales: {
                    x: {
                        stacked: true // Enable stacking for bars
                    },
                    y: {
                        stacked: true // Enable stacking for bars
                    }
                }
            }
        });

         // Segundo Chart - Horizontal
        const ctx2 = document.getElementById('myChart2').getContext('2d');

         const labels2 = ["IDENTIFICAR", "PROTEGER", "DETECTAR", "RESPONDER", "RECUPERAR"]
         const datasets2 =[{ "label": "Sim", "data": [15, 3, 9, 13, 5, 6]}, {"label": "Não","data": [11, 5, 1, 10, 2, 5]}, {"label": "Atrasado","data": [12, 5, 1, 18, 4, 7]}]



        const chart2 = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: labels2,
                datasets:  datasets2
            },
                options: {
                    indexAxis: 'y',
                    scales: {
                            x: {
                              stacked: true
                            },
                            y: {
                              stacked: true
                            }
                          },
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                      title: {
                        display: true,
                        text: 'Ações por Dimensão'
                      }
                    }
                  },

           });

    </script>