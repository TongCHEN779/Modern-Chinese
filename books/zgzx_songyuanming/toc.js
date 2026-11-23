(function(){var D=[["l","p01.html","编辑说明"],["l","p02.html","李觏"],["l","p03.html","邵雍"],["l","p04.html","周敦颐"],["l","p05.html","张载"],["l","p06.html","王安石"],["l","p07.html","程颢"],["l","p08.html","程颐"],["l","p09.html","朱熹"],["l","p10.html","陆九渊"],["l","p11.html","陈亮"],["l","p12.html","叶适"],["l","p13.html","邓牧"],["l","p14.html","罗钦顺"],["l","p15.html","王守仁"],["l","p16.html","王廷相"],["l","p17.html","王艮"],["l","p18.html","李贽"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
