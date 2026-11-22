(function(){var D=[["l","p01.html","在桥梁工地上"],["l","p02.html","爬在旗杆上的人"],["l","p03.html","本报内部消息"],["l","p04.html","本报内部消息（续篇）"],["l","p05.html","在悬崖上"],["l","p06.html","组织部新来的青年人"],["l","p07.html","小巷深处"],["l","p08.html","平原的颂歌"],["l","p09.html","太阳的家乡"],["l","p10.html","沉默"],["l","p11.html","草木篇"],["l","p12.html","科长"],["l","p13.html","寒夜的别离"],["l","p14.html","西苑草"],["l","p15.html","被围困的农庄主席"],["l","p16.html","入党"],["l","p17.html","杨妇道"],["l","p18.html","改选"],["l","p19.html","红豆"],["l","p20.html","美丽"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
