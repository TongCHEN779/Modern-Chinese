(function(){var D=[["l","p001.html","杜牧简介"],["l","p002.html","前言"],["l","p003.html","卷一 赋三首"],["l","p004.html","卷一 诗二十八首"],["l","p005.html","卷二 律诗六十七首"],["l","p006.html","卷三 律诗八十八首"],["l","p007.html","卷四 长韵四首 律诗七十一首"],["l","p008.html","卷五"],["l","p009.html","卷六"],["l","p010.html","卷七"],["l","p011.html","卷八"],["l","p012.html","卷九"],["l","p013.html","卷十"],["l","p014.html","卷十一"],["l","p015.html","卷十二"],["l","p016.html","卷十三"],["l","p017.html","卷十四"],["l","p018.html","卷十五"],["l","p019.html","卷十六"],["l","p020.html","卷十七"],["l","p021.html","卷十八"],["l","p022.html","卷十九"],["l","p023.html","卷二十"],["l","p024.html","外集"],["l","p025.html","别集"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
