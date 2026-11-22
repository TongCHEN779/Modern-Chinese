(function(){var D=[["l","p01.html","2000年重版前言"],["l","p02.html","人物"],["l","p03.html","第一幕"],["l","p04.html","第二幕"],["l","p05.html","第三幕"],["l","p06.html","第四幕"],["l","p07.html","第五幕"],["g","附录"],["l","p08.html","关于《白毛女》的音乐(1945年)"],["l","p09.html","关于《白毛女》歌剧的创作(1946年)"],["l","p10.html","《白毛女》的创作与演出(1946年)"],["l","p11.html","《白毛女》音乐的创作经验(1946年)"],["l","p12.html","再版前言(1947年)"],["l","p13.html","前言(1950年)"],["l","p14.html","关于《白毛女》的修改(1962年)"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
