ymaps.ready(init);

function init(){
	var myMap = new ymaps.Map('map', {
		center: [59.932603, 30.302410],
		zoom: 15});


	document.getElementById('btnSearch').onclick = function() {
      // Строка с адресом, который необходимо геокодировать
    //var address = encodeURIComponent(document.getElementById("InAddress").value);
	var address = document.getElementById("InAddress").value;
    var geocoder = ymaps.geocode(address, {kind: 'house', results: 1});
	var listAddr = [];
	var commIndex = 0;
	var tableHeader = '<table id = "ResTable" style = "outline: 2px solid grey;"><tr><th>№</th><th>Адрес</th><th>Категория</th><th>Координаты</th><th>Расстояние, м</th><th>Время</th></tr>';
	var tableFoot = "</table>";
	var tableRow = '';
    // После того, как поиск вернул результат, вызывается callback-функция
    geocoder.then(
        function (res) {
			var coordinates = res.geoObjects.get(0).geometry.getCoordinates();
			// Новый запрос на этот раз по координатам первого объекта. Находим все объекты вокруг.
			ymaps.geocode(coordinates, {kind: 'house', results: 100, boundedBy: [[59.927075, 30.418989], [59.933627, 30.430730]], strictsBounds: true}).then(
				function (res) {
					// Добавляем коллекцию найденных геообъектов на карту.
					myMap.geoObjects.add(res.geoObjects);
					// Масштабируем карту на область видимости коллекции.
					myMap.setBounds(res.geoObjects.getBounds());
					// Пишем результат в массив с адресами найденных точек
					try {
						res.geoObjects.each(function(el, i){
							var pointA = coordinates;
							var pointB = res.geoObjects.get(i).geometry.getCoordinates();
							commIndex = i;
							tableRow += '<tr style = "border: 1px solid grey;">';
							tableRow += '<td style = "border: 1px solid grey;">'+(i)+'</td>';
							tableRow += '<td style = "border: 1px solid grey;">'+res.geoObjects.get(i).getAddressLine()+'</td>';
							tableRow += '<td style = "border: 1px solid grey;">house</td>';
							tableRow += '<td style = "border: 1px solid grey;">'+res.geoObjects.get(i).geometry.getCoordinates()+'</td>';
							tableRow += '<td style = "border: 1px solid grey; text-align: center;"><div id = "dist_r'+i+'"></div></td>';
							tableRow += '<td style = "border: 1px solid grey;"><div id = "dur_r'+i+'"></div></td>';
							// Кнопка расчета показателей для отдельной строки
							tableRow += '<td style = "border: 1px solid grey;"><a id = "get_r'+i+'"href="#dist_r'+i+'" onclick="ShowRoute(['+pointA+'], ['+pointB+'], '+i+');"\>...</a></td>';
							tableRow += '</tr>'});
							}
					catch(err){
						document.getElementById('outputpanel').innerHTML = "Ничего не найдено";
					}
					//commIndex = commIndex+1;
					// Ищем ближайшие станции метро
					ymaps.geocode(coordinates, {kind: 'metro', results: 3}).then(
					function (res) {
					// Добавляем коллекцию найденных геообъектов на карту.
					//myMap.geoObjects.add(res.geoObjects);
					// Масштабируем карту на область видимости коллекции.
					//myMap.setBounds(res.geoObjects.getBounds());
					// Пишем результат в массив с адресами найденных точек
					try {
						res.geoObjects.each(function(el, i){
							var pointA = coordinates;
							var pointB = res.geoObjects.get(i).geometry.getCoordinates();
							commIndex = commIndex+1;
							tableRow += '<tr style = "border: 1px solid grey; color: blue;">';
							tableRow += '<td style = "border: 1px solid grey;">'+(commIndex)+'</td>';
							tableRow += '<td style = "border: 1px solid grey;">'+res.geoObjects.get(i).getAddressLine()+'</td>';
							tableRow += '<td style = "border: 1px solid grey;">metro</td>';
							tableRow += '<td style = "border: 1px solid grey;">'+res.geoObjects.get(i).geometry.getCoordinates()+'</td>';
							tableRow += '<td style = "border: 1px solid grey; text-align: center;"><div id = "dist_r'+commIndex+'"></div></td>';
							tableRow += '<td style = "border: 1px solid grey;"><div id = "dur_r'+commIndex+'"></div></td>';
							// Кнопка расчета показателей для отдельной строки
							tableRow += '<td style = "border: 1px solid grey;"><a id = "get_r'+commIndex+'"href="#dist_r'+commIndex+'" onclick="ShowRoute(['+pointA+'], ['+pointB+'], '+commIndex+');"\>...</a></td>';
							tableRow += '</tr>'});
							}
					catch(err){
						document.getElementById('outputpanel').innerHTML = "Ничего не найдено";
					}
					// Вычисляем объекты конкурентов
					var n = document.getElementById("objectType").options.selectedIndex;
					var searchControl = new ymaps.control.SearchControl({options: {provider: 'yandex#search'}})
					myMap.controls.add(searchControl);
					searchControl.search(document.getElementById("objectType").options[n].value).then(
						function(res) {
							var results = searchControl.getResultsArray();
							try {
								for(i=0; i < searchControl.getResultsCount(); i++) {
								//	alert(searchControl.getResultsCount());
								commIndex = commIndex+1;
								var pointA = coordinates;
								var pointB = results[i].geometry.getCoordinates();
								tableRow += '<tr style = "border: 1px solid grey; color: red;">';
								tableRow += '<td style = "border: 1px solid grey;">'+(commIndex)+'</td>';
								tableRow += '<td style = "border: 1px solid grey;"><b>'+results[i].properties.get('name')+'</b>, '+results[i].properties.get('description')+'</td>';
								tableRow += '<td style = "border: 1px solid grey;">competitor</td>';
								tableRow += '<td style = "border: 1px solid grey;">'+results[i].geometry.getCoordinates()+'</td>';
								tableRow += '<td style = "border: 1px solid grey; text-align: center;"><div id = "dist_r'+commIndex+'"></div></td>';
								tableRow += '<td style = "border: 1px solid grey;"><div id = "dur_r'+commIndex+'"></div></td>';
								// Кнопка расчета показателей для отдельной строки
								tableRow += '<td style = "border: 1px solid grey;"><a id = "get_r'+commIndex+'"href="#dist_r'+commIndex+'" onclick="ShowRoute(['+pointA+'], ['+pointB+'], '+commIndex+');"\>...</a></td>';
								tableRow += '</tr>';
								};
							}
							catch(err){
								document.getElementById('outputpanel').innerHTML = "Ничего не найдено";
							}

							// Закончили вычислять объекты конкурентов
								//Ищем остановки общественного транспорта
								searchControl.search('Остановка общественного транспорта').then(
										function(res) {
									var results = searchControl.getResultsArray();
									try {
										for(i=0; i < searchControl.getResultsCount(); i++) {
											commIndex = commIndex+1;
											var pointA = coordinates;
											var pointB = results[i].geometry.getCoordinates();
											tableRow += '<tr style = "border: 1px solid grey; color: green;">';
											tableRow += '<td style = "border: 1px solid grey;">'+(commIndex)+'</td>';
											tableRow += '<td style = "border: 1px solid grey;"><b>'+results[i].properties.get('name')+'</b>, '+results[i].properties.get('description')+'</td>';
											//tableRow += '<td style = "border: 1px solid grey;">'+JSON.stringify(results[i].properties.getAll())+'</td>';
											tableRow += '<td style = "border: 1px solid grey;">bus stop</td>';
											tableRow += '<td style = "border: 1px solid grey;">'+results[i].geometry.getCoordinates()+'</td>';
											tableRow += '<td style = "border: 1px solid grey; text-align: center;"><div id = "dist_r'+commIndex+'"></div></td>';
											tableRow += '<td style = "border: 1px solid grey;"><div id = "dur_r'+commIndex+'"></div></td>';
											// Кнопка расчета показателей для отдельной строки
											tableRow += '<td style = "border: 1px solid grey;"><a id = "get_r'+commIndex+'"href="#dist_r'+commIndex+'" onclick="ShowRoute(['+pointA+'], ['+pointB+'], '+commIndex+');"\>...</a></td>';
											tableRow += '</tr>';
									};
								}
									catch(err){
										document.getElementById('outputpanel').innerHTML = "Ничего не найдено";
									}
								document.getElementById('outputpanel').innerHTML = tableHeader + tableRow + tableFoot;
								document.getElementById('info').innerHTML = "Поиск успешно завершен";
						});
							document.getElementById('outputpanel').innerHTML = tableHeader + tableRow + tableFoot;
							document.getElementById('info').innerHTML = "Поиск успешно завершен";
					});
					// Закончили исткать остановки
					document.getElementById('outputpanel').innerHTML = tableHeader + tableRow + tableFoot;
					document.getElementById('info').innerHTML = "Поиск успешно завершен";
				});
				document.getElementById('outputpanel').innerHTML = tableHeader + tableRow + tableFoot;
				document.getElementById('info').innerHTML = "Поиск успешно завершен";
				});

		});
	};
};