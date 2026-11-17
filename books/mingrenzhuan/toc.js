(function(){var D=[["l","p01.html","译本序"],["l","p02.html","贝多芬传"],["l","p03.html","米开朗琪罗传"],["l","p04.html","托尔斯泰传"],["l","p05.html","托尔斯泰的遗作简析"],["l","p06.html","亚洲对托尔斯泰的反响"],["l","p07.html","托尔斯泰逝世前两个月写给甘地的信"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
