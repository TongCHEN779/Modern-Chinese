(function(){var D=[["g","第三编"],["l","p01.html","第二十章 康斯坦丁·巴尔蒙特"],["l","p02.html","第二十一章 瓦列里·勃留索夫"],["l","p03.html","第二十二章 因诺肯季·安年斯基"],["l","p04.html","第二十三章 亚历山大·布洛克"],["l","p05.html","第二十四章 安德列·别雷"],["l","p06.html","第二十五章 维亚切斯拉夫·伊万诺夫"],["l","p07.html","第二十六章 马克西米里安·沃洛申"],["g","第四编"],["l","p08.html","第二十七章 列昂尼德·安德列耶夫"],["l","p09.html","第二十八章 阿列克谢·列米卓夫"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
