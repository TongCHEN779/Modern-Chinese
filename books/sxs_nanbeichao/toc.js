(function(){var D=[["l","p01.html","前言"],["g","南朝"],["l","p02.html","第一章 刘宋：南朝最为强大的朝代"],["l","p03.html","第二章 南齐：一个短命的王朝"],["l","p04.html","第三章 萧梁：“自我得之，自我失之”"],["l","p05.html","第四章 陈：“隔江犹唱后庭花”"],["g","北朝"],["l","p06.html","第一章 北魏：中国历史上第一个重要的少数民族朝代"],["l","p07.html","第二章 东魏、北齐：民族融合中的曲折"],["l","p08.html","第三章 西魏、北周：改革中走向强盛"],["g","附录"],["l","p09.html","附录一 南北朝的思想和宗教"],["l","p10.html","附录二 南北朝文学、史学和艺术的成就"],["l","p11.html","附录三 南北朝的科学技术成就"],["l","p12.html","附录四 南北朝历代皇帝年表"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
