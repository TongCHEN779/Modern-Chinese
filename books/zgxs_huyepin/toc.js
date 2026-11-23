(function(){var D=[["l","p01.html","前言"],["l","p02.html","到莫斯科去"],["l","p03.html","光明在我们的前面"],["l","p04.html","械斗"],["l","p05.html","中秋节"],["l","p06.html","珍珠耳坠子"],["l","p07.html","家长"],["l","p08.html","猫"],["l","p09.html","初恋的自白"],["l","p10.html","活珠子"],["l","p11.html","小人儿"],["l","p12.html","小小的旅途"],["l","p13.html","毁灭"],["l","p14.html","一群朋友"],["l","p15.html","傻子"],["l","p16.html","坟"],["l","p17.html","父亲和他的故事"],["l","p18.html","黎蒂"],["l","p19.html","他和他的家"],["l","p20.html","不能忘的影"],["l","p21.html","同居"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
