console.log(document.getElementById('news').innerHTML);

var news_json = JSON.parse(document.getElementById('news').innerHTML);

var parent_row = document.getElementById('news-table');

for (const object of Object.entries(news_json)) {
  	var tr = document.createElement('tr');
  	var td1 = document.createElement('td');
  	var td2 = document.createElement('td');
  	var td3 = document.createElement('td');
  	var a = document.createElement('a');

	td1.innerHTML = object[1]['publisher'];
	console.log(td1)
	td2.innerHTML = object[1]['title'];

	a.innerHTML = "Link";
	a.href = object[1]['link'];
	a.target = "_blank";
	td3.appendChild(a)

	tr.appendChild(td1)
	tr.appendChild(td2)
	tr.appendChild(td3)

	parent_row.appendChild(tr);
};