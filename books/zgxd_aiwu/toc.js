(function(){var D=[["l","p01.html","序"],["g","作品部份"],["l","p02.html","人生哲学的一课"],["l","p03.html","山峡中"],["l","p04.html","山中送客记"],["l","p05.html","乌鸦之歌"],["l","p06.html","瞎子客店"],["l","p07.html","我的旅伴"],["l","p08.html","月夜"],["l","p09.html","回家"],["l","p10.html","石青嫂子"],["l","p11.html","夜归"],["l","p12.html","雨"],["l","p13.html","红艳艳的罂粟花"],["l","p14.html","关于小说题材与鲁迅的通信"],["l","p15.html","墨水瓶挂在颈子上写作的"],["g","资料部份"],["l","p16.html","艾芜及其创作"],["l","p17.html","读《南行记》"],["l","p18.html","艾芜漂泊在缅甸"],["l","p19.html","艾芜年表简编"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
