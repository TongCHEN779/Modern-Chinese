(function(){var D=[["l","p01.html","“西方古典学研究”总序"],["l","p02.html","导读"],["l","p03.html","“希腊罗马史料集”总序"],["l","p04.html","编者导言"],["l","p05.html","致谢"],["l","p06.html","缩写说明"],["l","p07.html","符号说明"],["g","史料译注"],["l","p08.html","史料译注 1–10"],["l","p09.html","史料译注 11–20"],["l","p10.html","史料译注 21–30"],["l","p11.html","史料译注 31–40"],["l","p12.html","史料译注 41–50"],["l","p13.html","史料译注 51–60"],["l","p14.html","史料译注 61–70"],["l","p15.html","史料译注 71–80"],["l","p16.html","史料译注 81–90"],["l","p17.html","史料译注 91–100"],["l","p18.html","史料译注 101–110"],["l","p19.html","史料译注 111–120"],["l","p20.html","史料译注 121–130"],["l","p21.html","史料译注 131–140"],["l","p22.html","术语表"],["l","p23.html","附录"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
