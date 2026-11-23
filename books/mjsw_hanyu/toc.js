(function(){var D=[["l","p001.html","韩愈简介"],["l","p002.html","总序"],["g","诗集"],["l","p003.html","诗集 卷一"],["l","p004.html","诗集 卷二"],["l","p005.html","诗集 卷三"],["l","p006.html","诗集 卷四"],["l","p007.html","诗集 卷五"],["l","p008.html","诗集 卷六"],["l","p009.html","诗集 卷七"],["l","p010.html","诗集 卷八"],["l","p011.html","诗集 卷九"],["l","p012.html","诗集 卷十"],["l","p013.html","诗集 卷十一"],["l","p014.html","诗集 卷十二"],["g","文集"],["l","p015.html","文集 卷一 赋杂著"],["l","p016.html","文集 卷二 杂著书启"],["l","p017.html","文集 卷三 书"],["l","p018.html","文集 卷四 序"],["l","p019.html","文集 卷五 哀辞祭文"],["l","p020.html","文集 卷六 碑志"],["l","p021.html","文集 卷七 碑志"],["l","p022.html","文集 卷八 杂文状表状"],["g","文外集"],["l","p023.html","文外集 上"],["l","p024.html","文外集 下"],["g","集外文"],["l","p025.html","集外文 附录"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
