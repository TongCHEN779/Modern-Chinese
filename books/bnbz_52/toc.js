(function(){var D=[["l","p01.html","果园城"],["l","p02.html","“鬼爷”"],["l","p03.html","葛天民"],["l","p04.html","桃红"],["l","p05.html","贺文龙的文稿"],["l","p06.html","颜料盒"],["l","p07.html","傲骨"],["l","p08.html","阿嚏"],["l","p09.html","塔"],["l","p10.html","期待"],["l","p11.html","说书人"],["l","p12.html","灯"],["l","p13.html","邮差先生"],["l","p14.html","狩猎"],["l","p15.html","吻"],["l","p16.html","三个小人物"],["l","p17.html","北门街的好汉"],["l","p18.html","新版后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
