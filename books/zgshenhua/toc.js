(function(){var D=[["l","p01.html","序"],["l","p02.html","增订版序"],["g","第一篇 东北族群及其创世神话"],["l","p03.html","第一章 序论——环渤海湾地域的古亚洲文明"],["l","p04.html","第二章 通古斯族群及其创世神话"],["l","p05.html","第三章 蒙古族源流及其始祖传说"],["l","p06.html","第四章 朱蒙神话——中韩太阳始祖神话之比较"],["g","第二篇 西南族群及其创世神话"],["l","p07.html","第一章 序论"],["l","p08.html","第二章 氐羌族群及其创世神话"],["l","p09.html","第三章 藏族源流及其始祖传说"],["l","p10.html","第四章 百越族群及其创世神话"],["l","p11.html","第五章 台湾高山族始祖传说"],["l","p12.html","第六章 苗蛮族群及其创世神话"],["l","p13.html","第七章 西南民族创世神话研究的综合结论"],["l","p14.html","附录一 乱神蚩尤与枫木信仰"],["l","p15.html","附录二 绝地天通——昆仑神话主题解说"],["l","p16.html","附录三 从贺兰山到泸沽湖——摩梭、普米的民族亲缘关系及其文化传承"],["l","p17.html","参考文献资料"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
