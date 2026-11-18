(function(){var D=[["l","p01.html","前言"],["g","编年诗"],["l","p02.html","题友人云母障子—偶然作（五首选三）"],["l","p03.html","淇上即事田园—送邢桂州"],["l","p04.html","千塔主人—和太常韦主簿五郎温汤寓目"],["l","p05.html","冬日游览—春园即事"],["l","p06.html","山居即事—冬晚对雪忆胡居士家"],["g","未编年诗"],["l","p07.html","扶南曲歌词五首—送沈子福归江东"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
