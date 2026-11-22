(function(){var D=[["l","p01.html","翦网"],["l","p02.html","渐"],["l","p03.html","立达五周年纪念感想"],["l","p04.html","自然"],["l","p05.html","颜面"],["l","p06.html","儿女"],["l","p07.html","闲居"],["l","p08.html","从孩子得到的启示"],["l","p09.html","天的文学"],["l","p10.html","东京某晚的事"],["l","p11.html","楼板"],["l","p12.html","姓"],["l","p13.html","忆儿时"],["l","p14.html","华瞻的日记"],["l","p15.html","阿难"],["l","p16.html","晨梦"],["l","p17.html","艺术三昧"],["l","p18.html","缘"],["l","p19.html","大账簿"],["l","p20.html","秋"],["l","p21.html","告缘缘堂在天之灵"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
