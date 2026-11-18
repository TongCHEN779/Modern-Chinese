(function(){var D=[["l","p01.html","史记选序例"],["l","p02.html","项羽本纪"],["l","p03.html","陈涉世家"],["l","p04.html","留侯世家"],["l","p05.html","陈丞相世家"],["l","p06.html","孙子吴起列传"],["l","p07.html","商君列传"],["l","p08.html","平原君虞卿列传"],["l","p09.html","魏公子列传"],["l","p10.html","范睢蔡泽列传"],["l","p11.html","廉颇蔺相如列传"],["l","p12.html","田单列传"],["l","p13.html","刺客列传"],["l","p14.html","淮阴侯列传"],["l","p15.html","季布栾布列传"],["l","p16.html","张释之冯唐列传"],["l","p17.html","魏其武安侯列传"],["l","p18.html","李将军列传"],["l","p19.html","汲郑列传"],["l","p20.html","游侠列传"],["l","p21.html","滑稽列传"],["l","p22.html","后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
