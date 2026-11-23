(function(){var D=[["l","p01.html","“西方古典学研究”总序"],["l","p02.html","导读"],["l","p03.html","“希腊罗马史料集”总序"],["l","p04.html","编者导言"],["l","p05.html","缩写说明"],["l","p06.html","符号说明"],["g","史料译注"],["l","p07.html","史料译注 1–19"],["l","p08.html","史料译注 20–38"],["l","p09.html","史料译注 39–51"],["l","p10.html","史料译注 52–59b"],["l","p11.html","史料译注 60–72"],["l","p12.html","史料译注 73–87"],["l","p13.html","史料译注 88–102"],["l","p14.html","史料译注 103–112"],["l","p15.html","术语表"],["g","附录"],["l","p16.html","附录一　罗马人名"],["l","p17.html","附录二　罗马执政官"],["l","p18.html","附录三　希腊与罗马纪年"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
