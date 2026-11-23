(function(){var D=[["g","第二编"],["l","p01.html","第八章 弗拉基米尔·柯罗连科"],["l","p02.html","第九章 马克西姆·高尔基"],["l","p03.html","第十章 伊万·布宁"],["l","p04.html","第十一章 亚历山大·库普林"],["l","p05.html","第十二章 维肯季·魏列萨耶夫"],["l","p06.html","第十三章 讽刺作家：阿韦尔琴科、苔菲、萨沙·乔尔内"],["l","p07.html","第十四章 20世纪头二十年的小说家：米哈伊尔·阿尔志巴绥夫、阿纳托利·卡缅斯基、阿纳斯塔西娅·维尔比茨卡娅"],["g","第三编"],["l","p08.html","第十五章 象征主义"],["l","p09.html","第十六章 弗拉基米尔·索洛维约夫"],["l","p10.html","第十七章 德米特里·梅列日科夫斯基"],["l","p11.html","第十八章 济娜伊达·吉皮乌斯"],["l","p12.html","第十九章 费奥多尔·索洛古勃"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
