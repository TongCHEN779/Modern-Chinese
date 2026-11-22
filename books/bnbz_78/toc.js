(function(){var D=[["l","p01.html","关大妈"],["l","p02.html","妯娌"],["l","p03.html","鱼圩边"],["l","p04.html","黎明前的故事"],["l","p05.html","新当选的团支书"],["l","p06.html","百合花"],["l","p07.html","高高的白杨树"],["l","p08.html","澄河边上"],["l","p09.html","如愿"],["l","p10.html","春暖时节"],["l","p11.html","里程"],["l","p12.html","静静的产院"],["l","p13.html","三走严庄"],["l","p14.html","同志之间"],["l","p15.html","阿舒"],["l","p16.html","第二步"],["l","p17.html","逝去的夜"],["l","p18.html","回头卒"],["l","p19.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
