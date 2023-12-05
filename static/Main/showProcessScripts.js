function drawVSMLine(elementId, lastElementID) {
	var element = document.getElementById('VSMContainer'+elementId);
	var lastElement = document.getElementById('VSMContainer'+lastElementID);
	var elementRect = element.getBoundingClientRect();
	var lastElementRect = lastElement.getBoundingClientRect();
	var elementCentreX = elementRect.right - elementRect.left;
	var elementCentreY = elementRect.bottom - elementRect.top;
	var lastElementCentreX = lastElementRect.right - lastElementRect.left;
	var lastElementCentreY = lastElementRect.bottom - lastElementRect.top;
	var canvas = document.getElementById("cards");
	var ctx = canvas.getContext("2d");
	
	ctx.beginPath();
	ctx.moveTo(elementCentreX, elementCentreY);
	ctx.lineTo(lastElementCentreX, lastElementCentreY);
	ctx.stroke();
}

function getCookie(cname) { //used to parse CSRF token (security)
     var name = cname + "=";
     var ca = document.cookie.split(';');
     for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if(c.indexOf(name) == 0)
           return c.substring(name.length,c.length);
     }
     return "";
     }

function popUpFunction(subProcessId) { //gets popup element and shows it
	var popup = document.getElementById("myPopup" + subProcessId);
	popup.classList.toggle("show");
}	

function sensorPopUpFunction(sensorId) { //getes sensor popup element and shows it
	var popup = document.getElementById("sensorPopup" + sensorId);
	popup.classList.toggle("show");
}		

function createNewGraph(id) {
		  const canvas = document.createElement("canvas"); //creates new canvas to be used for multiple graphs
		  canvas.id = "temp-graph"+id;
		  document.getElementById("test"+id).appendChild(canvas);
  		 

  			}

 
function createNewPressureGraph(id) {
		  const canvas = document.createElement("canvas"); //creates new canvas to be used for multiple graphs
		  canvas.id = "pressure-graph"+id;
		  document.getElementById("pressureTest"+id).appendChild(canvas);
		
  			}
  		 
  		  

  			
  	function temp(id) {
							   var $id = id;
								var $tempGraph = $("#temp-graph"+id);
								$.ajax({
						        url: "popUp"+$id,
						        success: function (data) {
						         // var url = $tempGraph.data("url"); //data url for obtaining required data
						  
						         var url = "popUp"+$id;
						          var ctx = $tempGraph[0].getContext("2d");
						          
						          new Chart(ctx, {
						            type: 'line',
						           // labels:data.initialTempTime,
						            data: {
						            	//labels: data.newList,
						              datasets: [{
											 label: 'Temperature over time',                
						                backgroundColor: 'red',
						                borderColor: 'red',
						                borderWidth: 1.5,
						                data: data.initialTempData,
						              }]          
						            },
						            options: {
						              elements:{
						                  point:{
						                    radius: 0 //removing points from line graph
						                  },
						                },
						              plugins: {
						                autocolors: false,
						                annotation: { //annotation plugin used for displaying min/max lines
						                  annotations: {
						                  	//annotation plugin for adding min/max lines
						                    line1: {
						                      type: 'line',
						                      yMin: data.temperatureData.minTemp,
						                      yMax: data.temperatureData.minTemp,
						                      borderColor: 'rgb(0, 255, 0)',
						                      borderWidth: 2,
						
						                      label : {
						                        display: true,
						                        position: 'center',
						                        content: 'Min',
						                      }
						                    },
						                    line2: {
						                      type: 'line',
						                      yMin: data.temperatureData.maxTemp,
						                      yMax: data.temperatureData.maxTemp,
						                      borderColor: 'rgb(24, 150, 138)',
						                      borderWidth: 2,
						
						                      label: {
						                        display: true,
						                        position: 'center',
						                        content: 'Max',
						                     },
						                     ellipse1: {
		                     				 display:true,
													 type: 'ellipse',
													 xMin: 0 ,
													 xMax: 0,
													 yMin: 3,
													 yMax:  7,
													 backgroundColor: 'rgba(99, 255, 132, 0.25)'
													}
						                    },
						
						                  }
						                }
						              },
						
						
						            	scales: {
						                y: {
						                  
						                    min: -5,
						                    max: 15,
						                
						              },
												x:{
												
													display:false,
						              type: 'realtime',//using chart.js streaming-plugin to show real-time data
						                  realtime:{
						                  	duration: 60000,  // data in the past 20000 ms will be displayed
						                    refresh: 1500,    // onRefresh callback will be called every 1000 ms
						                    delay: 1500,      // delay of 1000 ms, so upcoming values are known before plotting a line
						                    pause: data.jobEnd,     // chart is not paused
						                    ttl: 10000000000,  // data will be automatically deleted as it disappears off the chart
						                    frameRate: 60,  // chart is drawn 5 times every second 
						                    onRefresh: async function(chart){ //refreshes once per second
														data = await fetch(url, { //fetching data using POST+crsf token for security
														method: "POST",
														headers: {
														"X-CSRFToken": getCookie("csrftoken"),},}) //cleaning/parsing csrf DATA
														.then(response => response.json())
														.then(data => { //gathered data = data
													  //gathered data = data
													//  console.log(data.tempReached)
													console.log(data)
													 chart.options.scales.x.realtime.refresh = data.refreshRate;
													 chart.options.scales.x.realtime.pause = data.jobEnd;

											    	chart.update('quiet');

						                      	
						                      if (data.jobEnd == false){
						                      	chart.data.datasets.forEach(async function(dataset) {		
						                      	//console.log(1)	                
						                        dataset.data.push({
						                          x: data.temperatureData['time'],
						                          y: data.temperatureData[id], //assigns current temp value to line graph
							
						                        })
						                        chart.update('quiet');
						                    
						                      
													})
						                      		//if(data.tempReached == true){
													  			//chart.options.plugins.annotation.annotations.label1.content = ['Temperature reached here', data.tempReachedTime];
													  			//chart.options.plugins.annotation.annotations.label1.xValue= data.tempReachedTime;
													  			//chart.options.plugins.annotation.annotations.ellipse1.display= true;
													  			chart.options.plugins.annotation.annotations.ellipse1={
													  				type:'ellipse',
													  				xMax: data.ellipseSupport,
													  				xMin : data.tempReachedTime,
													  				yMin: 3,
																	 yMax:  7,
																	 backgroundColor: 'rgba(99, 255, 132, 0.25)'

													  		//	}
													  			
																	
													  			
						                      		}

						                      
						                       } else {
						                       
						                       	chart.options={
						                      
						           // labels:data.initialTempTime,
						     
						            
						                       	
						            
						                       		elements:{
										                  point:{
										                    radius: 0 //removing points from line graph
										                  },
										                },
										                plugins: {
										                autocolors: false,
										                annotation: { //annotation plugin used for displaying min/max lines
										                  annotations: {
										                  	//annotation plugin for adding min/max lines
										                    line1: {
										                      type: 'line',
										                      yMin: data.temperatureData.minTemp,
										                      yMax: data.temperatureData.minTemp,
										                      borderColor: 'rgb(0, 255, 0)',
										                      borderWidth: 2,
										
										                      label : {
										                        display: true,
										                        position: 'center',
										                        content: 'Min',
										                      }
										                    },
										                    line2: {
										                      type: 'line',
										                      yMin: data.temperatureData.maxTemp,
										                      yMax: data.temperatureData.maxTemp,
										                      borderColor: 'rgb(24, 150, 138)',
										                      borderWidth: 2,
										
										                      label: {
										                        display: true,
										                        position: 'center',
										                        content: 'Max',
										                     }
										                    },
										                    ellipse1: {
																	 type: 'ellipse',
																	 xMin: data.cleanedTempReachedTime-6 ,
																	 xMax: data.cleanedTempReachedTime - 9,
																	 yMin: 3,
																	 yMax:  7,
																	 backgroundColor: 'rgba(99, 255, 132, 0.25)'
																	}
										
										                  }
										                }
										              },
						                       		scales: {
						                       			x: {
						                       				display:true,
						                       			//beginAtZero: true,
						                       			

						                       		


						                       			},
						                       			y:{
						                       				min: -5,
						                       				max: 15,
						                       			}
						                       		}


						                       	}
						                       
						           
										                 }
										                
										                        
										                     })
										                 
										                   }
										                  }
										
										           }   
										          
										             },
										           
										              
						         
						            }
						          });
						        }
						      });
						    };		
						  
function pressure(id) {
							   var $id = id;
								var $pressureGraph = $("#pressure-graph"+id);
								$.ajax({
						        url: "popUp"+$id,
						        success: function (data) {
						         // var url = $tempGraph.data("url"); //data url for obtaining required data
						         var url = "popUp"+$id;
						          var ctx = $pressureGraph[0].getContext("2d");
						          
						          new Chart(ctx, {
						            type: 'line',
						            
						            data: {
						           // labels:data.testData.x,

						              datasets: [{
						              	 label: 'Pressure Over Time',

						              	 backgroundColor: 'rgb(75, 192, 192)',

										    fill: false,

										    borderWidth: 1.5,
										    borderColor: 'rgb(75, 192, 192)',

		
										   data: data.initialPressureData, }]          
						            },
						            options: {
						           
						            	
						              elements:{
						                  point:{
						                    radius: 0 //removing points from line graph
						                  },
						                },
						              plugins: {
						                autocolors: false,
						                annotation: { //annotation plugin used for displaying min/max lines
						                  annotations: {
						                  	//annotation plugin for adding min/max lines
						                    line1: {
						                      type: 'line',
						                      yMin: data.pressureData.maxPressure,
						                      yMax: data.pressureData.maxPressure,
						                      borderColor: 'rgb(0, 255, 0)',
						                      borderWidth: 2,
						
						                      label : {
						                        display: true,
						                        position: 'center',
						                        content: 'Min',
						                      }
						                    },
						                    line2: {
						                      type: 'line',
						                      yMin: data.pressureData.minPressure,
						                      yMax: data.pressureData.minPressure,
						                      borderColor: 'rgb(24, 150, 138)',
						                      borderWidth: 2,
						
						                      label: {
						                        display: true,
						                        position: 'center',
						                        content: 'Max',
						                     }
						                    },
						                      ellipse1: {
		                     				display:true,
													 type: 'ellipse',
													 xMin: 0 ,
													 xMax: 0,
													 yMin: 5,
													 yMax:  9,
													 backgroundColor: 'rgba(196, 23, 23, 0.25)'
													}
						                  }
						                }

						             },
						
						
						            	scales: {
						               y:{
						               	min: -5,
						               	max: 15,
						               },
						                
												x:{
													display:false,
													//display:false,
						              type: 'realtime',//using chart.js streaming-plugin to show real-time data
						                  realtime:{
						                  duration: 60000,  // data in the past 20000 ms will be displayed
							                refresh: 1500,    // onRefresh callback will be called every 1000 ms
							                delay: 1500,      // delay of 1000 ms, so upcoming values are known before plotting a line
							                pause: data.jobEnd,     // chart is not paused
							                ttl: 10000000000,   // data will be automatically deleted as it disappears off the chart
							                frameRate: 60,  // chart is drawn 5 times every second 
						                    onRefresh: async function(chart){ //refreshes once per second
						                      data = await fetch(url, { //fetching data using POST+crsf token for security
													  method: "POST",
													  headers: {
													  "X-CSRFToken": getCookie("csrftoken"),},}) //cleaning/parsing csrf DATA
											    .then(response => response.json())
											    .then(data => {
											    	chart.options.scales.x.realtime.refresh = data.refreshRate;
											    	chart.options.scales.x.realtime.pause = data.jobEnd;
											    	chart.update('quiet')
											    	

											     //gathered data = data
						                      if (data.jobEnd == false){
						                      	

						                      chart.data.datasets.forEach(async function(dataset) {
						                   //   	console.log(data.pressureReached)
		


						                        dataset.data.push({
						                          x: data.pressureData['time'],
						                          y: data.pressureData[id], //assigns current temp value to line graph)

						                        })

						                        chart.update('quiet')
						                    
						                      
														})

						                      if(data.ellipseSupportPressure!= ''){
						
													  			chart.options.plugins.annotation.annotations.ellipse1={
													  				type:'ellipse',
													  				xMax: data.ellipseSupportPressure,
													  				xMin : data.pressureReachedTime,
													  				 yMin: 5,
																	 yMax:  9,
																	 backgroundColor: 'rgba(196, 23, 23, 0.25)'

													  			}
										
						                      		}
						                       } else {
						                       
						                       	chart.options={
						                       		elements:{
											                  point:{
											                    radius: 0 //removing points from line graph
											                  },
											                },
						                       		scales: {
						                       			x: {
						                       				display:true,
						                       				

						                       				
						                       			},
						                       			y:{
						                       				min: -5,
						                       				max: 15,
						                       			},
						                       		},
						                        plugins: {

						                autocolors: false,
						                annotation: { //annotation plugin used for displaying min/max lines
						                  annotations: {
						                  	//annotation plugin for adding min/max lines
						                    line1: {
						                      type: 'line',
						                      yMin: data.pressureData.maxPressure,
						                      yMax: data.pressureData.maxPressure,
						                      borderColor: 'rgb(0, 255, 0)',
						                      borderWidth: 1.5,
						
						                      label : {
						                        display: true,
						                        position: 'center',
						                        content: 'Min',
						                      }
						                    },
						                    line2: {
						                      type: 'line',
						                      yMin:  data.pressureData.minPressure,
						                      yMax:  data.pressureData.minPressure,
						                      borderColor: 'rgb(24, 150, 138)',
						                      borderWidth: 1.5,
						
						                      label: {
						                        display: true,
						                        position: 'center',
						                        content: 'Max',
						                     }
						                    },
						                    ellipse1: {
																	 type: 'ellipse',
																	 xMin: data.cleanedPressureReachedTime-6 ,
																	 xMax: data.cleanedPressureReachedTime - 9,
																	 yMin: 5,
																	 yMax:  9,
																	 backgroundColor: 'rgba(196, 23, 23, 0.25)'
																	}						                  
																}
						                }

						             },


						                       	}
						                      
						                     	// chart.data.datasets[0].data.push(data.initialPressureData);
						                     	// chart.update('quiet');
						                       
						                     }
						                     	//chart.update('quiet')
						                        
						                     })
						                 
						                   }
						                  }
						
						           }   
						          
						             },
						              
						              
						            
						              
						            }
						          })
						        }
						      });
						    }
						 //   })
						 //   }		