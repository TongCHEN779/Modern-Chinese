(function(){var D=[["l","p01.html","前言"],["l","p02.html","第一章 努尔哈赤奠基大清"],["l","p03.html","第二章 大清奠基工程的完成者——皇太极"],["l","p04.html","第三章 清军入关，统一中原"],["l","p05.html","第四章 清初三先生"],["l","p06.html","第五章 康熙大帝开创盛世"],["l","p07.html","第六章 承上启下的改革型皇帝——雍正"],["l","p08.html","第七章 清初文字狱"],["l","p09.html","第八章 乾隆盛世"],["l","p10.html","第九章 曹雪芹与《红楼梦》"],["l","p11.html","第十章 大贪官和珅"],["l","p12.html","第十一章 “浓墨宰相”刘墉"],["l","p13.html","第十二章 白莲教和天理教起义"],["l","p14.html","第十三章 鸦片战争始末"],["l","p15.html","第十四章 魏源与《海国图志》"],["l","p16.html","第十五章 太平天国运动"],["l","p17.html","第十六章 辛酉政变始末"],["l","p18.html","第十七章 晚清中兴四大臣"],["l","p19.html","第十八章 百日维新始末"],["l","p20.html","第十九章 严复和《天演论》"],["l","p21.html","第二十章 义和团运动"],["l","p22.html","第二十一章 清末谴责小说"],["l","p23.html","第二十二章 清王朝的终结"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
