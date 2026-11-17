(function(){var D=[["l","p01.html","自序"],["g","百年中国的政治激流"],["l","p02.html","一、中国现代化的历史反思"],["l","p03.html","二、现代中国的自由主义思潮与运动"],["l","p04.html","三、在自由与公正之间：社会民主主义在中国"],["l","p05.html","四、现代中国的公共领域"],["g","大时代中的知识分子困境"],["l","p06.html","五、重建社会重心：现代中国的知识分子社会"],["l","p07.html","六、「少数人的责任」：知识分子的士大夫意识"],["l","p08.html","七、城市「权力的文化网络」中的知识分子"],["l","p09.html","八、中国知识分子群体人格的历史探索"],["l","p10.html","九、入世与出世：进退维谷的两难困境"],["l","p11.html","十、外圆与内方：近代知识分子的双重人格"],["g","现代中国的政治正当性"],["l","p12.html","十一、正当性的三种历史类型"],["l","p13.html","十二、从天德正当性到历史正当性"],["l","p14.html","十三、从公共善到个人自由与权利"],["l","p15.html","十四、国家富强正当性的出现及其冲突"],["l","p16.html","十五、政治的精神：个人、良知和公意"],["l","p17.html","十六、正当性基础：民主抑或宪政？"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
